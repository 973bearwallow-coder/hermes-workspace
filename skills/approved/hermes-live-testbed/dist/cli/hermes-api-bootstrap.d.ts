export interface HermesApiEnvironmentResult {
    path: string;
    changed: boolean;
    created: boolean;
}
export declare function resolveHermesHome(home: string, env: NodeJS.ProcessEnv): string;
export declare function generateHermesApiKey(): string;
export declare function isDefaultLocalHermesApi(value: string): boolean;
/**
 * Persist the private loopback bridge that Hermes Live Voice needs.
 *
 * This intentionally edits only the two API-server variables in Hermes' own
 * environment file. Unknown settings and comments are preserved, and the
 * replacement is atomic so an interrupted setup cannot truncate Hermes config.
 */
export declare function ensureHermesApiEnvironment(hermesHome: string, apiKey: string): Promise<HermesApiEnvironmentResult>;
//# sourceMappingURL=hermes-api-bootstrap.d.ts.map