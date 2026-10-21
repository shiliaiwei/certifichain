---
name: certifier-editorial-luxury-design
description: Authoritative design standard for Certifier Studio editorial luxury system. Covers full-screen hero section architecture, oversized monumental V logo, interactive frosted capsule navigation dock, continuous right-side certificate marquee, clean 3-color palette (Pure White #ffffff, Deep Charcoal #0f172a, Subtle Slate rgba(15, 23, 42, 0.08)), zero red, soft rounded corners (18-24px), capsule pills (9999px), and consistent application across all catalog and studio pages.
---

# Certifier Studio Editorial Luxury Design DNA Standard

- **Framework**: Certifier Studio Master Design System
- **Specification**: Editorial Luxury & Full-Screen Homepage Design System
- **Release Version**: `v3.1.0` (Complete Whole-Page & Sub-Pages Unified System)

---

## 1. Core Visual DNA & Rules

1. **Strict 3-Color Closed Palette**:
   - `Foundation White`: `#ffffff` (`--bg-canvas`, `--bg-panel`) - Pure, clean, crisp white surface.
   - `Deep Charcoal`: `#0f172a` (`--text-primary`, `--border-dark`) - Master typography and high-contrast solid accents (AAA contrast).
   - `Subtle Slate`: `rgba(15, 23, 42, 0.08)` (`--border-subtle`) - Hairline borders, dividers, and card outlines.
   - Zero red colors allowed across the entire system.

2. **Full-Screen Viewport Architecture**:
   - Homepage hero sections must span `100vw` by `100vh` edge-to-edge (`margin: 0; padding: 0; border-radius: 0; overflow: hidden;`).
   - Cinematic backdrops paired with multi-stop linear gradient overlays (`linear-gradient(180deg, rgba(15, 23, 42, 0.55) 0%, rgba(15, 23, 42, 0.0) 24%, rgba(15, 23, 42, 0.0) 55%, rgba(15, 23, 42, 0.85) 100%)`).

3. **Monumental "V" Lettermark Logo**:
   - Header brand area displays **only the logo** with zero extra text or subtitles.
   - Large bold typography: `font-family: 'Space Grotesk', sans-serif; font-size: clamp(68px, 7.5vw, 96px); font-weight: 900; line-height: 0.8; letter-spacing: -0.07em; color: #ffffff; text-shadow: 0 8px 32px rgba(0, 0, 0, 0.65);`.
   - Subtle hover zoom: `transform: scale(1.06);`.

4. **Interactive Capsule Navigation Dock**:
   - Floating frosted glass capsule: `background: rgba(255, 255, 255, 0.16); backdrop-filter: blur(24px); border: 1px solid rgba(255, 255, 255, 0.28); border-radius: 9999px; padding: 8px 24px; gap: 20px; box-shadow: 0 8px 28px rgba(0, 0, 0, 0.16);`.
   - Working interactive dropdown popovers on hover/focus with smooth cubic-bezier transitions.
   - Caret icon rotation (`transform: rotate(180deg)`) on active/hover state.
   - Responsive category switching and smooth scrolling to sections (`#grid`, `#blankPresetsSection`, `#visualStageWrapper`).

5. **Right-Side Continuous Certificate Marquee**:
   - Vertical infinite scrolling track (`@keyframes winzyMarqueeScroll`) rendering randomized certificate specimen cards.
   - Cards sampled from verified local preview PNGs (`certificates/previews/`).
   - Hover pause (`animation-play-state: paused;`) allowing users to inspect and click cards to open them in the visual stage inspector (`selectTemplateById(id)`).

6. **Corner Certificate Intelligence Cluster**:
   - Bottom-left corner features detailed certificate counts: Total Templates (2,328), Master Certificates (2,137), Digital Badges (86), Transcripts & Records (60), and Vector SVGs (4,185).
   - Quick-jump capsule filter pills allowing one-click filtering.
   - Zero login, signup, or booking buttons.

---

## 2. Whole-Page Sub-Sections & Sub-Pages Transformation Standard

1. **Card & Container Geometry**:
   - **Zero Harsh Chamfers & Zero Fake Stitches**: Completely eradicate 45-degree polygon cuts, dark cyber coordinate grids, and dashed fake-leather stitching lines.
   - **Soft Modern Corners**: Main cards and modules use `border-radius: 20px - 24px`; inner cards use `border-radius: 16px - 18px`; buttons and badges use `border-radius: 9999px`.
   - **Modern Soft Shadow**: `box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04), 0 1px 3px rgba(15, 23, 42, 0.02);`.

2. **Controls & Navigation**:
   - Search bar: Encapsulated in a rounded capsule (`border-radius: 9999px`), light slate border, crisp charcoal text, embedded keyline search icon.
   - Stepper rail & category tabs: Styled with smooth capsule pills (`border-radius: 9999px`), active tabs filled with solid Deep Charcoal (`#0f172a`) and white text.

3. **Visual Stage & Inspector**:
   - Display plate: Pure white surface (`#ffffff`) with subtle hairline border and soft floating shadow.
   - Technical inspector: High-contrast header in Deep Charcoal (`#0f172a`), clean tabular parameter key-values, and rounded capsule status tags.

4. **Sub-Pages Alignment (e.g. `badge_studio.html`)**:
   - Background: Pure White canvas (`#ffffff`), zero dark radial grid.
   - Header: Inherits the prominent "V" lettermark mark and capsule navigation dock.
   - Panels & Grids: All customizer controls, color swatch buttons, live badge previews, and archive grids use rounded white card containers with delicate slate borders.
   - Zero Red: All accent highlights use Deep Charcoal (`#0f172a`) and subtle slate.
