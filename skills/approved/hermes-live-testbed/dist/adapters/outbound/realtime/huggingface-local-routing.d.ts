import type { LiveToolName } from "../../../application/live-gateway/ports/realtime-model.port.js";
export interface LocalRoutedAction {
    name: Extract<LiveToolName, "continue_hermes_conversation" | "start_background_task" | "list_background_tasks" | "follow_up_background_task" | "stop_background_task" | "pause_voice_input">;
    args: Record<string, unknown>;
    taskQuestion?: string;
    taskControl?: {
        type: "stop";
        selection: "latest" | "single";
    } | {
        type: "stop";
        selection: "matching";
        query: string;
    } | {
        type: "follow_up";
        message: string;
    };
}
export type LocalTaskMatch = {
    status: "matched";
    taskId: string;
} | {
    status: "ambiguous";
    count: number;
} | {
    status: "not_found";
};
export declare function isExplicitLocalDelegationRequest(text: string): boolean;
export declare function isClearLocalWorkRequest(text: string): boolean;
export declare function localRoutedAction(text: string): LocalRoutedAction | undefined;
export declare function buildLocalTaskQuestionResponse(question: string, toolResponse: Record<string, unknown>): Record<string, unknown>;
export declare function selectLocalTaskForQuestion(question: string, toolResponse: Record<string, unknown>): string | undefined;
export declare function buildLocalExactSpeechResponse(spoken: string): Record<string, unknown>;
export declare function selectLocalStoppableTasks(toolResponse: Record<string, unknown>): string[];
export declare function matchLocalStoppableTask(toolResponse: Record<string, unknown>, query: string): LocalTaskMatch;
export declare function selectLocalFinishedTask(toolResponse: Record<string, unknown>): string | undefined;
export declare function buildLocalConversationResponse(toolResponse: Record<string, unknown>): Record<string, unknown>;
//# sourceMappingURL=huggingface-local-routing.d.ts.map