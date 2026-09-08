# OpenAI Skills

- Repo: `openai/skills`
- URL: https://github.com/openai/skills
- Date: 2026-09-08
- Repo snapshot studied: `main` @ `49f948faa9258a0c61caceaf225e179651397431`
- Why picked today: GitHub's daily trending page listed `openai/skills` on September 8, 2026 with 490 stars today. I picked it over flashier entries because the source is an unusually inspectable example of packaging agent behavior as portable, reusable operating knowledge. The top-level [`README.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/README.md) now marks the repo deprecated in favor of [`openai/plugins`](https://github.com/openai/plugins), but the repo still teaches useful structure.

## Executive summary
[`openai/skills`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431) is not an application. It is a catalog of agent capability packages. The central idea is small and strong: a skill is a folder with a required [`SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md), optional [`agents/openai.yaml`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/agents/openai.yaml), and optional resources such as [`scripts`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts), [`references`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/references), and [`assets`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/assets).

The repo has 44 skill directories and about 780 files. That is enough surface to see a real content architecture, not just a couple of toy examples. The system split is clear: built-in skills live under [`skills/.system`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system), user-installable examples live under [`skills/.curated`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated), and each skill carries its own local workflow, helper scripts, UI metadata, references, and assets.

The builder lesson is that useful agent extensibility does not have to start with a server, API, or plugin runtime. A lot of repeatability can come from a disciplined folder contract, precise trigger metadata, progressive disclosure, and deterministic helper scripts. The weak part is lifecycle clarity: the repo is deprecated, many skills are mostly instruction bundles, and there is no central machine-readable index beyond the directory layout.

## What they built
They built a public catalog of skills for Codex-style agents. The top-level [`README.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/README.md) defines skills as folders of instructions, scripts, and resources that agents can discover and use. It also explains the two main distribution channels in this snapshot:

- Built-in system skills under [`skills/.system`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system), including [`skills/.system/imagegen`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/imagegen), [`skills/.system/openai-docs`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/openai-docs), [`skills/.system/plugin-creator`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/plugin-creator), [`skills/.system/skill-creator`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator), and [`skills/.system/skill-installer`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer).
- Curated installable skills under [`skills/.curated`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated), including targeted workflows like [`skills/.curated/gh-fix-ci`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci), [`skills/.curated/playwright`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright), [`skills/.curated/figma-implement-design`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/figma-implement-design), and [`skills/.curated/security-threat-model`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-threat-model).

The repo is basically a distribution format plus examples. The code that does real work sits inside individual skill folders, not in a shared application package.

## Why it matters
Most agent systems treat "capability" as either prompt text hidden in product code or as heavyweight plugin integration. This repo shows a middle layer: capability as a file-backed package that can be read, installed, audited, copied, and updated.

That matters because agents need more than tool schemas. They need local procedure. The [`skills/.system/skill-creator/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md) is explicit about this: metadata is always visible, the full instruction body is loaded only after trigger, and bundled resources are loaded only as needed. This "progressive disclosure" pattern is the real architecture.

The repo is also useful because it contains examples with different degrees of freedom. [`skills/.curated/gh-fix-ci/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci/SKILL.md) is a fairly narrow workflow around GitHub Actions failures. [`skills/.system/plugin-creator/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/plugin-creator/SKILL.md) is more deterministic and script-driven. [`skills/.curated/openai-docs/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/openai-docs/SKILL.md) is a routing layer to specific references.

## Repo shape at a glance
The repository has a simple top-level shape:

- [`README.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/README.md): describes Agent Skills, installation, and the deprecation notice.
- [`contributing.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/contributing.md): small community and security guidance, not a deep contributor guide.
- [`skills/.system`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system): five system skills that are expected to ship with Codex.
- [`skills/.curated`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated): 39 installable skills with domain-specific instructions, references, scripts, and assets.

Inside a mature skill, the layout becomes the actual interface:

- [`SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md): trigger metadata plus procedural instructions.
- [`agents/openai.yaml`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/agents/openai.yaml): UI-facing metadata for lists and chips.
- [`scripts`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts): deterministic helpers such as [`scripts/init_skill.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/init_skill.py), [`scripts/generate_openai_yaml.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/generate_openai_yaml.py), and [`scripts/quick_validate.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/quick_validate.py).
- [`references`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/references): deeper context such as [`references/openai_yaml.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/references/openai_yaml.md).
- [`assets`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/assets): optional images, icons, and resources that can be used without loading big blobs of instructions into context.

## Layered architecture dissection
### High-level system shape
The control flow is: the agent sees skill metadata, decides whether a skill applies, loads the matching skill's instructions, selectively reads any referenced resources, and runs bundled scripts when deterministic execution matters. The repo itself is a content-addressable knowledge base organized around that runtime behavior.

### Main layers
**1. Distribution and lifecycle layer**  
[`README.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/README.md) defines the catalog and points users to installation. The deprecation notice is important: this snapshot teaches the old skills catalog shape, while current examples have moved to [`openai/plugins`](https://github.com/openai/plugins).

**2. Skill contract layer**  
[`skills/.system/skill-creator/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md) is the best specification-like document in the repo. It says every skill needs a `SKILL.md` with YAML frontmatter containing `name` and `description`, and it describes optional [`agents/openai.yaml`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/agents/openai.yaml), [`scripts`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts), [`references`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/references), and [`assets`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/assets).

**3. Creation and validation layer**  
[`skills/.system/skill-creator/scripts/init_skill.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/init_skill.py) normalizes skill names, enforces allowed resource folders, writes starter instructions, and calls [`skills/.system/skill-creator/scripts/generate_openai_yaml.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/generate_openai_yaml.py) for UI metadata. [`skills/.system/skill-creator/scripts/quick_validate.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/quick_validate.py) gives authors a low-friction sanity check.

**4. Installation layer**  
[`skills/.system/skill-installer/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/SKILL.md) routes install requests to scripts. [`skills/.system/skill-installer/scripts/list-skills.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/scripts/list-skills.py) lists skills via the GitHub API, and [`skills/.system/skill-installer/scripts/install-skill-from-github.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/scripts/install-skill-from-github.py) installs from repo paths, URLs, downloaded archives, or sparse checkout.

**5. Domain workflow layer**  
Each curated skill is its own small playbook. [`skills/.curated/gh-fix-ci/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci/SKILL.md) is a workflow for GitHub Actions failures. [`skills/.curated/playwright/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/SKILL.md) and [`skills/.curated/playwright/scripts/playwright_cli.sh`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/scripts/playwright_cli.sh) package a repeatable browser-testing command surface. [`skills/.curated/openai-docs/references/latest-model.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/openai-docs/references/latest-model.md) and [`skills/.curated/openai-docs/references/prompting-guide.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/openai-docs/references/prompting-guide.md) show the reference-file pattern.

### Request / data / control flow
1. A user asks for a task.
2. The agent compares the task against the metadata in a skill's `SKILL.md`, such as the `description` in [`skills/.system/skill-installer/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/SKILL.md).
3. If the skill triggers, the agent loads the full body from the matching [`SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md).
4. The agent follows routing instructions to open only needed files, such as [`references/openai_yaml.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/references/openai_yaml.md).
5. When repeatability matters, the agent executes a bundled helper such as [`scripts/install-skill-from-github.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/scripts/install-skill-from-github.py) or [`scripts/playwright_cli.sh`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/scripts/playwright_cli.sh).

## Key directories and files
- [`README.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/README.md): public explanation, installation sketch, and deprecation notice.
- [`skills/.system`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system): built-in skills that reveal the intended core agent workflow.
- [`skills/.curated`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated): user-installable examples across deployment, design, docs, security, browser testing, and productivity.
- [`skills/.system/skill-creator/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md): the closest thing to a format guide.
- [`skills/.system/skill-creator/scripts/init_skill.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/init_skill.py): scaffolding and naming logic.
- [`skills/.system/skill-installer/scripts/install-skill-from-github.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/scripts/install-skill-from-github.py): install path, archive download, sparse-checkout fallback, and destination validation.
- [`skills/.curated/gh-fix-ci/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci/SKILL.md): a narrow task skill with clear prerequisites, scopes, and fallback behavior.
- [`skills/.curated/playwright/scripts/playwright_cli.sh`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/scripts/playwright_cli.sh): a tiny wrapper that proves skills can package commands as well as prose.

## Important components
The most important component is the skill folder contract described in [`skills/.system/skill-creator/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md). It is a deliberately simple boundary: metadata for triggering, instructions for behavior, resources for depth, scripts for repeatability, assets for output.

The second important component is [`skills/.system/skill-installer/scripts/install-skill-from-github.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/scripts/install-skill-from-github.py). It handles public downloads first, falls back to sparse git checkout for auth or unavailable paths, validates that the selected path contains a real skill, and refuses to overwrite an existing destination.

The third is [`agents/openai.yaml`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/agents/openai.yaml). It is not algorithmically deep, but it matters because skills are both runtime objects and UI objects. Discoverability is part of the product surface.

## Important knobs / configs / extension points
- Frontmatter in [`SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md): `name` and `description` decide whether the agent should load a skill at all.
- [`agents/openai.yaml`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/agents/openai.yaml): display name, short description, and default prompt for the UI layer.
- Resource directories such as [`scripts`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts), [`references`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/references), and [`assets`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/assets): the main extension points for each skill.
- Installer arguments in [`skills/.system/skill-installer/scripts/install-skill-from-github.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/scripts/install-skill-from-github.py): `--repo`, `--url`, `--path`, `--ref`, `--dest`, `--name`, and `--method` turn GitHub folders into local capabilities.
- Scaffold options in [`skills/.system/skill-creator/scripts/init_skill.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/init_skill.py): resource creation and interface metadata can be generated predictably.

## Practical questions and answers
**Is this mostly prompt engineering?**  
Partly, but the useful part is packaging discipline. A skill like [`skills/.curated/gh-fix-ci/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci/SKILL.md) is prompt text, but it encodes trigger criteria, prerequisites, failure boundaries, and a tool workflow.

**Where is the real engineering?**  
In the boundary between prose and deterministic helpers. [`skills/.system/skill-installer/scripts/install-skill-from-github.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/scripts/install-skill-from-github.py) does the fragile install work; [`skills/.system/skill-creator/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md) tells the agent when and why to use it.

**What should builders copy?**  
Copy progressive disclosure. Keep always-visible metadata short, load the main instructions only when needed, and keep heavy details in linked references like [`skills/.curated/openai-docs/references/prompting-guide.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/openai-docs/references/prompting-guide.md).

**What should builders distrust?**  
Treat the repo as an example snapshot, not the current product truth. The deprecation notice in [`README.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/README.md) says new examples have moved.

## What is smart
- The format uses plain folders and Markdown, so a skill can be reviewed, diffed, installed, and copied.
- The trigger description in each [`SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md) is treated as a product-critical interface, not decorative metadata.
- The skill-creation guidance explicitly discusses degrees of freedom in [`skills/.system/skill-creator/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md): use prose when judgement matters, scripts when operations are fragile.
- The installer has public download and sparse-checkout paths in [`skills/.system/skill-installer/scripts/install-skill-from-github.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/scripts/install-skill-from-github.py), which is the right split for public and private GitHub sources.
- The curated examples show that a capability package can be tiny when the task is tiny, as in [`skills/.curated/playwright/scripts/playwright_cli.sh`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/scripts/playwright_cli.sh).

## What is flawed or weak
- The top-level [`README.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/README.md) says the repo is deprecated, so builders should not treat the exact layout as the newest distribution path.
- There is no repo-level generated manifest listing the 44 skills, their descriptions, resource types, and current status. Consumers infer too much from [`skills/.system`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system) and [`skills/.curated`](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated).
- Quality and depth vary by skill. That is natural for a catalog, but it makes the package contract more important than any single example.
- Some scripts assume external tooling or network state, as [`skills/.curated/playwright/scripts/playwright_cli.sh`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/scripts/playwright_cli.sh) does with `npx`.

## What we can learn / steal
- Make agent capabilities file-native before making them platform-native.
- Put the trigger surface in metadata and keep it concise enough that the agent can always afford to see it.
- Move fragile repeatable operations into bundled scripts, as [`skills/.system/skill-installer/scripts/install-skill-from-github.py`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-installer/scripts/install-skill-from-github.py) does.
- Put bulky domain details behind explicit references, as [`skills/.system/skill-creator/references/openai_yaml.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/references/openai_yaml.md) does.
- Treat deprecation notices as architecture evidence. This repo captures a useful transition from skill folders toward plugin-packaged skills.

## How we could apply it
For our own recurring builder work, I would copy the shape but add a repo-level generated index. Each capability would have one short `SKILL.md`, one optional `references` folder for deep context, and helper scripts only for tasks that are easy to get wrong. The most important local rule would be the same as [`skills/.system/skill-creator/SKILL.md`](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md): spend context only when the task proves it needs that context.

## Bottom line
`openai/skills` is worth studying because it turns "agent memory and process" into a portable source tree. The repo is deprecated, but the pattern is still sharp: small trigger metadata, scoped instructions, optional references, optional scripts, optional assets, and a bias toward progressive disclosure.

The durable builder lesson is that agent extensibility is not only about new tools. It is also about packaging good judgement so it can be discovered and reused.
