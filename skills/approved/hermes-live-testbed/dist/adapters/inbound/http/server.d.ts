import { type AppConfig } from "../../../config.js";
import type { HermesRunsPort } from "../../../application/live-gateway/ports/hermes-runs.port.js";
import type { TaskSupervisorPort } from "../../../application/live-gateway/ports/task-supervisor.port.js";
import type { LiveModelAdapter } from "../../../application/live-gateway/ports/realtime-model.port.js";
import type { Logger } from "../../../logger.js";
export interface StartServerOptions {
    config: AppConfig;
    logger: Logger;
    hermes?: HermesRunsPort;
    liveModel?: LiveModelAdapter;
    taskSupervisor?: TaskSupervisorRuntime;
    signal?: AbortSignal;
}
export interface TaskSupervisorRuntime extends TaskSupervisorPort {
    initialize(): Promise<void>;
    close(): Promise<void>;
    health(): Promise<void>;
}
export declare function startServer({ config, logger, hermes: providedHermes, liveModel: providedLiveModel, taskSupervisor: providedTaskSupervisor, signal, }: StartServerOptions): Promise<{
    close(): Promise<void>;
    url: string;
}>;
//# sourceMappingURL=server.d.ts.map