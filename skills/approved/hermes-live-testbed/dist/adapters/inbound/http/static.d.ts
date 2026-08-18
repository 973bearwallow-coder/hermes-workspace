import type { IncomingMessage, ServerResponse } from "node:http";
export declare function serveStatic(req: IncomingMessage, res: ServerResponse, options: {
    root: string;
    fallback?: string;
}): boolean;
export declare function resolveStaticPath(root: string, rawPathname: string, fallback?: string): string | null;
//# sourceMappingURL=static.d.ts.map