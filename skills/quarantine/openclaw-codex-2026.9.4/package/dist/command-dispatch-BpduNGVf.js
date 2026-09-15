import { o as formatCodexDisplayText } from "./command-formatters-lxlkNZgU.js";
import { n as describeControlFailure } from "./capabilities-8vx68WLH.js";
//#region extensions/codex/src/command-dispatch.ts
/** Dispatches a `/codex` command to the lazily loaded handler. */
async function handleCodexCommand(ctx, options) {
	const { loadSubcommandHandler, resolvePluginConfig, ...subcommandOptions } = options;
	try {
		return await (loadSubcommandHandler ? await loadSubcommandHandler() : await loadDefaultCodexSubcommandHandler())(ctx, {
			...subcommandOptions,
			pluginConfig: resolvePluginConfig?.() ?? subcommandOptions.pluginConfig
		});
	} catch (error) {
		return { text: `Codex command failed: ${formatCodexDisplayText(describeControlFailure(error))}` };
	}
}
async function loadDefaultCodexSubcommandHandler() {
	const { handleCodexSubcommand } = await import("./command-handlers-tiL9iWj7.js");
	return handleCodexSubcommand;
}
//#endregion
export { handleCodexCommand };
