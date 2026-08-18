export interface PluginInstallOptions {
    dir?: string;
    mode?: "copy" | "symlink";
    force?: boolean;
}
export interface PluginInstallStatus {
    source: string;
    target: string;
    installed: boolean;
    manifestFound: boolean;
    symlink: boolean;
    symlinkTarget?: string;
    mode?: "copy" | "symlink";
    enabledHint: string;
}
export declare function installHermesPlugin(options?: PluginInstallOptions): Promise<PluginInstallStatus>;
export declare function pluginInstallStatus(options?: PluginInstallOptions): Promise<PluginInstallStatus>;
export declare function pluginSourceDir(): string;
export declare function pluginTargetDir(options?: PluginInstallOptions): string;
export declare function hermesPluginsDir(options?: PluginInstallOptions): string;
export declare function packageRoot(): string;
//# sourceMappingURL=plugin-installer.d.ts.map