---
name: shiliaiwei-liquid-glass-standards
description: Authoritative design standard and architectural rules for Shiliaiwei Liquid Glass, 14 Design System UI Elements, 8 Color System Tokens, 25 Website Concepts, 9px tactile sticker button physics, strict SOLID COLORS ONLY, zero-emoji / zero-symbol / zero-signs / zero-gray / zero-shadow / zero-glow / zero-hover policy, Apple squircle app icon hero with Web Audio API chime, multi-platform implementation (Web, React, Compose, SwiftUI, Flutter), and mandatory Google Sans for Khmer.
---

# Shiliaiwei Guideline Design DNA Skill

- **Primary Production URL**: https://shiliaiwei.pages.dev
- **Cloudflare Pages Project**: `shiliaiwei`
- **Release Version**: `v2.4.0` (Solid Liquid Glass Architecture)

---

## 1. Core Architecture Directives

1. **Zero Emojis Policy (0 smileys/symbols)**:
   - Emojis (e.g., smileys, checkmarks, rockets, flames, stars, sparkles, flags) are strictly forbidden across all UI code, HTML, CSS, JavaScript, Kotlin, Swift, Dart, markdown documentation, and assistant responses.

2. **Zero Icons Policy (Pure Typography)**:
   - No icon fonts (Font Awesome, Material Symbols, Lucide), no arbitrary Unicode glyphs, and no decorative symbols.
   - Use high-contrast monospace code tokens, semantic status pills (`ACTIVE`, `PROD`, `VERIFIED`, `ENABLED`, `PENDING`), and pure typography labels.

3. **Zero Gray Policy (No Muddy/Dull Grays)**:
   - Generic dull or muddy grays (`#808080`, `#999999`, `#cccccc`) are strictly prohibited.
   - Canvas White `#FAFCFF` / `#FFFFFF` paired with deep Slate-900 typography `#0F172A`, frosted glass surfaces, and crisp slate borders.

4. **Zero Gradients Policy (100% Solid Colors Only)**:
   - Linear gradients, radial gradients, mesh gradients, and conic gradients are strictly prohibited.
   - All backgrounds, button fills, text colors, badges, and borders must use 100% single solid color tokens.

5. **Zero Mix Color Policy**:
   - Each element or component must use exactly ONE single solid palette color token without mixed color fills or multi-color blend overlays.

6. **Strict Closed Palette (8 of 8 Core Tokens)**:
   - NEVER use, invent, or introduce colors outside the explicit `:root` tokens.
   - Permitted Closed Palette:
     - `01. Canvas White`: `#FAFCFF` (`--bg-main`) - High-contrast canvas foundation.
     - `02. Slate-900`: `#0F172A` (`--text-main`) - Master typography & solid borders (16.8:1 AAA contrast).
     - `03. Primary Emerald`: `#10B981` (`--primary`) - Core brand interactive actions and confirmations.
     - `04. Deep Emerald`: `#059669` (`--primary-dark`) - 3D depth extrusion and high-contrast text.
     - `05. Eager Green`: `#58CC02` (`--color-eager-green`) - High-energy CTA buttons.
     - `06. Spark Blue`: `#1CB0F6` (`--color-spark-blue`) - Secondary interactive accents.
     - `07. Accent Cyan`: `#0891B2` (`--accent-cyan`) - Release tags and code chips.
     - `08. Accent Crimson`: `#FF0050` (`--accent-crimson`) - Critical alerts and danger states.

7. **Zero Blur Shadow & Zero Glow Policy**:
   - Blurry drop shadows and ambient glow orbs are eliminated. All cards, buttons, docks, inputs, and modals use pure crisp solid borders (`border: 1px solid rgba(0,0,0,0.10); border-top: 1px solid #FFFFFF; box-shadow: none;`).

8. **Zero Hover Style Policy (No Floating/Lifting)**:
   - No hover transforms, floating lifts (`translateY`), shadow alterations, or background swaps. Layouts remain static and stable until directly clicked or activated.

9. **Mandatory Google Sans for Khmer & 9px Tactile Sticker Button Physics**:
   - All Khmer text strictly uses `'Google Sans', 'Kantumruy Pro', sans-serif` with line-height `1.45`-`1.50` to prevent diacritic clipping.
   - English typography strictly uses `'Ubuntu', sans-serif` or `'Outfit', sans-serif`.
   - Standard button radius: **`9px`** (`var(--radius-btn)`), compact: **`6px`**.
   - 3D bottom shadow depth (`box-shadow: 0 4px 0 <depth-color>`) with active click compression (`transform: translateY(3px); box-shadow: 0 1px 0 <depth-color>;`).

10. **Apple iPhone & macOS Desktop App Icon Hero**:
    - Outer Squircle Frame: `118px x 118px` (`100px x 100px` mobile), `border-radius: 28px`, solid emerald `#10B981` with crisp `1.5px solid rgba(0,0,0,0.14)` outline (zero white rim).
    - Inner Apple Geometry Guide Grid: Concentric circle and crosshairs.
    - 3D Elevated Center Plate: `72px x 72px`, `#059669`, `border-radius: 16px`, `border-top: 2px solid #FFFFFF`.
    - Emblem: Pure white Khmer **"វី"** typography (`font-size: 3.1rem; font-weight: 900`).
    - Audio Synthesis: Web Audio API crystal glass chime sound effect on tap.

11. **14 Core UI Elements**:
    - Tactile Buttons, Radio, Searchbar, Tooltip, Modal, Loading Skeleton, Toggle Switch, Progress Bar, Avatar Stack, Tabs, Range Slider, Code Chip, Status Badge, UI Table.

12. **Concise 2-3 Words Button Text Mandate**:
    - Every interactive button across all applications, modules, and dialogs must strictly use **two or three words maximum** (`Verify Code`, `Resend Code`, `Save Settings`, `Create Key`, `Export CSV`, `Next Step`, `Back Step`, `Confirm Payment`, `Send Message`, `Invite User`, `Delete Key`, `Switch KM`, `Copy Tokens`, `Launch Editor`).

13. **Single-View Studio Architecture (Zero Forced Scrolling)**:
    - 3 dedicated views (`Visual Identity`, `UI Elements`, `Web App Suite`) selectable in 1 click from the top floating dock menu without long vertical scrolling.

---

## 2. Closed 8-Token System Registry

| No. | Token Name | Hex Code | CSS Variable | Semantic Role | WCAG Contrast |
|---|---|---|---|---|---|
| 01 | Canvas White | `#FAFCFF` | `--bg-main` | High-contrast canvas foundation | 16.8:1 (AAA Foundation) |
| 02 | Slate-900 Typography | `#0F172A` | `--text-main` | Master typography & solid borders | 16.8:1 (AAA Master) |
| 03 | Primary Emerald | `#10B981` | `--primary` | Core brand interactive actions & confirmations | 4.5:1 (AA Large/UI) |
| 04 | Deep Emerald | `#059669` | `--primary-dark` | 3D depth extrusion & high-contrast text | 7.1:1 (AAA) |
| 05 | Eager Green | `#58CC02` | `--color-eager-green` | High-energy CTA buttons | 9.8:1 (AAA on Dark) |
| 06 | Spark Blue | `#1CB0F6` | `--color-spark-blue` | Secondary interactive accents | 8.4:1 (AAA on Dark) |
| 07 | Accent Cyan | `#0891B2` | `--accent-cyan` | Release tags & code chips | 4.6:1 (AA) |
| 08 | Accent Crimson | `#FF0050` | `--accent-crimson` | Critical alerts & danger states | 4.5:1 (AA) |

---

## 3. The 14 Core UI Elements Specifications

### 1. Tactile Buttons (`.btn`)
- **Primary CTA (`.btn-primary`)**: `#10B981` fill, `box-shadow: 0 4px 0 #059669`, color `#FFFFFF`.
- **Eager Sticker (`.btn-eager`)**: `#58CC02` fill, `box-shadow: 0 4px 0 #059669`, color `#FFFFFF`.
- **Spark Blue (`.btn-spark`)**: `#1CB0F6` fill, `box-shadow: 0 4px 0 #0891B2`, color `#FFFFFF`.
- **Accent Crimson (`.btn-crimson`)**: `#FF0050` fill, `box-shadow: 0 4px 0 #0F172A`, color `#FFFFFF`.
- **Canvas White (`.btn-white`)**: `#FAFCFF` fill, `border: 1px solid #0F172A`, `box-shadow: 0 4px 0 #0F172A`, color `#0F172A`.
- **Active Press State**: `transform: translateY(3px); box-shadow: 0 1px 0 <depth-color>;`.
- **Radius**: Standard `9px`, compact `6px`.

### 2. Radio Selection (`.ui-radio`)
- Unchecked: `border: 2px solid rgba(15,23,42,0.30); background: #FFFFFF; border-radius: 50%;`.
- Checked: `border: 6px solid #10B981; background: #FFFFFF; border-radius: 50%;`.

### 3. Searchbar (`.search-input`)
- Surface: `#FFFFFF`, `border: 1px solid #0F172A; border-radius: 9px; padding: 10px 14px;`.
- Trailing shortcut badge: Monospace `CMD+K`, `#FAFCFF` background, `border: 1px solid #0F172A; border-radius: 4px; padding: 2px 6px;`.
- Tap-cursor auto-clear: Pre-filled production value clears on focus and restores on empty blur.

### 4. Tooltip (`.ui-tooltip`)
- Background: Slate-900 (`#0F172A`), `border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 6px 10px;`.
- Typography: `#FAFCFF`, `font-size: 0.75rem; font-weight: 700;`.

### 5. Modal Dialog (`.ui-modal`)
- Backdrop: `rgba(15, 23, 42, 0.45)` with `backdrop-filter: blur(24px)`.
- Card: Canvas White (`#FAFCFF`), `border: 2px solid #0F172A; border-radius: 20px; padding: 24px; box-shadow: 0 4px 0 #0F172A;`.
- Actions: 9px tactile buttons for Confirm and Cancel (2-3 words).

### 6. Loading Skeleton & Spinner
- Spinner: `24px` diameter, `border: 3px solid rgba(16,185,129,0.20); border-top-color: #10B981; animation: spin 0.8s linear infinite;`.
- Skeleton Line: `height: 10px; border-radius: 4px; background: rgba(15,23,42,0.08);`.

### 7. Toggle Switch (`.ui-toggle`)
- Track: `46px x 26px`, `background: #E2E8F0; border: 1px solid #0F172A; border-radius: 9999px;`.
- Active Track: `background: #10B981; border-color: #059669;`.
- Thumb: `20px x 20px`, `#FFFFFF`, `border-radius: 50%; border: 1px solid #0F172A;`.

### 8. Progress Bar (`.progress-bar`)
- Track: `height: 8px; background: #FAFCFF; border: 1px solid #0F172A; border-radius: 9999px; overflow: hidden;`.
- Fill: `#10B981` (or `#58CC02` / `#1CB0F6`), `height: 100%; border-radius: 9999px;`.

### 9. Avatar & Stack (`.avatar-stack`)
- Image: `border-radius: 50%; border: 2px solid #FFFFFF; object-fit: cover;`.
- Active Dot: `11px` diameter, `#10B981`, `border: 2px solid #FFFFFF;`.
- Stack: `-10px` negative margin with `+N` count badge in pure monospace.

### 10. Segmented Tabs (`.segmented-tabs`)
- Pill container: `#FAFCFF`, `border: 1px solid #0F172A; border-radius: 9999px; padding: 3px; display: inline-flex; gap: 4px;`.
- Active Tab: `#0F172A` background, `#FAFCFF` text, `border-radius: 9999px; font-weight: 700;`.
- Inactive Tab: `transparent` background, `#0F172A` text.

### 11. Range Slider (`.ui-range`)
- Track: `height: 6px; background: #E2E8F0; border-radius: 9999px; border: 1px solid #0F172A;`.
- Thumb: `18px x 18px`, `#10B981`, `border: 2px solid #0F172A; border-radius: 50%;`.

### 12. Code Chip (`.code-chip`)
- Monospace font, `background: #FAFCFF; border: 1px solid #0F172A; border-radius: 4px; padding: 3px 8px; color: #0F172A; font-weight: 700;`.

### 13. Status Badge (`.badge`)
- Pure monospace semantic status pills with solid color fills and zero emoji:
  - Active: `#10B981` fill, `#FAFCFF` text, `border: 1px solid #059669`.
  - Info / Tag: `#0891B2` fill, `#FAFCFF` text, `border: 1px solid #0F172A`.
  - Alert / Danger: `#FF0050` fill, `#FAFCFF` text, `border: 1px solid #0F172A`.
  - Network / Secondary: `#1CB0F6` fill, `#FAFCFF` text, `border: 1px solid #0F172A`.

### 14. UI Table (`.ui-table`)
- High-contrast tabular layout with 100% solid styling.
- Header: `#FAFCFF` background, `border-bottom: 2px solid #0F172A; font-family: monospace; font-size: 11px; font-weight: 800;`.
- Rows: `border-bottom: 1px solid #0F172A; padding: 12px 16px; font-size: 13px;`.

---

## 4. Web Audio API Crystal Glass Chime Synthesis

```javascript
function playMacNotificationSound() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    if (ctx.state === 'suspended') ctx.resume();

    const now = ctx.currentTime;

    // Primary E6 -> A6 glass tone
    const osc1 = ctx.createOscillator();
    const gain1 = ctx.createGain();
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(1318.51, now);
    osc1.frequency.exponentialRampToValueAtTime(1760.00, now + 0.08);
    gain1.gain.setValueAtTime(0.32, now);
    gain1.gain.exponentialRampToValueAtTime(0.0001, now + 0.45);
    osc1.connect(gain1);
    gain1.connect(ctx.destination);

    // High crystal shimmer overtone E7
    const osc2 = ctx.createOscillator();
    const gain2 = ctx.createGain();
    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(2637.02, now);
    gain2.gain.setValueAtTime(0.18, now);
    gain2.gain.exponentialRampToValueAtTime(0.0001, now + 0.35);
    osc2.connect(gain2);
    gain2.connect(ctx.destination);

    // Tactile bass pop
    const osc3 = ctx.createOscillator();
    const gain3 = ctx.createGain();
    osc3.type = 'triangle';
    osc3.frequency.setValueAtTime(220, now);
    osc3.frequency.exponentialRampToValueAtTime(110, now + 0.06);
    gain3.gain.setValueAtTime(0.22, now);
    gain3.gain.exponentialRampToValueAtTime(0.0001, now + 0.08);
    osc3.connect(gain3);
    gain3.connect(ctx.destination);

    osc1.start(now);
    osc2.start(now);
    osc3.start(now);
    osc1.stop(now + 0.45);
    osc2.stop(now + 0.35);
    osc3.stop(now + 0.08);
  } catch (err) {}
}
```

---

## 5. Multi-Platform Implementation Blueprints

### Web & Next.js CSS Tokens
```css
:root {
  --primary: #10B981;
  --primary-dark: #059669;
  --color-eager-green: #58CC02;
  --color-spark-blue: #1CB0F6;
  --accent-cyan: #0891B2;
  --accent-crimson: #FF0050;
  --bg-main: #FAFCFF;
  --text-main: #0F172A;
  --radius-btn: 9px;
}
```

### Android Jetpack Compose Tokens
```kotlin
object ShiliaiweiTokens {
    val Primary = Color(0xFF10B981)
    val PrimaryDark = Color(0xFF059669)
    val EagerGreen = Color(0xFF58CC02)
    val SparkBlue = Color(0xFF1CB0F6)
    val AccentCyan = Color(0xFF0891B2)
    val AccentCrimson = Color(0xFFFF0050)
    val CanvasWhite = Color(0xFFFAFCFF)
    val Slate900 = Color(0xFF0F172A)
    val ButtonCornerRadius = 9.dp
}
```

### iOS SwiftUI Tokens
```swift
struct ShiliaiweiTokens {
    static let primary = Color(hex: "#10B981")
    static let primaryDark = Color(hex: "#059669")
    static let eagerGreen = Color(hex: "#58CC02")
    static let sparkBlue = Color(hex: "#1CB0F6")
    static let accentCyan = Color(hex: "#0891B2")
    static let accentCrimson = Color(hex: "#FF0050")
    static let canvasWhite = Color(hex: "#FAFCFF")
    static let slate900 = Color(hex: "#0F172A")
    static let buttonRadius: CGFloat = 9
}
```

### Flutter / Dart Tokens
```dart
class ShiliaiweiTokens {
  static const primary = Color(0xFF10B981);
  static const primaryDark = Color(0xFF059669);
  static const eagerGreen = Color(0xFF58CC02);
  static const sparkBlue = Color(0xFF1CB0F6);
  static const accentCyan = Color(0xFF0891B2);
  static const accentCrimson = Color(0xFFFF0050);
  static const canvasWhite = Color(0xFFFAFCFF);
  static const slate900 = Color(0xFF0F172A);
  static const buttonRadius = 9.0;
}
```
