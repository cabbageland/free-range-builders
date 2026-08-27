# Claude Code Plugins Directory

- Repo: `anthropics/claude-plugins-official`
- URL: https://github.com/anthropics/claude-plugins-official
- Date: 2026-08-27
- Repo snapshot studied: `main` @ `b819188d2eea14e0400556ca29dbd1179a7c595b`
- Why picked today: GitHub's daily trending page surfaced this repo, and the GitHub repo API showed 34,584 stars and 3,905 forks when checked. It is interesting because the valuable part is not "app code" but the install contract: a marketplace registry, immutable slugs, local plugin bundles, remote provenance, and declarative behavior surfaces that are unusually easy to study.

## Executive summary
[`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b) is not a normal product repo. It is a control plane for Claude Code extensions. The real center of gravity is [`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json), which encodes plugin identity, source provenance, category, homepage, rename migration, and the distinction between strict plugin bundles and looser skill bundles.

The smartest thing here is that plugin behavior is expressed as files, not hidden service state. The root [`README.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/README.md) defines the filesystem contract. [`plugins/example-plugin`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin) shows the minimum shape. [`plugins/code-review/commands/code-review.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review/commands/code-review.md) proves that even fairly elaborate review orchestration can live in auditable markdown plus frontmatter. [`plugins/mcp-server-dev/skills/build-mcp-server/SKILL.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/mcp-server-dev/skills/build-mcp-server/SKILL.md) shows the same pattern for longer-form guidance.

The weak side is that the repo is also a trust-distribution system. The top-level README explicitly warns that Anthropic does not control every included MCP server, file, or dependency. The registry is strong, but many actual behaviors are federated across external repos and partner-maintained sources, so operational quality is inevitably uneven.

## What they built
They built an official plugin marketplace repo for Claude Code with four concrete parts:

- A root registry in [`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json).
- A set of Anthropic-maintained internal plugins under [`plugins`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins). The API listing exposed 39 entries when checked.
- A set of partner and community plugins under [`external_plugins`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/external_plugins). The API listing exposed 15 entries when checked.
- A consistent on-disk extension shape built around [`.claude-plugin/plugin.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/.claude-plugin/plugin.json), optional [`.mcp.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/.mcp.json), command markdown, and skill directories.

## Why it matters
Most extension marketplaces get mushy at exactly the point where builders need precision. This repo is valuable because the install and packaging boundary is explicit.

1. [`README.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/README.md) documents the plugin directory layout and the installation path `/plugin install {plugin-name}@claude-plugins-official`.
2. [`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json) records provenance in machine-readable form instead of leaving the marketplace as a bag of links.
3. [`plugins/code-review/commands/code-review.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review/commands/code-review.md) shows that a plugin command can be an auditable orchestration spec with allowed-tool boundaries, agent fan-out, and filtering rules.
4. [`plugins/mcp-server-dev/skills/build-mcp-server/SKILL.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/mcp-server-dev/skills/build-mcp-server/SKILL.md) shows the repo is not only about pointing at MCP servers. It also packages longer-lived builder workflows as skills.

## Repo shape at a glance
The repo has a clean, layered shape:

- [`README.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/README.md): installation, trust model, immutable-slug rule, and the standard plugin directory layout.
- [`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json): canonical marketplace registry, rename map, categories, and source descriptors.
- [`plugins`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins): Anthropic-maintained plugins such as [`code-review`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review), [`mcp-server-dev`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/mcp-server-dev), and [`example-plugin`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin).
- [`external_plugins`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/external_plugins): local wrappers for partner/community entries such as [`github`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/external_plugins/github), [`playwright`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/external_plugins/playwright), and [`terraform`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/external_plugins/terraform).

## Layered architecture dissection
### High-level system shape
The high-level system is: one marketplace slug resolves to one registry entry, the registry entry resolves to either a local directory, a remote git URL, or a git subdirectory, and the installed plugin becomes a filesystem bundle of manifests, commands, skills, and optional MCP configuration. This is a packaging architecture more than an application architecture.

### Main layers
**1. Marketplace identity layer**  
[`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json) is the authoritative ledger. It defines top-level metadata, the [`renames` map](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json#L9-L18), and per-plugin source records that can be local paths, raw URLs, or `git-subdir` descriptors with pinned refs and SHAs.

**2. Bundle-shape layer**  
[`README.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/README.md) defines the plugin directory contract. [`plugins/example-plugin`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin) makes it concrete with [`.claude-plugin/plugin.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/.claude-plugin/plugin.json), [`.mcp.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/.mcp.json), [`commands`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/commands), and [`skills`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/skills).

**3. Declarative behavior layer**  
[`plugins/code-review/commands/code-review.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review/commands/code-review.md) shows behavior written as frontmatter plus a precise instruction program. [`plugins/mcp-server-dev/skills/build-mcp-server/SKILL.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/mcp-server-dev/skills/build-mcp-server/SKILL.md) does the same for a long-form design workflow.

**4. Federated source layer**  
The registry contains both fully local entries like [`agent-sdk-dev`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json#L54-L66) and remote or subdirectory-based entries like [`42crunch-api-security-testing`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json#L19-L37) and the non-strict AMD skills bundle in [`marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json#L220-L234). That means the marketplace is designed to curate across many repos without forcing one packaging style.

### Request / data / control flow
The install flow described in [`README.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/README.md) is conceptually simple:

1. The user installs a slug from `claude-plugins-official`.
2. The loader checks [`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json), including the rename map if the old slug was retained for migration.
3. The loader resolves the plugin `source`, which may be local, `url`, or `git-subdir`.
4. Claude Code then consumes the plugin bundle's manifests and directories, such as [`.mcp.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/.mcp.json), [`commands`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review/commands), or [`skills`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/mcp-server-dev/skills).

## Key directories and files
- [`README.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/README.md): the shortest path to the packaging contract and trust model.
- [`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json): the canonical registry and provenance layer.
- [`plugins/example-plugin`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin): the minimal reference implementation.
- [`plugins/code-review`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review): a good example of behavior-as-markdown.
- [`plugins/mcp-server-dev`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/mcp-server-dev): a good example of behavior-as-skill-bundle.
- [`external_plugins`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/external_plugins): proof that third-party curation is a first-class part of the repo shape.

## Important components
The single most important component is [`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json). It is the difference between a discoverable marketplace and a folder full of bundles.

The second is [`plugins/example-plugin/.claude-plugin/plugin.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/.claude-plugin/plugin.json). Its minimal fields are a useful clue: identity metadata is tiny, while the real capability surface comes from the surrounding directory tree.

The third is [`plugins/code-review/commands/code-review.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review/commands/code-review.md). That file reads like a tiny orchestration program: tool allowlist, agent fan-out, confidence scoring rubric, and posting rules.

The fourth is [`plugins/mcp-server-dev/skills/build-mcp-server/SKILL.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/mcp-server-dev/skills/build-mcp-server/SKILL.md), which shows that the plugin format is capable of carrying real builder workflows, not just one-shot commands.

## Important knobs / configs / extension points
- [`README.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/README.md): immutable plugin slugs, `displayName` guidance, and rename migration rules.
- [`marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json): `source`, `category`, `homepage`, `strict`, `skills`, and pinned SHA fields.
- [`plugins/example-plugin/.mcp.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/.mcp.json): the MCP integration seam.
- [`plugins/code-review/commands/code-review.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review/commands/code-review.md): `allowed-tools` and command-level review workflow.
- The AMD skills bundle entry in [`marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json#L220-L234): a concrete example of `strict: false` plus explicit skill exports.

## Practical questions and answers
**Is this just a list of recommended repos?**  
No. [`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json) stores enough metadata to act as the authoritative install registry.

**Where does plugin behavior actually live?**  
In the bundle files themselves: [`.claude-plugin/plugin.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/.claude-plugin/plugin.json), [`.mcp.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/.mcp.json), [`commands`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review/commands), and [`skills`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/mcp-server-dev/skills).

**How does the repo handle renames without breaking installed users?**  
The root [`renames` map](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json#L9-L18) keeps old slugs migratable.

**Can the marketplace curate skill bundles that are not strict plugins?**  
Yes. The AMD entry in [`marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json#L220-L234) uses `strict: false` and a `skills` array to expose selected skill directories from a larger repo.

**What should a builder read first?**  
Start with [`README.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/README.md), then [`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json), then [`plugins/example-plugin`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin), [`plugins/code-review`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review), and [`plugins/mcp-server-dev`](https://github.com/anthropics/claude-plugins-official/tree/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/mcp-server-dev).

## What is smart
- Making the marketplace itself a versioned repo with explicit install provenance in [`.claude-plugin/marketplace.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json).
- Treating immutable slugs plus a [`renames` map](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/.claude-plugin/marketplace.json#L9-L18) as first-class migration infrastructure.
- Using ordinary files like [`code-review.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review/commands/code-review.md) and [`SKILL.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/mcp-server-dev/skills/build-mcp-server/SKILL.md) as the auditable behavior surface.
- Supporting both strict plugin bundles and curated skill bundles instead of forcing one packaging style on every source.

## What is flawed or weak
- [`README.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/README.md) has to warn users about plugin trust, which is the unavoidable downside of federating many third-party MCP servers and repos.
- The visible plugin manifests such as [`plugins/example-plugin/.claude-plugin/plugin.json`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/example-plugin/.claude-plugin/plugin.json) are intentionally small, which keeps identity simple but leaves a lot of behavior encoded in conventions elsewhere.
- Command logic in files like [`code-review.md`](https://github.com/anthropics/claude-plugins-official/blob/b819188d2eea14e0400556ca29dbd1179a7c595b/plugins/code-review/commands/code-review.md) is readable, but prose-heavy orchestration is harder to statically validate than typed code.
- The marketplace centralizes discovery, but actual reliability is split across many external source repos and pinned SHAs, which means quality assurance is distributed rather than unified.

## What we can learn / steal
- Put extension provenance in a versioned registry, not only in a UI database.
- Treat renames and migration as part of the product contract from day one.
- Keep the bundle contract filesystem-native so builders can inspect it with ordinary tools.
- Allow "skill bundles" and "full plugins" to coexist instead of overfitting one install model.

## How we could apply it
If we were building our own extension marketplace, I would copy three things almost verbatim: one canonical registry file, immutable install slugs with rename migration, and a filesystem-first bundle format that can carry commands, skills, and MCP wiring without hiding everything behind opaque hosted state.

I would add stronger automated validation over command and skill surfaces, but the repo's core packaging discipline is excellent.

## Bottom line
`claude-plugins-official` is worth studying because it turns plugin distribution into a concrete, inspectable source contract instead of an invisible marketplace backend.

The main builder lesson is that a marketplace becomes much more durable once install identity, provenance, migration, and capability shape are all visible in files.
