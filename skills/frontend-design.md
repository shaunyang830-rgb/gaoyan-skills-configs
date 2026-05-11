---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Reference Design Systems

A curated library of world-class DESIGN.md files is available in the vault. **Before designing, consider referencing one or more of these systems** as aesthetic inspiration or a direct style guide.

| Brand | File Path | Aesthetic Signature |
|-------|-----------|-------------------|
| **高岩科技** | `高岩知识库/assets/design-systems/gaoyan-DESIGN.md` | 餐饮大数据专业感，高岩蓝+厨人黄双色，微软雅黑+Century Gothic，报告/产品双模式 |
| **Notion** | `高岩知识库/assets/design-systems/notion-DESIGN.md` | Warm minimalism, NotionInter, whisper borders, 4-layer shadows |
| **Stripe** | `高岩知识库/assets/design-systems/stripe-DESIGN.md` | Fintech luxury, sohne-var weight 300, blue-tinted shadows, deep navy |
| **Linear** | `高岩知识库/assets/design-systems/linear-DESIGN.md` | Dark-mode native, Inter 510 weight, semi-transparent borders, indigo accent |
| **Apple** | `高岩知识库/assets/design-systems/apple-DESIGN.md` | Cinematic minimalism, SF Pro, binary light/dark rhythm, single blue accent |
| **Figma** | `高岩知识库/assets/design-systems/figma-DESIGN.md` | Monochrome chrome + vibrant gradients, figmaSans variable, pill geometry |
| **Spotify** | `高岩知识库/assets/design-systems/spotify-DESIGN.md` | Dark immersive, Spotify Green accent, pill/circle geometry, content-first |
| **Uber** | `高岩知识库/assets/design-systems/uber-DESIGN.md` | Bold black/white, UberMove, 999px pills, whisper-soft shadows |
| **Vercel** | `高岩知识库/assets/design-systems/vercel-DESIGN.md` | Developer minimalism, Geist, shadow-as-border technique, aggressive tracking |
| **Cursor** | `高岩知识库/assets/design-systems/cursor-DESIGN.md` | Warm cream, CursorGothic + jjannon serif, oklab borders, orange accent |

**How to use:**
- User mentions a brand style → read the corresponding DESIGN.md for exact tokens
- User says "clean/minimal" → consider Notion, Vercel, or Apple
- User says "dark/developer" → consider Linear, Spotify, or Cursor
- User says "SaaS/product" → consider Stripe or Linear
- User wants "bold/high contrast" → consider Uber or Figma
- Otherwise → use the design systems as inspiration while forging your own distinct aesthetic

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
