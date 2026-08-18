import { z } from "zod";
export declare const TASK_ID_MAX_CHARS = 256;
export declare const NOTIFICATION_ID_MAX_CHARS = 256;
export declare const TASK_LIST_DEFAULT_LIMIT = 50;
export declare const TASK_LIST_MAX_LIMIT = 100;
export declare const MAX_TASK_SEQUENCE: number;
export declare const RequestIdSchema: z.ZodString;
export declare const TaskIdSchema: z.ZodString;
export declare const NotificationIdSchema: z.ZodString;
export declare const ConversationIdSchema: z.ZodString;
export declare const TaskSequenceSchema: z.ZodNumber;
export declare const ApprovalChoiceSchema: z.ZodEnum<["once", "session", "always", "deny"]>;
export type ApprovalChoice = z.infer<typeof ApprovalChoiceSchema>;
export declare const RealtimeResponseTruncationSchema: z.ZodObject<{
    itemId: z.ZodString;
    contentIndex: z.ZodDefault<z.ZodNumber>;
    audioEndMs: z.ZodNumber;
}, "strict", z.ZodTypeAny, {
    itemId: string;
    contentIndex: number;
    audioEndMs: number;
}, {
    itemId: string;
    contentIndex?: number | undefined;
    audioEndMs: number;
}>;
export type RealtimeResponseTruncation = z.infer<typeof RealtimeResponseTruncationSchema>;
export declare const ConversationSelectionSchema: z.ZodEffects<z.ZodObject<{
    mode: z.ZodEnum<["new", "resume", "unbound"]>;
    sessionId: z.ZodOptional<z.ZodString>;
    title: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    mode: "new" | "resume" | "unbound";
    sessionId?: string | undefined;
    title?: string | undefined;
}, {
    mode: "new" | "resume" | "unbound";
    sessionId?: string | undefined;
    title?: string | undefined;
}>, {
    mode: "new" | "resume" | "unbound";
    sessionId?: string | undefined;
    title?: string | undefined;
}, {
    mode: "new" | "resume" | "unbound";
    sessionId?: string | undefined;
    title?: string | undefined;
}>;
export type ConversationSelection = z.infer<typeof ConversationSelectionSchema>;
export declare const ClientMessageSchema: z.ZodEffects<z.ZodDiscriminatedUnion<"type", [z.ZodObject<{
    type: z.ZodLiteral<"session.start">;
    id: z.ZodOptional<z.ZodString>;
    protocolVersion: z.ZodNumber;
    profileId: z.ZodOptional<z.ZodString>;
    userLabel: z.ZodOptional<z.ZodString>;
    conversation: z.ZodOptional<z.ZodEffects<z.ZodObject<{
        mode: z.ZodEnum<["new", "resume", "unbound"]>;
        sessionId: z.ZodOptional<z.ZodString>;
        title: z.ZodOptional<z.ZodString>;
    }, "strict", z.ZodTypeAny, {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
    }, {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
    }>, {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
    }, {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
    }>>;
}, "strict", z.ZodTypeAny, {
    type: "session.start";
    id?: string | undefined;
    protocolVersion: number;
    profileId?: string | undefined;
    userLabel?: string | undefined;
    conversation?: {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
    } | undefined;
}, {
    type: "session.start";
    id?: string | undefined;
    protocolVersion: number;
    profileId?: string | undefined;
    userLabel?: string | undefined;
    conversation?: {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
    } | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"audio.input">;
    id: z.ZodOptional<z.ZodString>;
    data: z.ZodString;
    mimeType: z.ZodDefault<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    type: "audio.input";
    id?: string | undefined;
    data: string;
    mimeType: string;
}, {
    type: "audio.input";
    id?: string | undefined;
    data: string;
    mimeType?: string | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"audio.end">;
    id: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    type: "audio.end";
    id?: string | undefined;
}, {
    type: "audio.end";
    id?: string | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"text.input">;
    id: z.ZodOptional<z.ZodString>;
    text: z.ZodString;
}, "strict", z.ZodTypeAny, {
    type: "text.input";
    id?: string | undefined;
    text: string;
}, {
    type: "text.input";
    id?: string | undefined;
    text: string;
}>, z.ZodObject<{
    type: z.ZodLiteral<"response.cancel">;
    id: z.ZodOptional<z.ZodString>;
    reason: z.ZodOptional<z.ZodString>;
    truncate: z.ZodOptional<z.ZodObject<{
        itemId: z.ZodString;
        contentIndex: z.ZodDefault<z.ZodNumber>;
        audioEndMs: z.ZodNumber;
    }, "strict", z.ZodTypeAny, {
        itemId: string;
        contentIndex: number;
        audioEndMs: number;
    }, {
        itemId: string;
        contentIndex?: number | undefined;
        audioEndMs: number;
    }>>;
}, "strict", z.ZodTypeAny, {
    type: "response.cancel";
    id?: string | undefined;
    reason?: string | undefined;
    truncate?: {
        itemId: string;
        contentIndex: number;
        audioEndMs: number;
    } | undefined;
}, {
    type: "response.cancel";
    id?: string | undefined;
    reason?: string | undefined;
    truncate?: {
        itemId: string;
        contentIndex?: number | undefined;
        audioEndMs: number;
    } | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"task.list">;
    id: z.ZodString;
    limit: z.ZodDefault<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    type: "task.list";
    id: string;
    limit: number;
}, {
    type: "task.list";
    id: string;
    limit?: number | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"task.get">;
    id: z.ZodString;
    taskId: z.ZodString;
}, "strict", z.ZodTypeAny, {
    type: "task.get";
    id: string;
    taskId: string;
}, {
    type: "task.get";
    id: string;
    taskId: string;
}>, z.ZodObject<{
    type: z.ZodLiteral<"task.follow_up">;
    id: z.ZodString;
    taskId: z.ZodString;
    message: z.ZodString;
    title: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    type: "task.follow_up";
    id: string;
    taskId: string;
    message: string;
    title?: string | undefined;
}, {
    type: "task.follow_up";
    id: string;
    taskId: string;
    message: string;
    title?: string | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"task.stop">;
    id: z.ZodString;
    taskId: z.ZodString;
    reason: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    type: "task.stop";
    id: string;
    taskId: string;
    reason?: string | undefined;
}, {
    type: "task.stop";
    id: string;
    taskId: string;
    reason?: string | undefined;
}>, z.ZodObject<{
    type: z.ZodLiteral<"task.notification.ack">;
    id: z.ZodString;
    taskId: z.ZodString;
    notificationId: z.ZodString;
}, "strict", z.ZodTypeAny, {
    type: "task.notification.ack";
    id: string;
    taskId: string;
    notificationId: string;
}, {
    type: "task.notification.ack";
    id: string;
    taskId: string;
    notificationId: string;
}>, z.ZodObject<{
    type: z.ZodLiteral<"session.close">;
    id: z.ZodOptional<z.ZodString>;
    detach: z.ZodDefault<z.ZodLiteral<true>>;
}, "strict", z.ZodTypeAny, {
    type: "session.close";
    id?: string | undefined;
    detach: true;
}, {
    type: "session.close";
    id?: string | undefined;
    detach?: true | undefined;
}>]>, {
    type: "session.start";
    id?: string | undefined;
    protocolVersion: number;
    profileId?: string | undefined;
    userLabel?: string | undefined;
    conversation?: {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
    } | undefined;
} | {
    type: "audio.input";
    id?: string | undefined;
    data: string;
    mimeType: string;
} | {
    type: "audio.end";
    id?: string | undefined;
} | {
    type: "text.input";
    id?: string | undefined;
    text: string;
} | {
    type: "response.cancel";
    id?: string | undefined;
    reason?: string | undefined;
    truncate?: {
        itemId: string;
        contentIndex: number;
        audioEndMs: number;
    } | undefined;
} | {
    type: "task.list";
    id: string;
    limit: number;
} | {
    type: "task.get";
    id: string;
    taskId: string;
} | {
    type: "task.follow_up";
    id: string;
    taskId: string;
    message: string;
    title?: string | undefined;
} | {
    type: "task.stop";
    id: string;
    taskId: string;
    reason?: string | undefined;
} | {
    type: "task.notification.ack";
    id: string;
    taskId: string;
    notificationId: string;
} | {
    type: "session.close";
    id?: string | undefined;
    detach: true;
}, {
    type: "session.start";
    id?: string | undefined;
    protocolVersion: number;
    profileId?: string | undefined;
    userLabel?: string | undefined;
    conversation?: {
        mode: "new" | "resume" | "unbound";
        sessionId?: string | undefined;
        title?: string | undefined;
    } | undefined;
} | {
    type: "audio.input";
    id?: string | undefined;
    data: string;
    mimeType?: string | undefined;
} | {
    type: "audio.end";
    id?: string | undefined;
} | {
    type: "text.input";
    id?: string | undefined;
    text: string;
} | {
    type: "response.cancel";
    id?: string | undefined;
    reason?: string | undefined;
    truncate?: {
        itemId: string;
        contentIndex?: number | undefined;
        audioEndMs: number;
    } | undefined;
} | {
    type: "task.list";
    id: string;
    limit?: number | undefined;
} | {
    type: "task.get";
    id: string;
    taskId: string;
} | {
    type: "task.follow_up";
    id: string;
    taskId: string;
    message: string;
    title?: string | undefined;
} | {
    type: "task.stop";
    id: string;
    taskId: string;
    reason?: string | undefined;
} | {
    type: "task.notification.ack";
    id: string;
    taskId: string;
    notificationId: string;
} | {
    type: "session.close";
    id?: string | undefined;
    detach?: true | undefined;
}>;
export type ClientMessage = z.infer<typeof ClientMessageSchema>;
export type SessionStartMessage = Extract<ClientMessage, {
    type: "session.start";
}>;
export type TaskListMessage = Extract<ClientMessage, {
    type: "task.list";
}>;
export type TaskGetMessage = Extract<ClientMessage, {
    type: "task.get";
}>;
export type TaskFollowUpMessage = Extract<ClientMessage, {
    type: "task.follow_up";
}>;
export type TaskStopMessage = Extract<ClientMessage, {
    type: "task.stop";
}>;
export type TaskNotificationAckMessage = Extract<ClientMessage, {
    type: "task.notification.ack";
}>;
export type SessionCloseMessage = Extract<ClientMessage, {
    type: "session.close";
}>;
export declare function parseClientMessage(value: unknown): ClientMessage;
//# sourceMappingURL=client-protocol.d.ts.map