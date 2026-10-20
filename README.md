# Certifier Credential & HD Design Template Repository

A production-ready repository containing official Certifier design templates, editable design schemas, HD backgrounds, vector elements, typography, and blank canvas configurations.

* **Live Cloudflare Production URL**: [https://certchain.shiliaiwei.workers.dev](https://certchain.shiliaiwei.workers.dev)
* **Badge Studio**: [https://certchain.shiliaiwei.workers.dev/badge_studio.html](https://certchain.shiliaiwei.workers.dev/badge_studio.html)

---

## 1. Professional Directory Architecture

```
cetif/
├── .gitignore                      # Configured with heavy media exclusions
├── README.md                       # Comprehensive system architecture & developer guide
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

## 2. Asset Integrity Standard
- **Zero Scripts / Zero Runtime Overhead**: Pure asset and schema repository.
- **Strictly Zero Emojis**: Pure typography and assets only.

---

## 3. Git Remote Disconnect & Switch Guide

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
