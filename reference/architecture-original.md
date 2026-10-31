<!-- ══════════════════════════════════════════════════════════════════
     GigaNuke3: one facility, five bays.
       00 IDENT       who builds here
       01 TERRAIN     the last year of contributions, built on
       02 SETTLEMENT  this month, as a city
       03 PAYLOADS    the repositories: what gets built
       04 FLIGHT      the last four months, launched
     Every card is a generated SVG (scripts/), re-rendered hourly from
     live GitHub data by .github/workflows/profile-cards.yml.
     ══════════════════════════════════════════════════════════════════ -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dark_mode.svg?v=2">
  <img alt="GigaNuke3 terminal profile: AI Engineer / Software Developer, Local AI, Ollama, LLMs" src="light_mode.svg?v=2" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="tetris_dark.svg?v=2">
  <img alt="Terrain: this year's GitHub contributions as ground, with tetrominoes stacking onto it" src="tetris_light.svg?v=2" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="graph_dark.svg?v=2">
  <img alt="Code City: a miniature city built by this month's GitHub contributions" src="graph_light.svg?v=2" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="payloads_dark.svg?v=2">
  <img alt="Payload manifest: every public repository as a payload module, ordered by creation, sized by repository size, lit by recent pushes" src="payloads_light.svg?v=2" width="100%">
</picture>

<!-- manifest:start -->
<details>
<summary><b>OPEN THE PAYLOAD MANIFEST</b>: every module above, with links</summary>

| PAYLOAD | LANG | STATUS | LAST PUSH | NOTE |
|---|---|---|---|---|
| [HandsMenThreadsProject](https://github.com/GigaNuke3/HandsMenThreadsProject) | — | COLD | 2025-11-25 |  |
| [To-do-list-Web-app-But-evolves-progressively-](https://github.com/GigaNuke3/To-do-list-Web-app-But-evolves-progressively-) | PHP | COLD | 2026-03-21 |  |
| [chatapp](https://github.com/GigaNuke3/chatapp) | PHP | COLD | 2026-04-24 |  |
| [My-Bestfriends-Bday](https://github.com/GigaNuke3/My-Bestfriends-Bday) | TypeScript | COLD | 2026-07-27 |  |
| [Callama](https://github.com/GigaNuke3/Callama) | CSS | WARM | 2026-08-17 | Callama is an Ollama Electron Engine Application for Personal Use |
| [GigaNuke3](https://github.com/GigaNuke3/GigaNuke3) | Python | LIVE | 2026-10-05 |  |
| [Road-To-Ai-Engineering](https://github.com/GigaNuke3/Road-To-Ai-Engineering) | Python | LIVE | 2026-09-24 | To Become an Ai Engineer |
| [Specification-First-Model-Orchestration-SFMO-](https://github.com/GigaNuke3/Specification-First-Model-Orchestration-SFMO-) | — | WARM | 2026-09-12 | It's a Documentation Approach on Creating Applications Using the SFMO Method which I  created on which it will help for an Efficient and Elegant Way of Using Tokens for better Execution Generation. |
| [Portfolio](https://github.com/GigaNuke3/Portfolio) | TypeScript | LIVE | 2026-10-01 |  |

</details>
<!-- manifest:end -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="activity_dark.svg?v=2">
  <img alt="Mission Control: the last four months of contribution activity as a multi-stage rocket launch along a flight trajectory" src="activity_light.svg?v=2" width="100%">
</picture>

<div align="center">
  <p><strong>AI ENGINEERING · SOFTWARE · LOCAL AI</strong></p>
  <p><a href="https://github.com/GigaNuke3">GitHub</a></p>
</div>

## Design reference: principles for an original design

This section documents the project's visual language for reference. Use its principles of hierarchy, consistency, and meaningful data visualization when designing something new. Create a separate identity, composition, and visual metaphor; do not reproduce the GigaNuke3 profile, artwork, or five-bay design with different text.

### Project and UI structure

This is a GitHub profile README composed of generated SVG images, not a conventional web application. Python scripts generate paired dark/light panels; the README selects a theme through `<picture>` and displays each image at full container width. The repository manifest is a native `<details>` disclosure with a Markdown table and working repository links.

| Existing panel | Content and presentation | Transferable principle |
|---|---|---|
| Identity | Terminal-style title bar, square portrait on the left, aligned profile text on the right | Establish who the page belongs to and what they do before showing detailed activity |
| Terrain | Large summary numbers above a contribution grid with falling tetrominoes | Make summary metrics easy to scan, then reveal the underlying history |
| Settlement | Monthly contributions represented by a miniature city, with today's lot emphasized | Give data a coherent visual metaphor and clearly locate the present |
| Payloads | Repository modules arranged by creation date, with size and recency cues | Encode distinct facts consistently and provide a readable text counterpart |
| Flight | Recent activity presented through a rocket launch and monthly detail blocks | Combine an overview with supporting details in a predictable reading order |

The cards share a frame, type family, palette, and alignment rules. That repetition makes varied content feel related. The facility narrative, bay names, terrain game, city, and launch sequence together form this project's distinctive identity; a new design should develop its own organizing idea.

### Visual style and layout

The style is a compact engineering console: flat neutral surfaces, thin borders, warm accents, crisp pixel geometry, small metadata, and precise alignment. Detail comes from grids, dither patterns, outlined structures, and data rather than large shadows or decorative gradients.

Most panels use a 900-unit-wide SVG canvas; the terrain panel calculates its width from the calendar columns. The shared content margin is 28 units, while the identity panel has its own internal offsets. Frames use a 1-unit border, a 4-unit corner radius, orange corner registration marks, and a small bottom-right bay label. Common panel headers place a title on the left, context on the right, and a divider beneath. Summary values sit above the main visualization.

For a new design, carry over consistent alignment, clear grouping, and a deliberate density of information. Choose new proportions, spacing, frame treatment, and content arrangement. The exact registration marks and terminal chrome are reference details, not a template to trace.

### Color roles

These are the shared source values in [profile_card.py](scripts/profile_card.py), recorded to explain the existing design rather than prescribe a new palette. The city and flight illustrations add their own supporting shades.

| Role | Dark theme | Light theme |
|---|---|---|
| Surface | `#0d1117` | `#f6f8fa` |
| Border | `#30363d` | `#d0d7de` |
| Primary text | `#f0f3f6` | `#24292f` |
| Accent / key | `#ffa657` | `#953800` |
| Secondary value | `#c9d1d9` | `#57606a` |
| Muted text | `#8b949e` | `#6e7781` |

Neutral colors carry most of the scene; the warm accent connects headings, current activity, status indicators, and structural details. The identity card uses the accent more heavily for its profile text. Light mode adapts the accent to a darker rust color rather than simply inverting the dark theme. For an original design, define equivalent semantic roles with a distinct palette and check contrast on the actual backgrounds.

### Typography

All SVG cards inherit `Consolas, 'Courier New', monospace`; there is no bundled custom font. The monospace rhythm supports aligned numbers, compact labels, and the terminal character of the profile. The surrounding Markdown uses GitHub's typography instead.

| Use in the existing SVGs | Typical source size / treatment |
|---|---|
| Summary metrics | 19–24 units; bold in the city and flight panels |
| Main panel titles | 15 units, bold, usually uppercase |
| Identity name | 14 units, bold |
| Profile text and terrain labels | Approximately 11–12.5 units |
| Supporting metadata | Approximately 7.5–9.5 units |
| Fine annotations | Often 6.5–8 units; some illustration lettering is smaller |
| Bay footer | 7 units with 1-unit letter spacing |

Hierarchy comes from size, weight, color, alignment, and selective uppercase labels rather than multiple font families. The identity readout uses a tight 13.6-unit line step. These are SVG coordinates, not recommended website text sizes: shrinking the image also shrinks every label.

For a new application, establish a readable body size and line height for the target screen. Use monospace where it helps numbers or technical metadata, and choose the overall type system to suit the new identity. Do not carry tiny chart annotations over into essential UI text.

### Motion, interaction, and accessibility

The SVGs use looping SMIL animation: a blinking cursor, falling pieces, city activity, repository status lights, and a staged rocket launch. Some motion conveys state; some creates atmosphere. Shared CSS responds to `prefers-reduced-motion` by hiding `.fx` layers and showing `.still` alternatives where provided.

The embedded panels are images, not interactive dashboards. The terminal dots are decorative, and the repository links live in the Markdown manifest. SVG `<title>` annotations in the source should not be treated as a reliable tooltip interface when the SVG is embedded as an image. The README supplies image alt text, but that text does not expose every visualized data point.

For a new UI, keep essential content available without motion, provide readable text equivalents for meaningful charts, and use real semantic links and controls for actions. Preserve keyboard access and visible focus. The current images scale as a whole rather than rearranging their internal layout; an application should reflow content on smaller screens instead of shrinking a desktop composition until its labels are unreadable.

### Applying the reference without copying

- Reuse the reasoning: consistent components, strong information hierarchy, limited color roles, aligned metrics, and understandable data mappings.
- Create a new composition: choose sections and reading order from the new product's needs rather than recreating these five panels.
- Develop an independent identity: use original naming, copy, imagery, iconography, visual metaphor, typography choices, and motion choreography.
- Avoid copying the portrait, GN3 branding, bay labels, terminal prompt, pixel scenes, or their combined arrangement. Recoloring the same composition is not an original direction.
- Review the result at narrow widths, in both themes, and with reduced motion. Essential information must remain readable and accessible.

**Reusable design brief:** “Create an original interface informed by disciplined alignment, clear metric hierarchy, restrained color, and purposeful data visualization. Develop its identity and layout around the new content. Use this project to understand design decisions, while creating new artwork, typography treatment, component geometry, and interaction patterns. Support readable responsive layouts, accessible controls, and reduced motion.”

### Source map

- [profile_card.py](scripts/profile_card.py): shared frame, theme tokens, font stack, reduced-motion CSS, and identity layout.
- [grid_common.py](scripts/grid_common.py) and [tetris_grid.py](scripts/tetris_grid.py): pixel/dither treatments, metric tiles, calendar geometry, and terrain animation.
- [code_city.py](scripts/code_city.py): monthly city metaphor, building palette, header hierarchy, and current-day emphasis.
- [payloads.py](scripts/payloads.py): repository modules, status encoding, and the linked Markdown manifest.
- [activity.py](scripts/activity.py): mission layout, timeline animation, and monthly detail blocks.

This reference is outside the `manifest:start` / `manifest:end` block so automatic repository-table updates preserve it.
