//#region extensions/codex/src/app-server/version.ts
/**
* Version and package pins for the managed Codex app-server runtime.
*/
/** Exact Codex app-server version shipped by the OpenClaw Codex bridge. */
const CODEX_APP_SERVER_VERSION = "0.153.4";
/** Inclusive runtime compatibility floor for external app-server binaries. */
const MIN_SUPPORTED_CODEX_APP_SERVER_VERSION = "0.149.0";
/** npm package name for the managed Codex app-server binary. */
const MANAGED_CODEX_APP_SERVER_PACKAGE = "@openai/codex";
//#endregion
export { MANAGED_CODEX_APP_SERVER_PACKAGE as n, MIN_SUPPORTED_CODEX_APP_SERVER_VERSION as r, CODEX_APP_SERVER_VERSION as t };
