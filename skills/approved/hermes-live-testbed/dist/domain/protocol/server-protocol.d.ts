import { z } from "zod";
export declare const RealtimeClientCapabilitiesSchema: z.ZodObject<{
    provider: z.ZodEnum<["local", "gemini", "openai", "mock"]>;
    model: z.ZodString;
    audio: z.ZodObject<{
        input: z.ZodObject<{
            enabled: z.ZodBoolean;
            mimeType: z.ZodOptional<z.ZodString>;
            recommendedFrameMs: z.ZodOptional<z.ZodNumber>;
        }, "strict", z.ZodTypeAny, {
            enabled: boolean;
            mimeType?: string | undefined;
            recommendedFrameMs?: number | undefined;
        }, {
            enabled: boolean;
            mimeType?: string | undefined;
            recommendedFrameMs?: number | undefined;
        }>;
        output: z.ZodObject<{
            enabled: z.ZodBoolean;
            mimeType: z.ZodOptional<z.ZodString>;
        }, "strict", z.ZodTypeAny, {
            enabled: boolean;
            mimeType?: string | undefined;
        }, {
            enabled: boolean;
            mimeType?: string | undefined;
        }>;
        turnDetection: z.ZodEnum<["disabled", "semantic_vad", "server_vad", "provider", "none"]>;
    }, "strict", z.ZodTypeAny, {
        input: {
            enabled: boolean;
            mimeType?: string | undefined;
            recommendedFrameMs?: number | undefined;
        };
        output: {
            enabled: boolean;
            mimeType?: string | undefined;
        };
        turnDetection: "disabled" | "none" | "provider" | "semantic_vad" | "server_vad";
    }, {
        input: {
            enabled: boolean;
            mimeType?: string | undefined;
            recommendedFrameMs?: number | undefined;
        };
        output: {
            enabled: boolean;
            mimeType?: string | undefined;
        };
        turnDetection: "disabled" | "none" | "provider" | "semantic_vad" | "server_vad";
    }>;
}, "strict", z.ZodTypeAny, {
    provider: "gemini" | "local" | "mock" | "openai";
    model: string;
    audio: {
        input: {
            enabled: boolean;
            mimeType?: string | undefined;
            recommendedFrameMs?: number | undefined;
        };
        output: {
            enabled: boolean;
            mimeType?: string | undefined;
        };
        turnDetection: "disabled" | "none" | "provider" | "semantic_vad" | "server_vad";
    };
}, {
    provider: "gemini" | "local" | "mock" | "openai";
    model: string;
    audio: {
        input: {
            enabled: boolean;
            mimeType?: string | undefined;
            recommendedFrameMs?: number | undefined;
        };
        output: {
            enabled: boolean;
            mimeType?: string | undefined;
        };
        turnDetection: "disabled" | "none" | "provider" | "semantic_vad" | "server_vad";
    };
}>;
export type RealtimeClientCapabilities = z.infer<typeof RealtimeClientCapabilitiesSchema>;
export declare const TaskCapabilitiesSchema: z.ZodObject<{
    scope: z.ZodLiteral<"owner">;
    sequence: z.ZodLiteral<"per_task">;
    reconnect: z.ZodLiteral<"snapshot">;
    durable: z.ZodBoolean;
    parallel: z.ZodBoolean;
    maxConcurrent: z.ZodNumber;
    maxRetained: z.ZodNumber;
    supports: z.ZodObject<{
        list: z.ZodBoolean;
        get: z.ZodBoolean;
        stop: z.ZodBoolean;
        followUp: z.ZodBoolean;
        resume: z.ZodLiteral<false>;
        notificationAck: z.ZodBoolean;
    }, "strict", z.ZodTypeAny, {
        list: boolean;
        get: boolean;
        stop: boolean;
        followUp: boolean;
        resume: false;
        notificationAck: boolean;
    }, {
        list: boolean;
        get: boolean;
        stop: boolean;
        followUp: boolean;
        resume: false;
        notificationAck: boolean;
    }>;
}, "strict", z.ZodTypeAny, {
    scope: "owner";
    sequence: "per_task";
    reconnect: "snapshot";
    durable: boolean;
    parallel: boolean;
    maxConcurrent: number;
    maxRetained: number;
    supports: {
        list: boolean;
        get: boolean;
        stop: boolean;
        followUp: boolean;
        resume: false;
        notificationAck: boolean;
    };
}, {
    scope: "owner";
    sequence: "per_task";
    reconnect: "snapshot";
    durable: boolean;
    parallel: boolean;
    maxConcurrent: number;
    maxRetained: number;
    supports: {
        list: boolean;
        get: boolean;
        stop: boolean;
        followUp: boolean;
        resume: false;
        notificationAck: boolean;
    };
}>;
export type TaskCapabilities = z.infer<typeof TaskCapabilitiesSchema>;
export declare const PublicTaskStateSchema: z.ZodEnum<["accepted", "queued", "running", "stopping", "completed", "failed", "cancelled", "unknown"]>;
export type PublicTaskState = z.infer<typeof PublicTaskStateSchema>;
export declare const PublicTaskProgressSchema: z.ZodEffects<z.ZodObject<{
    message: z.ZodString;
    stage: z.ZodOptional<z.ZodString>;
    current: z.ZodOptional<z.ZodNumber>;
    total: z.ZodOptional<z.ZodNumber>;
    percent: z.ZodOptional<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    message: string;
    stage?: string | undefined;
    current?: number | undefined;
    total?: number | undefined;
    percent?: number | undefined;
}, {
    message: string;
    stage?: string | undefined;
    current?: number | undefined;
    total?: number | undefined;
    percent?: number | undefined;
}>, {
    message: string;
    stage?: string | undefined;
    current?: number | undefined;
    total?: number | undefined;
    percent?: number | undefined;
}, {
    message: string;
    stage?: string | undefined;
    current?: number | undefined;
    total?: number | undefined;
    percent?: number | undefined;
}>;
export type PublicTaskProgress = z.infer<typeof PublicTaskProgressSchema>;
export declare const PublicTaskResultSchema: z.ZodEffects<z.ZodObject<{
    summary: z.ZodOptional<z.ZodString>;
    output: z.ZodOptional<z.ZodString>;
    truncated: z.ZodDefault<z.ZodBoolean>;
    usage: z.ZodOptional<z.ZodEffects<z.ZodRecord<z.ZodString, z.ZodUnknown>, Record<string, unknown>, Record<string, unknown>>>;
}, "strict", z.ZodTypeAny, {
    summary?: string | undefined;
    output?: string | undefined;
    truncated: boolean;
    usage?: Record<string, unknown> | undefined;
}, {
    summary?: string | undefined;
    output?: string | undefined;
    truncated?: boolean | undefined;
    usage?: Record<string, unknown> | undefined;
}>, {
    summary?: string | undefined;
    output?: string | undefined;
    truncated: boolean;
    usage?: Record<string, unknown> | undefined;
}, {
    summary?: string | undefined;
    output?: string | undefined;
    truncated?: boolean | undefined;
    usage?: Record<string, unknown> | undefined;
}>;
export type PublicTaskResult = z.infer<typeof PublicTaskResultSchema>;
export declare const PublicTaskErrorSchema: z.ZodObject<{
    code: z.ZodString;
    message: z.ZodString;
    recoverable: z.ZodDefault<z.ZodBoolean>;
}, "strict", z.ZodTypeAny, {
    code: string;
    message: string;
    recoverable: boolean;
}, {
    code: string;
    message: string;
    recoverable?: boolean | undefined;
}>;
export type PublicTaskError = z.infer<typeof PublicTaskErrorSchema>;
export declare const PublicTaskSnapshotSchema: z.ZodEffects<z.ZodObject<{
    taskId: z.ZodString;
    kind: z.ZodOptional<z.ZodEnum<["background", "follow_up"]>>;
    parentTaskId: z.ZodOptional<z.ZodString>;
    rootTaskId: z.ZodOptional<z.ZodString>;
    sequence: z.ZodEffects<z.ZodNumber, number, number>;
    state: z.ZodEnum<["accepted", "queued", "running", "stopping", "completed", "failed", "cancelled", "unknown"]>;
    title: z.ZodOptional<z.ZodString>;
    createdAt: z.ZodNumber;
    updatedAt: z.ZodNumber;
    startedAt: z.ZodOptional<z.ZodNumber>;
    finishedAt: z.ZodOptional<z.ZodNumber>;
    progress: z.ZodOptional<z.ZodEffects<z.ZodObject<{
        message: z.ZodString;
        stage: z.ZodOptional<z.ZodString>;
        current: z.ZodOptional<z.ZodNumber>;
        total: z.ZodOptional<z.ZodNumber>;
        percent: z.ZodOptional<z.ZodNumber>;
    }, "strict", z.ZodTypeAny, {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    }, {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    }>, {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    }, {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    }>>;
    result: z.ZodOptional<z.ZodEffects<z.ZodObject<{
        summary: z.ZodOptional<z.ZodString>;
        output: z.ZodOptional<z.ZodString>;
        truncated: z.ZodDefault<z.ZodBoolean>;
        usage: z.ZodOptional<z.ZodEffects<z.ZodRecord<z.ZodString, z.ZodUnknown>, Record<string, unknown>, Record<string, unknown>>>;
    }, "strict", z.ZodTypeAny, {
        summary?: string | undefined;
        output?: string | undefined;
        truncated: boolean;
        usage?: Record<string, unknown> | undefined;
    }, {
        summary?: string | undefined;
        output?: string | undefined;
        truncated?: boolean | undefined;
        usage?: Record<string, unknown> | undefined;
    }>, {
        summary?: string | undefined;
        output?: string | undefined;
        truncated: boolean;
        usage?: Record<string, unknown> | undefined;
    }, {
        summary?: string | undefined;
        output?: string | undefined;
        truncated?: boolean | undefined;
        usage?: Record<string, unknown> | undefined;
    }>>;
    error: z.ZodOptional<z.ZodObject<{
        code: z.ZodString;
        message: z.ZodString;
        recoverable: z.ZodDefault<z.ZodBoolean>;
    }, "strict", z.ZodTypeAny, {
        code: string;
        message: string;
        recoverable: boolean;
    }, {
        code: string;
        message: string;
        recoverable?: boolean | undefined;
    }>>;
}, "strict", z.ZodTypeAny, {
    taskId: string;
    kind?: "background" | "follow_up" | undefined;
    parentTaskId?: string | undefined;
    rootTaskId?: string | undefined;
    sequence: number;
    state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
    title?: string | undefined;
    createdAt: number;
    updatedAt: number;
    startedAt?: number | undefined;
    finishedAt?: number | undefined;
    progress?: {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    } | undefined;
    result?: {
        summary?: string | undefined;
        output?: string | undefined;
        truncated: boolean;
        usage?: Record<string, unknown> | undefined;
    } | undefined;
    error?: {
        code: string;
        message: string;
        recoverable: boolean;
    } | undefined;
}, {
    taskId: string;
    kind?: "background" | "follow_up" | undefined;
    parentTaskId?: string | undefined;
    rootTaskId?: string | undefined;
    sequence: number;
    state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
    title?: string | undefined;
    createdAt: number;
    updatedAt: number;
    startedAt?: number | undefined;
    finishedAt?: number | undefined;
    progress?: {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    } | undefined;
    result?: {
        summary?: string | undefined;
        output?: string | undefined;
        truncated?: boolean | undefined;
        usage?: Record<string, unknown> | undefined;
    } | undefined;
    error?: {
        code: string;
        message: string;
        recoverable?: boolean | undefined;
    } | undefined;
}>, {
    taskId: string;
    kind?: "background" | "follow_up" | undefined;
    parentTaskId?: string | undefined;
    rootTaskId?: string | undefined;
    sequence: number;
    state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
    title?: string | undefined;
    createdAt: number;
    updatedAt: number;
    startedAt?: number | undefined;
    finishedAt?: number | undefined;
    progress?: {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    } | undefined;
    result?: {
        summary?: string | undefined;
        output?: string | undefined;
        truncated: boolean;
        usage?: Record<string, unknown> | undefined;
    } | undefined;
    error?: {
        code: string;
        message: string;
        recoverable: boolean;
    } | undefined;
}, {
    taskId: string;
    kind?: "background" | "follow_up" | undefined;
    parentTaskId?: string | undefined;
    rootTaskId?: string | undefined;
    sequence: number;
    state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
    title?: string | undefined;
    createdAt: number;
    updatedAt: number;
    startedAt?: number | undefined;
    finishedAt?: number | undefined;
    progress?: {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    } | undefined;
    result?: {
        summary?: string | undefined;
        output?: string | undefined;
        truncated?: boolean | undefined;
        usage?: Record<string, unknown> | undefined;
    } | undefined;
    error?: {
        code: string;
        message: string;
        recoverable?: boolean | undefined;
    } | undefined;
}>;
export type PublicTaskSnapshot = z.infer<typeof PublicTaskSnapshotSchema>;
export declare const TaskNotificationSchema: z.ZodObject<{
    notificationId: z.ZodString;
    kind: z.ZodEnum<["completed", "failed", "cancelled", "unknown"]>;
    delivery: z.ZodEnum<["interrupt", "when_idle", "silent"]>;
    message: z.ZodString;
    createdAt: z.ZodNumber;
    acknowledged: z.ZodBoolean;
}, "strict", z.ZodTypeAny, {
    notificationId: string;
    kind: "cancelled" | "completed" | "failed" | "unknown";
    delivery: "interrupt" | "silent" | "when_idle";
    message: string;
    createdAt: number;
    acknowledged: boolean;
}, {
    notificationId: string;
    kind: "cancelled" | "completed" | "failed" | "unknown";
    delivery: "interrupt" | "silent" | "when_idle";
    message: string;
    createdAt: number;
    acknowledged: boolean;
}>;
export type TaskNotification = z.infer<typeof TaskNotificationSchema>;
export declare const PublicConversationSchema: z.ZodEffects<z.ZodObject<{
    mode: z.ZodEnum<["new", "resume", "unbound"]>;
    sessionId: z.ZodOptional<z.ZodString>;
    title: z.ZodOptional<z.ZodString>;
    source: z.ZodOptional<z.ZodString>;
    preview: z.ZodOptional<z.ZodString>;
    lastActiveAt: z.ZodOptional<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    mode: "new" | "resume" | "unbound";
    sessionId?: string | undefined;
    title?: string | undefined;
    source?: string | undefined;
    preview?: string | undefined;
    lastActiveAt?: number | undefined;
}, {
    mode: "new" | "resume" | "unbound";
    sessionId?: string | undefined;
    title?: string | undefined;
    source?: string | undefined;
    preview?: string | undefined;
    lastActiveAt?: number | undefined;
}>, {
    mode: "new" | "resume" | "unbound";
    sessionId?: string | undefined;
    title?: string | undefined;
    source?: string | undefined;
    preview?: string | undefined;
    lastActiveAt?: number | undefined;
}, {
    mode: "new" | "resume" | "unbound";
    sessionId?: string | undefined;
    title?: string | undefined;
    source?: string | undefined;
    preview?: string | undefined;
    lastActiveAt?: number | undefined;
}>;
export type PublicConversation = z.infer<typeof PublicConversationSchema>;
export declare const ServerMessageSchema: z.ZodUnion<[z.ZodObject<{
    type: z.ZodLiteral<"session.ready">;
    protocolVersion: z.ZodUnion<[z.ZodLiteral<3>, z.ZodLiteral<4>, z.ZodLiteral<5>, z.ZodLiteral<6>]>;
    requestId: z.ZodOptional<z.ZodString>;
    sessionId: z.ZodString;
    model: z.ZodString;
    hermes: z.ZodObject<{
        model: z.ZodOptional<z.ZodString>;
        capabilities: z.ZodOptional<z.ZodEffects<z.ZodRecord<z.ZodString, z.ZodUnknown>, Record<string, unknown>, Record<string, unknown>>>;
    }, "strict", z.ZodTypeAny, {
        model?: string | undefined;
        capabilities?: Record<string, unknown> | undefined;
    }, {
        model?: string | undefined;
        capabilities?: Record<string, unknown> | undefined;
    }>;
    realtime: z.ZodObject<{
        provider: z.ZodEnum<["local", "gemini", "openai", "mock"]>;
        model: z.ZodString;
        audio: z.ZodObject<{
            input: z.ZodObject<{
                enabled: z.ZodBoolean;
                mimeType: z.ZodOptional<z.ZodString>;
                recommendedFrameMs: z.ZodOptional<z.ZodNumber>;
            }, "strict", z.ZodTypeAny, {
                enabled: boolean;
                mimeType?: string | undefined;
                recommendedFrameMs?: number | undefined;
            }, {
                enabled: boolean;
                mimeType?: string | undefined;
                recommendedFrameMs?: number | undefined;
            }>;
            output: z.ZodObject<{
                enabled: z.ZodBoolean;
                mimeType: z.ZodOptional<z.ZodString>;
            }, "strict", z.ZodTypeAny, {
                enabled: boolean;
                mimeType?: string | undefined;
            }, {
                enabled: boolean;
                mimeType?: string | undefined;
            }>;
            turnDetection: z.ZodEnum<["disabled", "semantic_vad", "server_vad", "provider", "none"]>;
        }, "strict", z.ZodTypeAny, {
            input: {
                enabled: boolean;
                mimeType?: string | undefined;
                recommendedFrameMs?: number | undefined;
            };
            output: {
                enabled: boolean;
                mimeType?: string | undefined;
            };
            turnDetection: "disabled" | "none" | "provider" | "semantic_vad" | "server_vad";
        }, {
            input: {
                enabled: boolean;
                mimeType?: string | undefined;
                recommendedFrameMs?: number | undefined;
            };
            output: {
                enabled: boolean;
                mimeType?: string | undefined;
            };
            turnDetection: "disabled" | "none" | "provider" | "semantic_vad" | "server_vad";
        }>;
    }, "strict", z.ZodTypeAny, {
        provider: "gemini" | "local" | "mock" | "openai";
        model: string;
        audio: {
            input: {
                enabled: boolean;
                mimeType?: string | undefined;
                recommendedFrameMs?: number | undefined;
            };
            output: {
                enabled: boolean;
                mimeType?: string | undefined;
            };
            turnDetection: "disabled" | "none" | "provider" | "semantic_vad" | "server_vad";
        };
    }, {
        provider: "gemini" | "local" | "mock" | "openai";
        model: string;
        audio: {
            input: {
                enabled: boolean;
                mimeType?: string | undefined;
                recommendedFrameMs?: number | undefined;
            };
            output: {
                enabled: boolean;
                mimeType?: string | undefined;
            };
            turnDetection: "disabled" | "none" | "provider" | "semantic_vad" | "server_vad";
        };
    }>;
    tasks: z.ZodObject<{
        scope: z.ZodLiteral<"owner">;
        sequence: z.ZodLiteral<"per_task">;
        reconnect: z.ZodLiteral<"snapshot">;
        durable: z.ZodBoolean;
        parallel: z.ZodBoolean;
        maxConcurrent: z.ZodNumber;
        maxRetained: z.ZodNumber;
        supports: z.ZodObject<{
            list: z.ZodBoolean;
            get: z.ZodBoolean;
            stop: z.ZodBoolean;
            followUp: z.ZodBoolean;
            resume: z.ZodLiteral<false>;
            notificationAck: z.ZodBoolean;
        }, "strict", z.ZodTypeAny, {
            list: boolean;
            get: boolean;
            stop: boolean;
            followUp: boolean;
            resume: false;
            notificationAck: boolean;
        }, {
            list: boolean;
            get: boolean;
            stop: boolean;
            followUp: boolean;
            resume: false;
            notificationAck: boolean;
        }>;
    }, "strict", z.ZodTypeAny, {
        scope: "owner";
        sequence: "per_task";
        reconnect: "snapshot";
        durable: boolean;
        parallel: boolean;
        maxConcurrent: number;
        maxRetained: number;
        supports: {
            list: boolean;
            get: boolean;
            stop: boolean;
            followUp: boolean;
            resume: false;
            notificationAck: boolean;
        };
    }, {
        scope: "owner";
        sequence: "per_task";
        reconnect: "snapshot";
        durable: boolean;
        parallel: boolean;
        maxConcurrent: number;
        maxRetained: number;
        supports: {
            list: boolean;
            get: boolean;
            stop: boolean;
            followUp: boolean;
            resume: false;
            notificationAck: boolean;
        };
    }>;
    conversation: z.ZodOptional<z.ZodEffects<z.ZodObject<{
        mode: z.ZodEnum<["new", "resume", "unbound"]>;
        sessionId: z.ZodOptional<z.ZodString>;
        title: z.ZodOptional<z.ZodString>;
        source: z.ZodOptional<z.ZodString>;
        preview: z.ZodOptional<z.ZodString>;
        lastActiveAt: z.ZodOptional<z.ZodNumber>;
    }, "strict", z.ZodTypeAny, {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
        source?: string | undefined;
        preview?: string | undefined;
        lastActiveAt?: number | undefined;
    }, {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
        source?: string | undefined;
        preview?: string | undefined;
        lastActiveAt?: number | undefined;
    }>, {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
        source?: string | undefined;
        preview?: string | undefined;
        lastActiveAt?: number | undefined;
    }, {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
        source?: string | undefined;
        preview?: string | undefined;
        lastActiveAt?: number | undefined;
    }>>;
}, "strict", z.ZodTypeAny, {
    type: "session.ready";
    protocolVersion: 3 | 4 | 5 | 6;
    requestId?: string | undefined;
    sessionId: string;
    model: string;
    hermes: {
        model?: string | undefined;
        capabilities?: Record<string, unknown> | undefined;
    };
    realtime: {
        provider: "gemini" | "local" | "mock" | "openai";
        model: string;
        audio: {
            input: {
                enabled: boolean;
                mimeType?: string | undefined;
                recommendedFrameMs?: number | undefined;
            };
            output: {
                enabled: boolean;
                mimeType?: string | undefined;
            };
            turnDetection: "disabled" | "none" | "provider" | "semantic_vad" | "server_vad";
        };
    };
    tasks: {
        scope: "owner";
        sequence: "per_task";
        reconnect: "snapshot";
        durable: boolean;
        parallel: boolean;
        maxConcurrent: number;
        maxRetained: number;
        supports: {
            list: boolean;
            get: boolean;
            stop: boolean;
            followUp: boolean;
            resume: false;
            notificationAck: boolean;
        };
    };
    conversation?: {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
        source?: string | undefined;
        preview?: string | undefined;
        lastActiveAt?: number | undefined;
    } | undefined;
}, {
    type: "session.ready";
    protocolVersion: 3 | 4 | 5 | 6;
    requestId?: string | undefined;
    sessionId: string;
    model: string;
    hermes: {
        model?: string | undefined;
        capabilities?: Record<string, unknown> | undefined;
    };
    realtime: {
        provider: "gemini" | "local" | "mock" | "openai";
        model: string;
        audio: {
            input: {
                enabled: boolean;
                mimeType?: string | undefined;
                recommendedFrameMs?: number | undefined;
            };
            output: {
                enabled: boolean;
                mimeType?: string | undefined;
            };
            turnDetection: "disabled" | "none" | "provider" | "semantic_vad" | "server_vad";
        };
    };
    tasks: {
        scope: "owner";
        sequence: "per_task";
        reconnect: "snapshot";
        durable: boolean;
        parallel: boolean;
        maxConcurrent: number;
        maxRetained: number;
        supports: {
            list: boolean;
            get: boolean;
            stop: boolean;
            followUp: boolean;
            resume: false;
            notificationAck: boolean;
        };
    };
    conversation?: {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
        source?: string | undefined;
        preview?: string | undefined;
        lastActiveAt?: number | undefined;
    } | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"session.error">;
    code: z.ZodString;
    message: z.ZodString;
    requestId: z.ZodOptional<z.ZodString>;
    recoverable: z.ZodDefault<z.ZodBoolean>;
}, "strict", z.ZodTypeAny, {
    type: "session.error";
    code: string;
    message: string;
    requestId?: string | undefined;
    recoverable: boolean;
}, {
    type: "session.error";
    code: string;
    message: string;
    requestId?: string | undefined;
    recoverable?: boolean | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"audio.output">;
    data: z.ZodString;
    mimeType: z.ZodString;
    itemId: z.ZodOptional<z.ZodString>;
    contentIndex: z.ZodOptional<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    type: "audio.output";
    data: string;
    mimeType: string;
    itemId?: string | undefined;
    contentIndex?: number | undefined;
}, {
    type: "audio.output";
    data: string;
    mimeType: string;
    itemId?: string | undefined;
    contentIndex?: number | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"transcript.delta">;
    speaker: z.ZodEnum<["user", "assistant", "system"]>;
    text: z.ZodString;
    final: z.ZodOptional<z.ZodBoolean>;
}, "strict", z.ZodTypeAny, {
    type: "transcript.delta";
    speaker: "assistant" | "system" | "user";
    text: string;
    final?: boolean | undefined;
}, {
    type: "transcript.delta";
    speaker: "assistant" | "system" | "user";
    text: string;
    final?: boolean | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"input.speech_started">;
    provider: z.ZodEnum<["openai", "local"]>;
    itemId: z.ZodOptional<z.ZodString>;
    audioStartMs: z.ZodOptional<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    type: "input.speech_started";
    provider: "local" | "openai";
    itemId?: string | undefined;
    audioStartMs?: number | undefined;
}, {
    type: "input.speech_started";
    provider: "local" | "openai";
    itemId?: string | undefined;
    audioStartMs?: number | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"input.pause_requested">;
    reason: z.ZodLiteral<"voice_command">;
}, "strict", z.ZodTypeAny, {
    type: "input.pause_requested";
    reason: "voice_command";
}, {
    type: "input.pause_requested";
    reason: "voice_command";
}>, z.ZodObject<{
    type: z.ZodLiteral<"response.started">;
    responseId: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    type: "response.started";
    responseId?: string | undefined;
}, {
    type: "response.started";
    responseId?: string | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"response.completed">;
    responseId: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    type: "response.completed";
    responseId?: string | undefined;
}, {
    type: "response.completed";
    responseId?: string | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"response.cancelled">;
    responseId: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    type: "response.cancelled";
    responseId?: string | undefined;
}, {
    type: "response.cancelled";
    responseId?: string | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"response.failed">;
    responseId: z.ZodOptional<z.ZodString>;
    error: z.ZodString;
}, "strict", z.ZodTypeAny, {
    type: "response.failed";
    responseId?: string | undefined;
    error: string;
}, {
    type: "response.failed";
    responseId?: string | undefined;
    error: string;
}>, z.ZodEffects<z.ZodObject<{
    type: z.ZodLiteral<"task.snapshot">;
    reason: z.ZodEnum<["initial", "reconnect", "list", "get"]>;
    requestId: z.ZodOptional<z.ZodString>;
    tasks: z.ZodArray<z.ZodEffects<z.ZodObject<{
        taskId: z.ZodString;
        kind: z.ZodOptional<z.ZodEnum<["background", "follow_up"]>>;
        parentTaskId: z.ZodOptional<z.ZodString>;
        rootTaskId: z.ZodOptional<z.ZodString>;
        sequence: z.ZodEffects<z.ZodNumber, number, number>;
        state: z.ZodEnum<["accepted", "queued", "running", "stopping", "completed", "failed", "cancelled", "unknown"]>;
        title: z.ZodOptional<z.ZodString>;
        createdAt: z.ZodNumber;
        updatedAt: z.ZodNumber;
        startedAt: z.ZodOptional<z.ZodNumber>;
        finishedAt: z.ZodOptional<z.ZodNumber>;
        progress: z.ZodOptional<z.ZodEffects<z.ZodObject<{
            message: z.ZodString;
            stage: z.ZodOptional<z.ZodString>;
            current: z.ZodOptional<z.ZodNumber>;
            total: z.ZodOptional<z.ZodNumber>;
            percent: z.ZodOptional<z.ZodNumber>;
        }, "strict", z.ZodTypeAny, {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        }, {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        }>, {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        }, {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        }>>;
        result: z.ZodOptional<z.ZodEffects<z.ZodObject<{
            summary: z.ZodOptional<z.ZodString>;
            output: z.ZodOptional<z.ZodString>;
            truncated: z.ZodDefault<z.ZodBoolean>;
            usage: z.ZodOptional<z.ZodEffects<z.ZodRecord<z.ZodString, z.ZodUnknown>, Record<string, unknown>, Record<string, unknown>>>;
        }, "strict", z.ZodTypeAny, {
            summary?: string | undefined;
            output?: string | undefined;
            truncated: boolean;
            usage?: Record<string, unknown> | undefined;
        }, {
            summary?: string | undefined;
            output?: string | undefined;
            truncated?: boolean | undefined;
            usage?: Record<string, unknown> | undefined;
        }>, {
            summary?: string | undefined;
            output?: string | undefined;
            truncated: boolean;
            usage?: Record<string, unknown> | undefined;
        }, {
            summary?: string | undefined;
            output?: string | undefined;
            truncated?: boolean | undefined;
            usage?: Record<string, unknown> | undefined;
        }>>;
        error: z.ZodOptional<z.ZodObject<{
            code: z.ZodString;
            message: z.ZodString;
            recoverable: z.ZodDefault<z.ZodBoolean>;
        }, "strict", z.ZodTypeAny, {
            code: string;
            message: string;
            recoverable: boolean;
        }, {
            code: string;
            message: string;
            recoverable?: boolean | undefined;
        }>>;
    }, "strict", z.ZodTypeAny, {
        taskId: string;
        kind?: "background" | "follow_up" | undefined;
        parentTaskId?: string | undefined;
        rootTaskId?: string | undefined;
        sequence: number;
        state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
        title?: string | undefined;
        createdAt: number;
        updatedAt: number;
        startedAt?: number | undefined;
        finishedAt?: number | undefined;
        progress?: {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        } | undefined;
        result?: {
            summary?: string | undefined;
            output?: string | undefined;
            truncated: boolean;
            usage?: Record<string, unknown> | undefined;
        } | undefined;
        error?: {
            code: string;
            message: string;
            recoverable: boolean;
        } | undefined;
    }, {
        taskId: string;
        kind?: "background" | "follow_up" | undefined;
        parentTaskId?: string | undefined;
        rootTaskId?: string | undefined;
        sequence: number;
        state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
        title?: string | undefined;
        createdAt: number;
        updatedAt: number;
        startedAt?: number | undefined;
        finishedAt?: number | undefined;
        progress?: {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        } | undefined;
        result?: {
            summary?: string | undefined;
            output?: string | undefined;
            truncated?: boolean | undefined;
            usage?: Record<string, unknown> | undefined;
        } | undefined;
        error?: {
            code: string;
            message: string;
            recoverable?: boolean | undefined;
        } | undefined;
    }>, {
        taskId: string;
        kind?: "background" | "follow_up" | undefined;
        parentTaskId?: string | undefined;
        rootTaskId?: string | undefined;
        sequence: number;
        state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
        title?: string | undefined;
        createdAt: number;
        updatedAt: number;
        startedAt?: number | undefined;
        finishedAt?: number | undefined;
        progress?: {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        } | undefined;
        result?: {
            summary?: string | undefined;
            output?: string | undefined;
            truncated: boolean;
            usage?: Record<string, unknown> | undefined;
        } | undefined;
        error?: {
            code: string;
            message: string;
            recoverable: boolean;
        } | undefined;
    }, {
        taskId: string;
        kind?: "background" | "follow_up" | undefined;
        parentTaskId?: string | undefined;
        rootTaskId?: string | undefined;
        sequence: number;
        state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
        title?: string | undefined;
        createdAt: number;
        updatedAt: number;
        startedAt?: number | undefined;
        finishedAt?: number | undefined;
        progress?: {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        } | undefined;
        result?: {
            summary?: string | undefined;
            output?: string | undefined;
            truncated?: boolean | undefined;
            usage?: Record<string, unknown> | undefined;
        } | undefined;
        error?: {
            code: string;
            message: string;
            recoverable?: boolean | undefined;
        } | undefined;
    }>, "many">;
    truncated: z.ZodDefault<z.ZodBoolean>;
}, "strict", z.ZodTypeAny, {
    type: "task.snapshot";
    reason: "get" | "initial" | "list" | "reconnect";
    requestId?: string | undefined;
    tasks: {
        taskId: string;
        kind?: "background" | "follow_up" | undefined;
        parentTaskId?: string | undefined;
        rootTaskId?: string | undefined;
        sequence: number;
        state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
        title?: string | undefined;
        createdAt: number;
        updatedAt: number;
        startedAt?: number | undefined;
        finishedAt?: number | undefined;
        progress?: {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        } | undefined;
        result?: {
            summary?: string | undefined;
            output?: string | undefined;
            truncated: boolean;
            usage?: Record<string, unknown> | undefined;
        } | undefined;
        error?: {
            code: string;
            message: string;
            recoverable: boolean;
        } | undefined;
    }[];
    truncated: boolean;
}, {
    type: "task.snapshot";
    reason: "get" | "initial" | "list" | "reconnect";
    requestId?: string | undefined;
    tasks: {
        taskId: string;
        kind?: "background" | "follow_up" | undefined;
        parentTaskId?: string | undefined;
        rootTaskId?: string | undefined;
        sequence: number;
        state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
        title?: string | undefined;
        createdAt: number;
        updatedAt: number;
        startedAt?: number | undefined;
        finishedAt?: number | undefined;
        progress?: {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        } | undefined;
        result?: {
            summary?: string | undefined;
            output?: string | undefined;
            truncated?: boolean | undefined;
            usage?: Record<string, unknown> | undefined;
        } | undefined;
        error?: {
            code: string;
            message: string;
            recoverable?: boolean | undefined;
        } | undefined;
    }[];
    truncated?: boolean | undefined;
}>, {
    type: "task.snapshot";
    reason: "get" | "initial" | "list" | "reconnect";
    requestId?: string | undefined;
    tasks: {
        taskId: string;
        kind?: "background" | "follow_up" | undefined;
        parentTaskId?: string | undefined;
        rootTaskId?: string | undefined;
        sequence: number;
        state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
        title?: string | undefined;
        createdAt: number;
        updatedAt: number;
        startedAt?: number | undefined;
        finishedAt?: number | undefined;
        progress?: {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        } | undefined;
        result?: {
            summary?: string | undefined;
            output?: string | undefined;
            truncated: boolean;
            usage?: Record<string, unknown> | undefined;
        } | undefined;
        error?: {
            code: string;
            message: string;
            recoverable: boolean;
        } | undefined;
    }[];
    truncated: boolean;
}, {
    type: "task.snapshot";
    reason: "get" | "initial" | "list" | "reconnect";
    requestId?: string | undefined;
    tasks: {
        taskId: string;
        kind?: "background" | "follow_up" | undefined;
        parentTaskId?: string | undefined;
        rootTaskId?: string | undefined;
        sequence: number;
        state: "accepted" | "cancelled" | "completed" | "failed" | "queued" | "running" | "stopping" | "unknown";
        title?: string | undefined;
        createdAt: number;
        updatedAt: number;
        startedAt?: number | undefined;
        finishedAt?: number | undefined;
        progress?: {
            message: string;
            stage?: string | undefined;
            current?: number | undefined;
            total?: number | undefined;
            percent?: number | undefined;
        } | undefined;
        result?: {
            summary?: string | undefined;
            output?: string | undefined;
            truncated?: boolean | undefined;
            usage?: Record<string, unknown> | undefined;
        } | undefined;
        error?: {
            code: string;
            message: string;
            recoverable?: boolean | undefined;
        } | undefined;
    }[];
    truncated?: boolean | undefined;
}>, z.ZodObject<{
    sequence: z.ZodEffects<z.ZodNumber, number, number>;
    taskId: z.ZodString;
    occurredAt: z.ZodNumber;
    type: z.ZodLiteral<"task.accepted">;
    requestId: z.ZodOptional<z.ZodString>;
    state: z.ZodEnum<["accepted", "queued"]>;
    title: z.ZodOptional<z.ZodString>;
    kind: z.ZodOptional<z.ZodEnum<["background", "follow_up"]>>;
    parentTaskId: z.ZodOptional<z.ZodString>;
    rootTaskId: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.accepted";
    requestId?: string | undefined;
    state: "accepted" | "queued";
    title?: string | undefined;
    kind?: "background" | "follow_up" | undefined;
    parentTaskId?: string | undefined;
    rootTaskId?: string | undefined;
}, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.accepted";
    requestId?: string | undefined;
    state: "accepted" | "queued";
    title?: string | undefined;
    kind?: "background" | "follow_up" | undefined;
    parentTaskId?: string | undefined;
    rootTaskId?: string | undefined;
}>, z.ZodObject<{
    sequence: z.ZodEffects<z.ZodNumber, number, number>;
    taskId: z.ZodString;
    occurredAt: z.ZodNumber;
    type: z.ZodLiteral<"task.started">;
    title: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.started";
    title?: string | undefined;
}, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.started";
    title?: string | undefined;
}>, z.ZodObject<{
    sequence: z.ZodEffects<z.ZodNumber, number, number>;
    taskId: z.ZodString;
    occurredAt: z.ZodNumber;
    type: z.ZodLiteral<"task.progress">;
    progress: z.ZodEffects<z.ZodObject<{
        message: z.ZodString;
        stage: z.ZodOptional<z.ZodString>;
        current: z.ZodOptional<z.ZodNumber>;
        total: z.ZodOptional<z.ZodNumber>;
        percent: z.ZodOptional<z.ZodNumber>;
    }, "strict", z.ZodTypeAny, {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    }, {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    }>, {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    }, {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    }>;
}, "strict", z.ZodTypeAny, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.progress";
    progress: {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    };
}, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.progress";
    progress: {
        message: string;
        stage?: string | undefined;
        current?: number | undefined;
        total?: number | undefined;
        percent?: number | undefined;
    };
}>, z.ZodObject<{
    sequence: z.ZodEffects<z.ZodNumber, number, number>;
    taskId: z.ZodString;
    occurredAt: z.ZodNumber;
    type: z.ZodLiteral<"task.stopping">;
    requestId: z.ZodOptional<z.ZodString>;
    reason: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.stopping";
    requestId?: string | undefined;
    reason?: string | undefined;
}, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.stopping";
    requestId?: string | undefined;
    reason?: string | undefined;
}>, z.ZodObject<{
    sequence: z.ZodEffects<z.ZodNumber, number, number>;
    taskId: z.ZodString;
    occurredAt: z.ZodNumber;
    type: z.ZodLiteral<"task.completed">;
    requestId: z.ZodOptional<z.ZodString>;
    result: z.ZodEffects<z.ZodObject<{
        summary: z.ZodOptional<z.ZodString>;
        output: z.ZodOptional<z.ZodString>;
        truncated: z.ZodDefault<z.ZodBoolean>;
        usage: z.ZodOptional<z.ZodEffects<z.ZodRecord<z.ZodString, z.ZodUnknown>, Record<string, unknown>, Record<string, unknown>>>;
    }, "strict", z.ZodTypeAny, {
        summary?: string | undefined;
        output?: string | undefined;
        truncated: boolean;
        usage?: Record<string, unknown> | undefined;
    }, {
        summary?: string | undefined;
        output?: string | undefined;
        truncated?: boolean | undefined;
        usage?: Record<string, unknown> | undefined;
    }>, {
        summary?: string | undefined;
        output?: string | undefined;
        truncated: boolean;
        usage?: Record<string, unknown> | undefined;
    }, {
        summary?: string | undefined;
        output?: string | undefined;
        truncated?: boolean | undefined;
        usage?: Record<string, unknown> | undefined;
    }>;
}, "strict", z.ZodTypeAny, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.completed";
    requestId?: string | undefined;
    result: {
        summary?: string | undefined;
        output?: string | undefined;
        truncated: boolean;
        usage?: Record<string, unknown> | undefined;
    };
}, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.completed";
    requestId?: string | undefined;
    result: {
        summary?: string | undefined;
        output?: string | undefined;
        truncated?: boolean | undefined;
        usage?: Record<string, unknown> | undefined;
    };
}>, z.ZodObject<{
    sequence: z.ZodEffects<z.ZodNumber, number, number>;
    taskId: z.ZodString;
    occurredAt: z.ZodNumber;
    type: z.ZodLiteral<"task.failed">;
    requestId: z.ZodOptional<z.ZodString>;
    error: z.ZodObject<{
        code: z.ZodString;
        message: z.ZodString;
        recoverable: z.ZodDefault<z.ZodBoolean>;
    }, "strict", z.ZodTypeAny, {
        code: string;
        message: string;
        recoverable: boolean;
    }, {
        code: string;
        message: string;
        recoverable?: boolean | undefined;
    }>;
}, "strict", z.ZodTypeAny, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.failed";
    requestId?: string | undefined;
    error: {
        code: string;
        message: string;
        recoverable: boolean;
    };
}, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.failed";
    requestId?: string | undefined;
    error: {
        code: string;
        message: string;
        recoverable?: boolean | undefined;
    };
}>, z.ZodObject<{
    sequence: z.ZodEffects<z.ZodNumber, number, number>;
    taskId: z.ZodString;
    occurredAt: z.ZodNumber;
    type: z.ZodLiteral<"task.cancelled">;
    requestId: z.ZodOptional<z.ZodString>;
    reason: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.cancelled";
    requestId?: string | undefined;
    reason?: string | undefined;
}, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.cancelled";
    requestId?: string | undefined;
    reason?: string | undefined;
}>, z.ZodObject<{
    sequence: z.ZodEffects<z.ZodNumber, number, number>;
    taskId: z.ZodString;
    occurredAt: z.ZodNumber;
    type: z.ZodLiteral<"task.unknown">;
    requestId: z.ZodOptional<z.ZodString>;
    error: z.ZodObject<{
        code: z.ZodString;
        message: z.ZodString;
        recoverable: z.ZodDefault<z.ZodBoolean>;
    }, "strict", z.ZodTypeAny, {
        code: string;
        message: string;
        recoverable: boolean;
    }, {
        code: string;
        message: string;
        recoverable?: boolean | undefined;
    }>;
}, "strict", z.ZodTypeAny, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.unknown";
    requestId?: string | undefined;
    error: {
        code: string;
        message: string;
        recoverable: boolean;
    };
}, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.unknown";
    requestId?: string | undefined;
    error: {
        code: string;
        message: string;
        recoverable?: boolean | undefined;
    };
}>, z.ZodObject<{
    sequence: z.ZodEffects<z.ZodNumber, number, number>;
    taskId: z.ZodString;
    occurredAt: z.ZodNumber;
    type: z.ZodLiteral<"task.notification">;
    requestId: z.ZodOptional<z.ZodString>;
    notification: z.ZodObject<{
        notificationId: z.ZodString;
        kind: z.ZodEnum<["completed", "failed", "cancelled", "unknown"]>;
        delivery: z.ZodEnum<["interrupt", "when_idle", "silent"]>;
        message: z.ZodString;
        createdAt: z.ZodNumber;
        acknowledged: z.ZodBoolean;
    }, "strict", z.ZodTypeAny, {
        notificationId: string;
        kind: "cancelled" | "completed" | "failed" | "unknown";
        delivery: "interrupt" | "silent" | "when_idle";
        message: string;
        createdAt: number;
        acknowledged: boolean;
    }, {
        notificationId: string;
        kind: "cancelled" | "completed" | "failed" | "unknown";
        delivery: "interrupt" | "silent" | "when_idle";
        message: string;
        createdAt: number;
        acknowledged: boolean;
    }>;
}, "strict", z.ZodTypeAny, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.notification";
    requestId?: string | undefined;
    notification: {
        notificationId: string;
        kind: "cancelled" | "completed" | "failed" | "unknown";
        delivery: "interrupt" | "silent" | "when_idle";
        message: string;
        createdAt: number;
        acknowledged: boolean;
    };
}, {
    sequence: number;
    taskId: string;
    occurredAt: number;
    type: "task.notification";
    requestId?: string | undefined;
    notification: {
        notificationId: string;
        kind: "cancelled" | "completed" | "failed" | "unknown";
        delivery: "interrupt" | "silent" | "when_idle";
        message: string;
        createdAt: number;
        acknowledged: boolean;
    };
}>, z.ZodObject<{
    type: z.ZodLiteral<"log">;
    level: z.ZodEnum<["debug", "info", "warn", "error"]>;
    message: z.ZodString;
    data: z.ZodOptional<z.ZodEffects<z.ZodRecord<z.ZodString, z.ZodUnknown>, Record<string, unknown>, Record<string, unknown>>>;
}, "strict", z.ZodTypeAny, {
    type: "log";
    level: "debug" | "error" | "info" | "warn";
    message: string;
    data?: Record<string, unknown> | undefined;
}, {
    type: "log";
    level: "debug" | "error" | "info" | "warn";
    message: string;
    data?: Record<string, unknown> | undefined;
}>]>;
export type ServerMessage = z.infer<typeof ServerMessageSchema>;
export type SessionReadyMessage = Extract<ServerMessage, {
    type: "session.ready";
}>;
export type TaskSnapshotMessage = Extract<ServerMessage, {
    type: "task.snapshot";
}>;
export type TaskLifecycleMessage = Extract<ServerMessage, {
    type: `task.${string}`;
}>;
export interface HermesRunEvent {
    event?: string;
    run_id?: string;
    timestamp?: number;
    delta?: string;
    output?: string;
    error?: string | boolean;
    usage?: Record<string, unknown>;
    [key: string]: unknown;
}
export declare function parseServerMessage(value: unknown): ServerMessage;
export declare function serverMessage(value: ServerMessage): string;
//# sourceMappingURL=server-protocol.d.ts.map