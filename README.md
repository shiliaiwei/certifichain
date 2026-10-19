# Certifier Local Studio & HD Design Template Repository

A production-ready local studio, offline repository, and interactive catalog viewer for official Certifier design templates, editable design schemas, HD backgrounds, vector elements, typography, and blank canvas configurations.

---

## 1. Professional Directory Architecture

```
cetif/
├── .gitignore                      # Configured with heavy media exclusions & Python caches
├── README.md                       # Comprehensive system architecture & developer guide
├── index.html                      # Root compiled studio viewer (offline production ready)
├── public/                         # Public web server distribution root
│   └── index.html                  # Standard web distribution entry point
├── src/                            # Application Source Code
│   ├── components/                 # Modular UI Components
│   │   ├── TopBarSkeuomorphic.html # 3D Textured Leather & Banknote Guilloche Top Bar
│   │   ├── CyberGridControls.html  # .TECH Domains Split Search & Stepper Tabs
│   │   ├── BlankPresetsGrid.html   # 18px Chamfered Blank Canvas Dimension Cards
│   │   └── KeylineIcons.html       # Keyline SVG Icons System Symbol Definitions
│   ├── styles/                     # CSS Design Systems
│   │   ├── skeuomorphic_leather.css# 3D Royal Purple Leather, Stitching & Guilloche
│   │   └── cyber_grid.css          # .TECH Domains Obsidian #08090b & 38px Grid
│   └── utils/                      # Core Data Pipeline & Automation Utilities
│       ├── build_catalog_html.py   # Master Catalog Builder & UI Compiler
│       ├── organize_templates_as_is.py
│       ├── save_editor_specs.py
│       ├── download_certificates.py
│       ├── download_resources.py
│       └── fetch_remaining_certificates.py
├── scripts/                        # Standard CLI Entry Points & Tasks
│   ├── build.py                    # Rebuilds catalog HTML and public distribution
│   ├── organize.py                 # Organizes templates into categorized folder structure
│   ├── specs.py                    # Validates and regenerates editor presets & specs
│   └── run_tests.py                # Automated test runner
├── tests/                          # Automated Test Suite (Unit & Integration)
│   ├── test_catalog_integrity.py   # Validates all catalog JSON schemas & counts
│   ├── test_editor_specifications.py # Validates canvas presets & typography
│   ├── test_directory_structure.py # Validates standard directories & clean root
│   └── test_build_pipeline.py      # Validates build execution & design tokens
├── catalogs/                       # Data / Master Catalog Indexes
│   ├── catalog_all.json            # Master index of all 2,328 templates
│   ├── certificates.json           # 2,137 certificate templates
│   ├── badges.json                 # 86 badge templates
│   ├── transcripts.json            # 45 transcript templates
│   ├── training_records.json       # 25 training record templates
│   ├── assessments.json            # 25 assessment templates
│   ├── letters.json                # 10 formal credential letters
│   └── extracted_elements.json     # 130 vector element definitions
├── editor_specifications/          # Editor Specifications & Canvas Presets
│   ├── blank_canvas_presets.json   # Exact dimensions (mm, inches, 96 DPI, 300 DPI)
│   ├── dynamic_attributes.json     # Dynamic placeholder tags ([recipient.name], etc.)
│   ├── typography_and_fonts.json   # 58 Google Fonts and text presets
│   └── qr_code_specs.json          # QR code rendering & dynamic URL specs
├── email_templates/                # Credential Delivery Email Templates
│   └── email_templates.json        # 5 email notification templates
├── elements/                       # 130 Vector SVG Assets
│   ├── bases/                      # 42 crests, shields, badge containers
│   ├── graphics/                   # 46 seals, laurel wreaths, stars, ribbons, stamps
│   ├── ribbons/                    # 30 banners, award sashes, curved ribbons
│   └── shapes/                     # 12 solid and outlined geometric forms
├── certificates/                   # 2,137 templates (backgrounds, json, previews)
├── badges/                         # 86 square badge templates
├── transcripts/                    # 45 academic & CPD transcript templates
├── training_records/               # 25 professional training record templates
├── assessments/                    # 25 assessment & skills evaluation templates
├── letters/                        # 10 formal credential & verification letter templates
└── Templates/                      # Hardlinked categorized folder hierarchy
```

---

## 2. Design System Architecture

### A. Navigation Bar: 3D Skeuomorphic Textured Leather & Banknote Guilloche
- **Visual Philosophy**: High-tactile physical craftsmanship, luxury leather goods, and central bank security engraving.
- **Color Palette**:
  - Royal Purple Gradient: Highlight `#6b22a8`, body `#4c1482`, deep base `#260742`.
  - Light Lavender Thread Stitching: `#e9d5ff` (`stroke-dasharray="4 4"`, `stroke-width="1.25"`, drop shadow).
  - Satin Card Finishes:
    - USD Emerald Green: `#059669`
    - KHR Royal Violet: `#a855f7`
    - WEI Sky Blue: `#0098ea`
- **3-Tier Pocket Assembly**:
  1. *Back Leather Sleeve*: Outer container with `38px` corner radius, deep ambient occlusion shadow (`0 24px 48px -12px rgba(45, 10, 80, 0.55)`), and dual-frequency procedural micro-radial pebble grain overlay.
  2. *Inserted Physical Card*: Credit-card proportioned satin card peeking upward from inside the sleeve slot, featuring an angled specular light sheen and mathematical spirograph banknote guilloche watermark. Houses corporate typographic badge (`SHILIAI [WEI]`) and cryptographic address pill (`0x71C84...F29A // CERT-VAULT`).
  3. *Front Overlapping Flap*: Leather front lip overlapping the lower card with a scooped curved edge (`M 2 2 Q 180 8 360 2`), top specular rim highlight, and physical tactile toggle switches.
- **Strictly No Emojis**: Pure typography and vector keyline icons.

### B. Main Canvas & UI: .TECH Domains Cyber-Grid & Chamfered
- **Visual Philosophy**: Dark technical neo-brutalism, terminal precision, and CNC hardware aesthetic.
- **Canvas Foundation**: Deep obsidian black `#08090b` with repeating 38px coordinate square grid rendered via linear gradients (`rgba(255, 255, 255, 0.035)`).
- **Color Tokens**:
  - Carbon panels: `#0d0e11`
  - Input surfaces: `rgb(15, 16, 18)`
  - Tactical mint/sage accent: `#d2e2b9` (hover `#e0eed0`)
  - Tech orange: `#f25a38`
  - Border divider: `rgba(255, 255, 255, 0.06)`
- **Geometric Cuts**: Precision 45-degree chamfer cuts on top-right corners:
  - `18px`: Stepper tabs, hero section, blank canvas cards.
  - `14px`: Search input groups, primary CTA buttons, template cards.
  - `12px`: Secondary tags, pills, category filters.
- **Continuous 1px Border Rule**: Nested inset polygon architecture (`.chamfer-wrapper` + `.chamfer-inner`) maintaining a crisp 1px stroke along diagonal cuts.
- **Typography**: Google Fonts `Space Grotesk` (display titles, counts, code, step numerals) paired with `DM Sans` (interface labels and body copy).
- **Keyline Icons System**: Standardized 24x24 outline vector icons with 1.8px stroke and two-tone tint fill.

---

## 3. Developer & Build Workflows

### Build Catalog Interface
To regenerate `index.html` and `public/index.html`:
```bash
python3 scripts/build.py
# or
python3 build_catalog_html.py
```

### Run Automated Tests
To run the automated unit and integration test suite:
```bash
python3 scripts/run_tests.py
# or
python3 -m unittest discover -v tests
```

### Organize Templates into Subcategories
```bash
python3 scripts/organize.py
```

---

## 4. Git Remote Disconnect & Switch Guide

To disconnect from an existing remote without deleting local files and push to a new repository:

1. **Check Current Remotes**:
   ```bash
   git remote -v
   ```

2. **Disconnect Old Remote (Does not delete any files)**:
   ```bash
   git remote remove origin
   ```

3. **Attach New Remote Repository**:
   ```bash
   git remote add origin <YOUR_NEW_REPO_URL>
   ```

4. **Verify Remote Connection**:
   ```bash
   git remote -v
   ```

5. **Push to New Repository (When Ready)**:
   ```bash
   git push -u origin refactor/standard-structure-and-redesign
   # or merge into main and push main:
   # git checkout main && git merge refactor/standard-structure-and-redesign
   # git push -u origin main
   ```

---

## 5. Document Dimensions Reference

| Document Type | Paper Size | Orientation | Dimensions (96 DPI) | High-Res / Print (300 DPI) | Aspect Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Certificate** | A4 | Landscape | 1123 × 794 px | 3508 × 2480 px (2000 × 1414 HD) | 1.414 (√2) |
| **Certificate** | A4 | Portrait | 794 × 1123 px | 2480 × 3508 px (1414 × 2000 HD) | 0.707 (1/√2) |
| **Certificate** | US Letter | Landscape | 1056 × 816 px | 3300 × 2550 px | 1.294 (11:8.5) |
| **Certificate** | US Letter | Portrait | 816 × 1056 px | 2550 × 3300 px | 0.772 (8.5:11) |
| **Badge** | Custom | Square | 512 × 512 px (viewport) | 1000 × 1000 px (vector) | 1:1 |
| **Transcript** | A4 | Landscape | 1123 × 794 px | 3508 × 2480 px | 1.414 |
| **Training Record** | A4 | Landscape | 1123 × 794 px | 3508 × 2480 px | 1.414 |
| **Assessment** | A4 | Landscape | 1123 × 794 px | 3508 × 2480 px | 1.414 |
| **Letter** | A4 | Portrait | 794 × 1123 px | 2480 × 3508 px | 0.707 |
