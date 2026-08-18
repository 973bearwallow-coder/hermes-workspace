export declare const GEMINI_LIVE_INPUT_SAMPLE_RATE = 16000;
export declare const CLIENT_CAPTURE_SAMPLE_RATE = 24000;
export declare const MIN_PCM_SAMPLE_RATE = 8000;
export declare const MAX_PCM_SAMPLE_RATE = 192000;
export declare const MAX_RESAMPLED_PCM16_BYTES: number;
export interface PcmAudioFrame {
    data: string;
    mimeType: string;
}
export declare function normalizePcm16Audio<T extends PcmAudioFrame>(audio: T, targetRate: number): T;
export declare function parsePcmSampleRate(mimeType: string): number | undefined;
export declare function requirePcmSampleRate(mimeType: string): number;
export declare function isValidPcmSampleRate(sampleRate: unknown): sampleRate is number;
export declare function validatePcmSampleRate(sampleRate: unknown, label?: string): asserts sampleRate is number;
export declare function isPcmMimeType(mimeType: string): boolean;
export declare function pcmMimeType(sampleRate: number): string;
export declare function resamplePcm16Base64(data: string, sourceRate: number, targetRate: number): string;
//# sourceMappingURL=pcm.d.ts.map