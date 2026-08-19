import { createHash, timingSafeEqual } from "node:crypto";
import { createServer } from "node:http";
import { basename, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { WebSocketServer } from "ws";
import { assertGatewayExposureConfig, assertHermesApiConfig, assertRealtimeProviderConfig, makeSessionKey, } from "../../../config.js";
import { LiveGatewaySession } from "../../../application/live-gateway/live-gateway-session.js";
import { TaskSupervisor } from "../../../application/task-supervisor/task-supervisor.js";
import { HermesClient } from "../../outbound/hermes/hermes-runs.client.js";
import { createLiveModelAdapter } from "../../outbound/realtime/factory.js";
import { FileTaskStore } from "../../outbound/task-store/file-task-store.js";
import { buildReadinessReport } from "../../../readiness.js";
import { serveStatic } from "./static.js";
import { WebSocketClientConnection } from "./websocket-client-connection.js";
import { errorToMessage } from "../../../domain/error-message.js";
import { HERMES_LIVE_PROTOCOL_VERSION, HERMES_LIVE_SUPPORTED_PROTOCOL_VERSIONS, } from "../../../domain/protocol/version.js";
import { realtimeClientCapabilities } from "../../../application/live-gateway/client-capabilities.js";
import { negotiateHermesApprovalCompatibility } from "../../../application/live-gateway/hermes-approval-compatibility.js";
import { HERMES_LIVE_SERVICE_ID } from "../../../service-identity.js";
const SERVER_SESSION_CLOSE_TIMEOUT_MS = 6_000;
const SERVER_WEBSOCKET_CLOSE_GRACE_MS = 250;
const SERVER_WEBSOCKET_FORCE_WAIT_MS = 1_000;
const SERVER_HTTP_CLOSE_TIMEOUT_MS = 2_000;
export async function startServer({ config, logger, hermes: providedHermes, liveModel: providedLiveModel, taskSupervisor: providedTaskSupervisor, signal, }) {
    assertGatewayExposureConfig(config);
    if (!providedHermes) {
        assertHermesApiConfig(config);
    }
    if (!providedLiveModel) {
        assertRealtimeProviderConfig(config);
    }
    const hermes = providedHermes ?? new HermesClient(config.hermes);
    const liveModel = providedLiveModel ?? createLiveModelAdapter(config);
    const taskSupervisor = providedTaskSupervisor ?? new TaskSupervisor({
        store: new FileTaskStore({
            directory: dirname(config.tasks.stateFile),
            filename: basename(config.tasks.stateFile),
            maxRecords: config.tasks.historyLimit + config.tasks.maxConcurrent + config.tasks.maxQueued,
            retentionMs: config.tasks.retentionMs,
            terminalReserveSlots: config.tasks.maxConcurrent,
        }),
        hermes,
        maxConcurrent: config.tasks.maxConcurrent,
        trustDeclaredReadOnly: config.tasks.trustDeclaredReadOnly === true,
        maxQueued: config.tasks.maxQueued,
        pollIntervalMs: config.tasks.pollIntervalMs,
        ...(config.hermes.instructions ? { runInstructions: config.hermes.instructions } : {}),
        onError: (error) => logger.error("background task supervisor error", { error: errorToMessage(error) }),
    });
    const defaultSessionKey = makeSessionKey(config.server.sessionPrefix, config.server.defaultProfileId, config.server.defaultUserLabel);
    let startupAbortClose;
    const closeTaskStateForAbort = () => {
        if (!startupAbortClose) {
            // Always settle this promise. The abort listener can run while
            // initialize() is still pending, so rethrowing here would briefly leave
            // a rejected promise without a handler. The startup path inspects and
            // propagates the captured cleanup failure before it rejects.
            startupAbortClose = Promise.resolve().then(() => taskSupervisor.close()).then(() => ({ ok: true }), (error) => {
                logger.error("failed to close task supervisor during startup cleanup", {
                    error: errorToMessage(error),
                });
                return { ok: false, error };
            });
        }
        return startupAbortClose;
    };
    if (signal?.aborted)
        closeTaskStateForAbort();
    else
        signal?.addEventListener("abort", closeTaskStateForAbort, { once: true });
    try {
        if (signal?.aborted)
            throw startupAbortError(signal);
        taskSupervisor.registerOwner(defaultSessionKey, defaultSessionKey);
        await taskSupervisor.initialize();
        if (signal?.aborted)
            throw startupAbortError(signal);
    }
    catch (error) {
        signal?.removeEventListener("abort", closeTaskStateForAbort);
        const closeResult = await closeTaskStateForAbort();
        if (!closeResult.ok) {
            throw startupCleanupError(signal?.aborted ? startupAbortError(signal) : error, closeResult.error);
        }
        if (signal?.aborted)
            throw startupAbortError(signal);
        throw error;
    }
    const demoRoot = resolveDemoRoot();
    const browserClientRoot = resolveBrowserClientRoot();
    const sessions = new Set();
    const server = createServer(async (req, res) => {
        try {
            await handleHttp(req, res, {
                config,
                hermes,
                taskSupervisor,
                demoRoot,
                browserClientRoot,
                requireHermesApiKey: !providedHermes,
                requireRealtimeProviderConfig: !providedLiveModel,
            });
        }
        catch (error) {
            const message = errorToMessage(error);
            logger.error("http handler failed", { error: message });
            json(req, res, 500, { status: "error", error: "Internal server error." });
        }
    });
    const wss = new WebSocketServer({ noServer: true, maxPayload: clientWebSocketMaxPayload(config) });
    server.on("upgrade", (req, socket, head) => {
        let url;
        try {
            url = parseRequestTarget(req.url);
            if (!parseHttpHost(req.headers.host, "http:")) {
                throw new TypeError("Invalid Host header");
            }
        }
        catch {
            rejectMalformedUpgrade(socket);
            return;
        }
        if (url.pathname !== "/v1/live") {
            socket.destroy();
            return;
        }
        if (!isWebSocketOriginAllowed(req, config)) {
            socket.write("HTTP/1.1 403 Forbidden\r\n\r\n");
            socket.destroy();
            return;
        }
        if (!isAuthorized(req, config, url, { allowQueryToken: true })) {
            socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n");
            socket.destroy();
            return;
        }
        if (sessions.size >= config.server.maxSessions) {
            socket.write("HTTP/1.1 503 Service Unavailable\r\nRetry-After: 5\r\n\r\n");
            socket.destroy();
            return;
        }
        wss.handleUpgrade(req, socket, head, (ws) => {
            const session = new LiveGatewaySession(new WebSocketClientConnection(ws), {
                config,
                hermes,
                liveModel,
                taskSupervisor,
                logger,
            });
            sessions.add(session);
            ws.once("close", () => {
                void session.close()
                    .catch((error) => {
                    logger.error("live session cleanup failed", {
                        error: errorToMessage(error),
                    });
                })
                    .finally(() => sessions.delete(session));
            });
            session.bind();
            let socketAlive = true;
            const socketHeartbeat = setInterval(() => {
                if (ws.readyState !== ws.OPEN) return;
                if (!socketAlive) {
                    logger.warn("live websocket heartbeat expired", { sessionId: session.id });
                    ws.terminate();
                    return;
                }
                socketAlive = false;
                ws.ping();
            }, 15000);
            ws.on("pong", () => {
                socketAlive = true;
            });
            ws.once("close", () => {
                clearInterval(socketHeartbeat);
            });
            wss.emit("connection", ws, req);
        });
    });
    try {
        await listenHttpServer(server, config.server.port, config.server.host);
    }
    catch (error) {
        signal?.removeEventListener("abort", closeTaskStateForAbort);
        await new Promise((resolve) => wss.close(() => resolve()));
        const closeResult = await closeTaskStateForAbort();
        if (!closeResult.ok)
            throw startupCleanupError(error, closeResult.error);
        throw error;
    }
    if (signal?.aborted) {
        signal.removeEventListener("abort", closeTaskStateForAbort);
        await new Promise((resolve) => wss.close(() => resolve()));
        await closeHttpServer(server);
        const closeResult = await closeTaskStateForAbort();
        if (!closeResult.ok)
            throw startupCleanupError(startupAbortError(signal), closeResult.error);
        throw startupAbortError(signal);
    }
    signal?.removeEventListener("abort", closeTaskStateForAbort);
    const address = server.address();
    const port = address?.port ?? config.server.port;
    const url = `http://${config.server.host}:${port}`;
    logger.info("hermes-live listening", { url });
    let closePromise;
    const close = () => {
        if (!closePromise) {
            closePromise = (async () => {
                // Stop accepting HTTP requests and WebSocket upgrades before waiting
                // for any client/provider cleanup.
                const httpClosing = closeHttpServer(server);
                // Session cleanup may take several seconds. Attach a rejection handler
                // immediately so an early server.close callback error cannot surface as
                // an unhandled rejection before the ordered aggregation below awaits it.
                void httpClosing.catch(() => undefined);
                const shutdownFailures = [];
                try {
                    server.closeIdleConnections();
                }
                catch (error) {
                    shutdownFailures.push(error);
                }
                try {
                    const sessionResults = await Promise.allSettled(Array.from(sessions, (session) => withServerDeadline(session.close(), SERVER_SESSION_CLOSE_TIMEOUT_MS, "Live session did not close before the server shutdown deadline.")));
                    for (const result of sessionResults) {
                        if (result.status === "rejected")
                            shutdownFailures.push(result.reason);
                    }
                }
                catch (error) {
                    shutdownFailures.push(error);
                }
                try {
                    await closeWebSocketServer(wss);
                }
                catch (error) {
                    shutdownFailures.push(error);
                }
                try {
                    server.closeAllConnections();
                }
                catch (error) {
                    shutdownFailures.push(error);
                }
                try {
                    await withServerDeadline(httpClosing, SERVER_HTTP_CLOSE_TIMEOUT_MS, "HTTP server did not close before the shutdown deadline.");
                }
                catch (error) {
                    shutdownFailures.push(error);
                }
                for (const client of wss.clients) {
                    try {
                        client.terminate();
                    }
                    catch (error) {
                        shutdownFailures.push(error);
                    }
                }
                try {
                    server.closeAllConnections();
                }
                catch (error) {
                    shutdownFailures.push(error);
                }
                // Task-state ownership must be released even when transport teardown
                // reports an error; otherwise a normal shutdown can look like a crash.
                try {
                    await taskSupervisor.close();
                }
                catch (error) {
                    shutdownFailures.push(error);
                }
                if (shutdownFailures.length === 1)
                    throw shutdownFailures[0];
                if (shutdownFailures.length > 1) {
                    throw new AggregateError(shutdownFailures, "Hermes Live server shutdown encountered multiple cleanup failures.");
                }
            })();
        }
        return closePromise;
    };
    return {
        url,
        close,
    };
}
function startupAbortError(signal) {
    return signal.reason instanceof Error
        ? signal.reason
        : new Error("Hermes Live startup was aborted before the server became ready.");
}
function startupCleanupError(startupError, cleanupError) {
    return new AggregateError([startupError, cleanupError], `Hermes Live startup failed and task-state cleanup also failed: ${errorToMessage(cleanupError)}`);
}
function closeHttpServer(server) {
    return new Promise((resolve, reject) => {
        server.close((error) => (error ? reject(error) : resolve()));
    });
}
async function closeWebSocketServer(wss) {
    for (const client of wss.clients)
        client.close(1001, "server shutdown");
    const closed = new Promise((resolve) => {
        try {
            wss.close(() => resolve());
        }
        catch {
            resolve();
        }
    });
    if (await settlesWithin(closed, SERVER_WEBSOCKET_CLOSE_GRACE_MS))
        return;
    for (const client of wss.clients)
        client.terminate();
    await settlesWithin(closed, SERVER_WEBSOCKET_FORCE_WAIT_MS);
}
async function settlesWithin(promise, timeoutMs) {
    let timeout;
    try {
        return await Promise.race([
            promise.then(() => true, () => true),
            new Promise((resolve) => {
                timeout = setTimeout(() => resolve(false), timeoutMs);
            }),
        ]);
    }
    finally {
        if (timeout)
            clearTimeout(timeout);
    }
}
async function withServerDeadline(promise, timeoutMs, message) {
    let timeout;
    try {
        return await Promise.race([
            promise,
            new Promise((_resolve, reject) => {
                timeout = setTimeout(() => reject(new Error(message)), timeoutMs);
            }),
        ]);
    }
    finally {
        if (timeout)
            clearTimeout(timeout);
    }
}
async function handleHttp(req, res, options) {
    addCors(req, res, options.config);
    if (req.method === "OPTIONS") {
        res.writeHead(204);
        res.end();
        return;
    }
    const url = parseRequestTarget(req.url);
    if (url.pathname === "/health") {
        if (!isGetOrHead(req)) {
            methodNotAllowed(req, res, "GET, HEAD");
            return;
        }
        json(req, res, 200, { status: "ok", service: HERMES_LIVE_SERVICE_ID });
        return;
    }
    if (requiresHttpAuth(url.pathname) && !isAuthorized(req, options.config, url, { allowQueryToken: false })) {
        json(req, res, 401, { status: "unauthorized" });
        return;
    }
    if (url.pathname === "/ready") {
        if (!isGetOrHead(req)) {
            methodNotAllowed(req, res, "GET, HEAD");
            return;
        }
        const report = await buildReadinessReport(options.config, {
            hermes: options.hermes,
            tasks: options.taskSupervisor,
            requireHermesApiKey: options.requireHermesApiKey,
            requireRealtimeProviderConfig: options.requireRealtimeProviderConfig,
        });
        json(req, res, report.ok ? 200 : 503, {
            status: report.ok ? "ready" : "not_ready",
            service: HERMES_LIVE_SERVICE_ID,
            checks: {
                gateway: report.gateway,
                hermes: report.hermes,
                realtime: report.realtime,
                tasks: report.tasks,
            },
        });
        return;
    }
    if (url.pathname === "/v1/capabilities") {
        if (!isGetOrHead(req)) {
            methodNotAllowed(req, res, "GET, HEAD");
            return;
        }
        const approvals = await negotiateHermesApprovalCompatibility(options.hermes);
        json(req, res, 200, {
            object: "hermes_live.capabilities",
            service: HERMES_LIVE_SERVICE_ID,
            protocolVersion: HERMES_LIVE_PROTOCOL_VERSION,
            supportedProtocolVersions: HERMES_LIVE_SUPPORTED_PROTOCOL_VERSIONS,
            websocket: { path: "/v1/live", protocol: "json-base64-audio" },
            realtime: realtimeClientCapabilities(options.config),
            hermes: { approvals },
            tasks: {
                scope: "owner",
                durable: true,
                persistence: "local_file",
                disconnectContinuation: true,
                gatewayRestartRecovery: "reconcile_by_upstream_run_id",
                hermesRestartRecovery: false,
                ambiguousDispatch: "fenced_no_automatic_retry",
                declaredReadOnlyTrusted: options.config.tasks.trustDeclaredReadOnly === true,
                maxConcurrent: options.config.tasks.maxConcurrent,
                maxQueued: options.config.tasks.maxQueued,
                maxRetained: options.config.tasks.historyLimit,
                retentionMs: options.config.tasks.retentionMs,
                pollIntervalMs: options.config.tasks.pollIntervalMs,
            },
            features: {
                auth_required: Boolean(options.config.server.authToken),
                server_managed_identity: !options.config.server.trustClientIdentity,
                max_sessions: options.config.server.maxSessions,
                huggingface_local: options.config.realtime.provider === "local",
                gemini_live: options.config.realtime.provider === "gemini",
                openai_realtime: options.config.realtime.provider === "openai",
                mock_live: options.config.realtime.provider === "mock",
                hermes_runs: true,
                hermes_conversations: true,
                conversation_create: true,
                conversation_resume: true,
                background_tasks: true,
                durable_task_state: true,
                task_reconnect_snapshot: true,
                parallel_read_only_tasks: options.config.tasks.maxConcurrent > 1 && options.config.tasks.trustDeclaredReadOnly === true,
                exact_task_stop: true,
                task_notifications: true,
                hermes_run_events_internal: true,
                hermes_stop: true,
                hermes_approval: false,
                hermes_approval_ui: false,
                hermes_approval_fallback_deny_all: approvals.fallback === "deny_all_then_stop",
                hermes_approval_fallback_stops_run: true,
                hermes_approval_requires_targeted_response: true,
                browser_demo: options.config.server.demoEnabled,
                optional_hermes_plugin: true,
            },
        });
        return;
    }
    if (url.pathname === "/v1/conversations") {
        const assertSessionsSupported = options.hermes.assertSessionsSupported;
        const listSessions = options.hermes.listSessions;
        const createSession = options.hermes.createSession;
        if (!assertSessionsSupported || !listSessions || !createSession) {
            json(req, res, 503, { status: "unavailable", error: "Hermes session continuity is unavailable." });
            return;
        }
        if (isGetOrHead(req)) {
            const limit = boundedQueryInteger(url, "limit", 20, 1, 100);
            const offset = boundedQueryInteger(url, "offset", 0, 0, 100_000);
            if (limit === undefined || offset === undefined) {
                json(req, res, 400, { status: "invalid_request", error: "Conversation pagination is invalid." });
                return;
            }
            const source = url.searchParams.get("source")?.trim();
            if (source !== undefined && (source.length === 0 || source.length > 64)) {
                json(req, res, 400, { status: "invalid_request", error: "Conversation source is invalid." });
                return;
            }
            await assertSessionsSupported.call(options.hermes);
            const conversations = await listSessions.call(options.hermes, {
                limit,
                offset,
                ...(source ? { source } : {}),
            });
            json(req, res, 200, { object: "list", conversations });
            return;
        }
        if (req.method === "POST") {
            const parsed = await readBoundedJsonObject(req, 16_384);
            if (!parsed.ok) {
                json(req, res, parsed.status, { status: "invalid_request", error: parsed.error });
                return;
            }
            const keys = Object.keys(parsed.value);
            const title = parsed.value.title;
            if (keys.some((key) => key !== "title") || (title !== undefined && (typeof title !== "string" || title.trim().length === 0 || title.trim().length > 100))) {
                json(req, res, 400, { status: "invalid_request", error: "Conversation title is invalid." });
                return;
            }
            await assertSessionsSupported.call(options.hermes);
            const conversation = await createSession.call(options.hermes, {
                ...(typeof title === "string" ? { title: title.trim() } : {}),
            });
            json(req, res, 201, { object: "hermes_live.conversation", conversation });
            return;
        }
        methodNotAllowed(req, res, "GET, HEAD, POST");
        return;
    }
    if (options.config.server.demoEnabled && serveStatic(req, res, { root: options.demoRoot })) {
        return;
    }
    if (options.config.server.demoEnabled &&
        (url.pathname === "/hermes-live-client.js" || url.pathname === "/mic-worklet.js") &&
        serveStatic(req, res, { root: options.browserClientRoot })) {
        return;
    }
    json(req, res, 404, { status: "not_found" });
}
function isAuthorized(req, config, url, options) {
    if (!config.server.authToken) {
        return true;
    }
    const bearer = bearerToken(req.headers.authorization);
    const queryToken = options.allowQueryToken ? url.searchParams.get("token") : undefined;
    return secureTokenEqual(bearer, config.server.authToken) || secureTokenEqual(queryToken, config.server.authToken);
}
function requiresHttpAuth(pathname) {
    return pathname === "/ready" || pathname === "/v1/capabilities" || pathname === "/v1/conversations";
}
function isWebSocketOriginAllowed(req, config) {
    const origin = req.headers.origin;
    if (!origin) {
        return true;
    }
    if (config.server.allowOrigin === "*") {
        return true;
    }
    if (config.server.allowOrigin) {
        return origin === config.server.allowOrigin;
    }
    const originUrl = parseBrowserOrigin(origin);
    const requestHost = originUrl
        ? parseHttpHost(req.headers.host, originUrl.protocol === "https:" ? "https:" : "http:")
        : undefined;
    return (originUrl !== undefined &&
        requestHost !== undefined &&
        isLoopbackHostname(originUrl.hostname) &&
        isLoopbackHostname(requestHost.hostname) &&
        effectivePort(originUrl) === effectivePort(requestHost));
}
function parseBrowserOrigin(origin) {
    if (origin !== origin.trim()) {
        return undefined;
    }
    try {
        const parsed = new URL(origin);
        if ((parsed.protocol !== "http:" && parsed.protocol !== "https:") ||
            parsed.username ||
            parsed.password ||
            parsed.search ||
            parsed.hash ||
            parsed.origin !== origin) {
            return undefined;
        }
        return parsed;
    }
    catch {
        return undefined;
    }
}
function parseHttpHost(host, protocol) {
    if (!host || host !== host.trim()) {
        return undefined;
    }
    try {
        const parsed = new URL(`${protocol}//${host}`);
        if (parsed.username || parsed.password || parsed.pathname !== "/" || parsed.search || parsed.hash) {
            return undefined;
        }
        return parsed;
    }
    catch {
        return undefined;
    }
}
function parseRequestTarget(target) {
    return new URL(target ?? "/", "http://localhost");
}
function rejectMalformedUpgrade(socket) {
    socket.end("HTTP/1.1 400 Bad Request\r\nConnection: close\r\nContent-Length: 0\r\n\r\n", () => socket.destroy());
}
function isLoopbackHostname(hostname) {
    const normalized = hostname.toLowerCase().replace(/^\[|\]$/g, "").replace(/\.$/, "");
    if (normalized === "localhost" || normalized === "::1") {
        return true;
    }
    const octets = normalized.split(".");
    return octets.length === 4 && octets[0] === "127" && octets.every((octet) => /^(?:0|[1-9]\d{0,2})$/.test(octet) && Number(octet) <= 255);
}
function effectivePort(url) {
    if (url.protocol === "http:") {
        return url.port || "80";
    }
    if (url.protocol === "https:") {
        return url.port || "443";
    }
    return undefined;
}
function addCors(req, res, config) {
    const origin = req.headers.origin;
    if (!origin) {
        return;
    }
    if (config.server.allowOrigin === "*" || config.server.allowOrigin === origin) {
        res.setHeader("access-control-allow-origin", origin);
        res.setHeader("vary", "origin");
        res.setHeader("access-control-allow-headers", "authorization, content-type");
        res.setHeader("access-control-allow-methods", "GET, HEAD, POST, OPTIONS");
    }
}
function boundedQueryInteger(url, name, fallback, minimum, maximum) {
    const raw = url.searchParams.get(name);
    if (raw === null)
        return fallback;
    if (!/^(?:0|[1-9]\d*)$/u.test(raw))
        return undefined;
    const value = Number(raw);
    return Number.isSafeInteger(value) && value >= minimum && value <= maximum ? value : undefined;
}
async function readBoundedJsonObject(req, maxBytes) {
    const contentLength = Number(req.headers["content-length"] ?? 0);
    if (Number.isFinite(contentLength) && contentLength > maxBytes) {
        return { ok: false, status: 413, error: "Request body is too large." };
    }
    const chunks = [];
    let bytes = 0;
    for await (const chunk of req) {
        const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
        bytes += buffer.byteLength;
        if (bytes > maxBytes)
            return { ok: false, status: 413, error: "Request body is too large." };
        chunks.push(buffer);
    }
    try {
        const value = JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}");
        if (!value || typeof value !== "object" || Array.isArray(value))
            throw new Error("invalid");
        return { ok: true, value: value };
    }
    catch {
        return { ok: false, status: 400, error: "Request body must be a JSON object." };
    }
}
function isGetOrHead(req) {
    return req.method === "GET" || req.method === "HEAD";
}
function methodNotAllowed(req, res, allow) {
    json(req, res, 405, { status: "method_not_allowed", allow }, { allow });
}
function json(req, res, status, body, headers = {}) {
    const payload = JSON.stringify(body);
    res.writeHead(status, {
        "content-type": "application/json; charset=utf-8",
        "content-length": String(Buffer.byteLength(payload)),
        "cache-control": "no-store",
        "referrer-policy": "no-referrer",
        "x-content-type-options": "nosniff",
        "x-frame-options": "DENY",
        ...headers,
    });
    if (req.method === "HEAD") {
        res.end();
    }
    else {
        res.end(payload);
    }
}
function bearerToken(authorization) {
    if (!authorization) {
        return undefined;
    }
    const [scheme, ...rest] = authorization.trim().split(/\s+/);
    if (scheme?.toLowerCase() !== "bearer" || rest.length !== 1) {
        return undefined;
    }
    return rest[0];
}
function secureTokenEqual(actual, expected) {
    if (!actual) {
        return false;
    }
    const actualHash = createHash("sha256").update(actual).digest();
    const expectedHash = createHash("sha256").update(expected).digest();
    return timingSafeEqual(actualHash, expectedHash);
}
function clientWebSocketMaxPayload(config) {
    const base64AudioBytes = Math.ceil((config.server.maxAudioBytes * 4) / 3);
    const textBytes = config.server.maxTextChars * 6;
    return Math.max(base64AudioBytes, textBytes) + 4096;
}
function resolveDemoRoot() {
    const current = dirname(fileURLToPath(import.meta.url));
    return join(current, "..", "..", "..", "..", "apps", "web-demo");
}
function resolveBrowserClientRoot() {
    const current = dirname(fileURLToPath(import.meta.url));
    return join(current, "..", "..", "..", "..", "clients", "browser");
}
function listenHttpServer(server, port, host) {
    return new Promise((resolve, reject) => {
        const cleanup = () => {
            server.off("error", onError);
            server.off("listening", onListening);
        };
        const onError = (error) => {
            cleanup();
            reject(new Error(`Failed to start hermes-live on ${host}:${port}: ${error.message}`));
        };
        const onListening = () => {
            cleanup();
            resolve();
        };
        server.once("error", onError);
        server.once("listening", onListening);
        server.listen(port, host);
    });
}
//# sourceMappingURL=server.js.map