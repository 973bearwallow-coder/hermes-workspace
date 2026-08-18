export const MAX_LIVE_TASK_NOTIFICATION_CONTEXT_CHARS = 1_000;
export const MAX_LIVE_TASK_NOTIFICATION_ANNOUNCEMENT_CHARS = 500;
export function requireLiveTaskNotification(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
        throw new Error("Task notification is invalid.");
    }
    const candidate = value;
    return {
        context: requireTaskNotificationText(candidate.context, MAX_LIVE_TASK_NOTIFICATION_CONTEXT_CHARS, "context"),
        announcement: requireTaskNotificationText(candidate.announcement, MAX_LIVE_TASK_NOTIFICATION_ANNOUNCEMENT_CHARS, "announcement"),
    };
}
function requireTaskNotificationText(value, maximumChars, field) {
    if (typeof value !== "string" ||
        value.length === 0 ||
        value.length > maximumChars ||
        value.trim().length === 0 ||
        /[\u0000-\u001f\u007f-\u009f]/u.test(value)) {
        throw new Error(`Task notification ${field} is invalid.`);
    }
    return value;
}
//# sourceMappingURL=realtime-model.port.js.map