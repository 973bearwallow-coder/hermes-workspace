//#region extensions/codex/src/migration/provider.ts
function isMemoryOnlyMigration(ctx) {
	return Boolean(ctx.itemKinds && ctx.itemKinds.length > 0 && ctx.itemKinds.every((kind) => kind === "memory"));
}
function isAuthOnlyMigration(ctx) {
	return Boolean(ctx.itemKinds && ctx.itemKinds.length > 0 && ctx.itemKinds.every((kind) => kind === "auth"));
}
function buildCodexMigrationProvider(params = {}) {
	return {
		id: "codex",
		label: "Codex",
		description: "Import Codex memory and skills while keeping Codex native plugins and hooks explicit.",
		supportedItemKinds: ["memory", "auth"],
		async detect(ctx) {
			const { discoverCodexSource, hasCodexSource } = await import("./source-CElXU0Oy.js").then((n) => n.i);
			const source = await discoverCodexSource({
				input: ctx.source,
				memoryOnly: isMemoryOnlyMigration(ctx),
				authOnly: isAuthOnlyMigration(ctx)
			});
			const found = isMemoryOnlyMigration(ctx) ? source.memoryFiles.length > 0 : isAuthOnlyMigration(ctx) ? Boolean(source.authPath) : hasCodexSource(source);
			return {
				found,
				source: source.root,
				label: "Codex",
				confidence: found ? source.confidence : "low",
				message: found ? "Codex state found." : "Codex state not found."
			};
		},
		async plan(ctx) {
			const { buildCodexMigrationPlan } = await import("./plan-7uG-Fp36.js");
			return buildCodexMigrationPlan(ctx);
		},
		deferredApply: { retrySafe: true },
		prepareApply(ctx) {
			if (isMemoryOnlyMigration(ctx) || isAuthOnlyMigration(ctx)) return;
			return import("./apply-CvT8tW5i.js").then(({ prepareTargetCodexAppServer }) => prepareTargetCodexAppServer(ctx));
		},
		async apply(ctx, plan) {
			const { applyCodexMigrationPlan } = await import("./apply-CvT8tW5i.js");
			return await applyCodexMigrationPlan({
				ctx,
				plan,
				runtime: params.runtime
			});
		}
	};
}
//#endregion
export { buildCodexMigrationProvider as t };
