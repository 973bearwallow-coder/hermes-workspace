import { runSetupCommand } from "./setup.js";
export function upgradeSetupArgs(args) {
    return args.includes("--non-interactive")
        ? [...args]
        : ["--non-interactive", ...args];
}
export async function runUpgradeCommand(args) {
    await runSetupCommand(upgradeSetupArgs(args));
}
export function upgradeHelp() {
    return `hermes-live upgrade [setup options]

Reinstall the bundled plugin and service definitions from this npm package.
Existing provider settings and credentials stay in place.

This command does not download a newer npm package. Update the package first:
  npm install --global hermes-live-voice@latest
  hermes-live upgrade`;
}
//# sourceMappingURL=upgrade.js.map