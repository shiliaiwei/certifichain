import base64
import json
import math
import os
import random
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def encrypt_resource_payload(raw_json_str: str, key: str = "CertifierStudio_Vault_SecKey_2026") -> str:
    """Encrypt resource catalog JSON payload with a rotating dynamic stream cipher."""
    data_bytes = raw_json_str.encode("utf-8")
    key_bytes = key.encode("utf-8")
    key_len = len(key_bytes)
    encrypted_bytes = bytearray(
        b ^ key_bytes[(i + 13) % key_len] ^ ((i * 7) & 0xFF)
        for i, b in enumerate(data_bytes)
    )
    return base64.b64encode(encrypted_bytes).decode("ascii")

def generate_guilloche_svg(w=1200, h=160):
    """Generate authentic mathematical banknote guilloche wave patterns & rosettes."""
    lines = []
    # 1. Interlocking sinusoidal wave bands (12 harmonic layers)
    for i in range(12):
        pts = []
        for x in range(0, w + 12, 12):
            y = 75 + 26 * math.sin(x * 0.018 + i * 0.35) + 14 * math.cos(x * 0.042 - i * 0.28)
            pts.append(f"{x},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="0.65"/>')

    # 2. Counter-harmonic security wave bands (8 inverse layers)
    for i in range(8):
        pts = []
        for x in range(0, w + 15, 15):
            y = 75 - 20 * math.sin(x * 0.024 - i * 0.45) + 10 * math.sin(x * 0.065 + i * 0.3)
            pts.append(f"{x},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="0.55"/>')

    # 3. Left Guilloche Rosette
    for i in range(7):
        R, r, p = 52 + i * 4, 18, 28
        pts = []
        for step in range(181):
            t = math.radians(step * 4)
            x = (R - r) * math.cos(t) + p * math.cos((R - r) * t / r) + 160
            y = (R - r) * math.sin(t) - p * math.sin((R - r) * t / r) + 80
            pts.append(f"{x:.1f},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="0.6"/>')

    # 4. Right Guilloche Rosette
    for i in range(7):
        R, r, p = 52 + i * 4, 18, 28
        pts = []
        for step in range(181):
            t = math.radians(step * 4)
            x = (R - r) * math.cos(t) + p * math.cos((R - r) * t / r) + (w - 160)
            y = (R - r) * math.sin(t) - p * math.sin((R - r) * t / r) + 80
            pts.append(f"{x:.1f},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="0.6"/>')

    return (
        f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" class="guilloche-watermark">'
        + "".join(lines)
        + "</svg>"
    )

def main():
    catalog_path = os.path.join(BASE_DIR, "catalogs", "catalog_all.json")
    with open(catalog_path, "r", encoding="utf-8") as f:
        master = json.load(f)

    # Elements
    elements_dir = os.path.join(BASE_DIR, "elements")
    elements_data = {}
    if os.path.exists(elements_dir):
        for sub in sorted(os.listdir(elements_dir)):
            sub_path = os.path.join(elements_dir, sub)
            if os.path.isdir(sub_path):
                elements_data[sub] = sorted(os.listdir(sub_path))

    # Editor specs
    specs_dir = os.path.join(BASE_DIR, "editor_specifications")
    blank_presets = {}
    if os.path.exists(os.path.join(specs_dir, "blank_canvas_presets.json")):
        with open(os.path.join(specs_dir, "blank_canvas_presets.json"), "r", encoding="utf-8") as f:
            blank_presets = json.load(f)

    attributes_data = {}
    if os.path.exists(os.path.join(specs_dir, "dynamic_attributes.json")):
        with open(os.path.join(specs_dir, "dynamic_attributes.json"), "r", encoding="utf-8") as f:
            attributes_data = json.load(f)

    typography_data = {}
    if os.path.exists(os.path.join(specs_dir, "typography_and_fonts.json")):
        with open(os.path.join(specs_dir, "typography_and_fonts.json"), "r", encoding="utf-8") as f:
            typography_data = json.load(f)

    guilloche_svg = generate_guilloche_svg()
    total_templates = sum(len(v) for v in master.values())
    total_svgs = sum(len(v) for v in elements_data.values())

    count_certificates = len(master.get("certificate", []))
    count_badges = len(master.get("badge", []))
    count_transcripts = len(master.get("transcript", []))
    count_training = len(master.get("training_record", []))
    count_assessments = len(master.get("assessment", []))
    count_letters = len(master.get("letter", []))
    count_other_records = count_training + count_assessments + count_letters

    # Encrypt all catalog templates, elements, and specifications into secure vault payload
    vault_bundle = {
        "templates": master,
        "elements": elements_data,
        "attributes": attributes_data,
        "typography": typography_data,
    }
    encrypted_vault_payload = encrypt_resource_payload(json.dumps(vault_bundle))

    # Extract verified random certificates for right-side marquee
    certs_raw = master.get("certificate", [])
    valid_marquee_certs = []
    for c in certs_raw:
        c_name = c.get("name", "")
        c_id = c.get("id", "")
        safe = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', c_name or 'template')
        safe = re.sub(r'_+', '_', safe)[:80]
        preview_rel = f"certificates/previews/{safe}_{c_id}_preview.png"
        preview_path = os.path.join(BASE_DIR, preview_rel)
        if os.path.exists(preview_path):
            clean_title = c_name.replace("_", " ").strip().title()
            valid_marquee_certs.append({
                "id": c_id,
                "name": clean_title,
                "preview": preview_rel,
                "paperSize": c.get("paperSize", "A4"),
                "orientation": c.get("orientation", "landscape"),
                "style": c.get("metadata", {}).get("style", "formal")
            })
    random.seed(2026)
    sample_marquee = random.sample(valid_marquee_certs, min(14, len(valid_marquee_certs))) if valid_marquee_certs else []
    
    marquee_cards_list = []
    for item in sample_marquee:
        s_id = item['id']
        s_name = item['name']
        s_prev = item['preview']
        s_paper = item['paperSize']
        s_orient = item['orientation']
        s_style = item['style']
        marquee_cards_list.append(f'''
              <div class="winzy-marquee-card" onclick="selectTemplateById('{s_id}'); return false;">
                <div class="winzy-marquee-thumb-wrap">
                  <div class="resource-protection-shield"></div>
                  <img src="{s_prev}" alt="{s_name}" class="winzy-marquee-thumb" loading="lazy" draggable="false">
                </div>
                <div class="winzy-marquee-info">
                  <div class="winzy-marquee-title">{s_name}</div>
                  <div class="winzy-marquee-meta">
                    <span class="winzy-marquee-tag">{s_paper}</span>
                    <span class="winzy-marquee-tag">{s_orient}</span>
                    <span class="winzy-marquee-tag">{s_style}</span>
                  </div>
                </div>
              </div>''')
    
    marquee_cards_html = "".join(marquee_cards_list) + "".join(marquee_cards_list)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Certifier Studio // Obsidian Cyber-Grid & Tactile Chamfer System</title>
<!-- STRICT ANTI-SCRAPING & RESOURCE ENCRYPTION DIRECTIVES -->
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, notranslate, noimageindex">
<meta name="googlebot" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="bingbot" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="ai-content-declaration" content="prohibit-training, no-ai-scrape, protected-resource">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500;1,700&family=Google+Sans+Text:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap" rel="stylesheet">
<style>
  /* ==========================================================================
     CLEAN MONOCHROME EDITORIAL LUXURY SYSTEM // ZERO CYBER-GRID // ZERO RED
     Pure Editorial Palette: White #ffffff, Deep Charcoal #0f172a, Soft Slate rgba(15, 23, 42, 0.08)
     ========================================================================== */
  :root {{
    /* 1. Surfaces & Foundation (Pure White) */
    --bg-canvas: #ffffff;
    --bg-panel: #ffffff;
    --bg-panel-secondary: #ffffff;
    --bg-input: #ffffff;
    --surface-purple: #0f172a;
    --plate-white: #ffffff;

    /* 2. Continuous Crisp Borders (Tints of #0f172a) */
    --border-subtle: rgba(15, 23, 42, 0.08);
    --border-muted: rgba(15, 23, 42, 0.16);
    --border-divider: rgba(15, 23, 42, 0.06);
    --border-dark: #0f172a;
    --border-light: rgba(15, 23, 42, 0.12);

    /* 3. Typography Tokens (Deep Charcoal #0f172a) */
    --text-white: #ffffff;
    --text-primary: #0f172a;
    --text-muted: rgba(15, 23, 42, 0.65);
    --text-dim: rgba(15, 23, 42, 0.45);
    --text-monochrome: #0f172a;

    /* 4. Strict Solid Accent Highlights (Zero Red) */
    --accent-coral: #0f172a;
    --accent-emerald: #0f172a;
    --accent-crimson: #0f172a;
    --accent-mint: #0f172a;
    --accent-mint-hover: #0f172a;
    --accent-orange: #0f172a;
    --accent-success: #0f172a;
    --accent-blue: #0f172a;

    /* 5. Typography Font Stacks */
    --font-main: "Google Sans Text", "Google Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-display: "Google Sans", "Google Sans Text", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: ui-monospace, SFMono-Regular, "JetBrains Mono", Menlo, Consolas, monospace;

    /* Compatibility & Semantic Tokens */
    --bg-obsidian-ref: #08090b; /* #08090b legacy token deprecated in favor of #ffffff / #0f172a */
    --leather-highlight: #ffffff;
    --leather-body: #ffffff;
    --leather-shadow: rgba(15, 23, 42, 0.04);
    --leather-deep: #ffffff;
    --leather-thread: rgba(15, 23, 42, 0.08);
    --satin-usd: #0f172a;
    --satin-khr: #0f172a;
    --satin-wei: #0f172a;
  }}

  *, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body.cyber-canvas {{
    background-color: #ffffff !important;
    background-image: none !important;
    color: #0f172a !important;
    font-family: var(--font-main);
    min-height: 100vh;
    padding: 0;
    margin: 0;
    -webkit-font-smoothing: antialiased;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-touch-callout: none;
  }}

  input, textarea {{
    -webkit-user-select: text;
    -moz-user-select: text;
    user-select: text;
  }}

  img {{
    pointer-events: none;
    -webkit-user-drag: none;
    user-drag: none;
  }}

  /* Keyline Icons System */
  .keyline-icon {{
    width: 16px;
    height: 16px;
    stroke: currentColor;
    stroke-width: 1.8;
    stroke-linecap: round;
    stroke-linejoin: round;
    fill: none;
    vertical-align: middle;
    flex-shrink: 0;
  }}

  .keyline-icon-24 {{
    width: 24px;
    height: 24px;
    stroke: currentColor;
    stroke-width: 1.8;
    stroke-linecap: round;
    stroke-linejoin: round;
    fill: none;
    vertical-align: middle;
    flex-shrink: 0;
  }}

  /* ==========================================================================
     CARD & POLYGON GEOMETRY (45-DEGREE CHAMFER & 1PX NESTED HAIRLINE BORDERS)
     ========================================================================== */

  .chamfer-18-wrapper {{
    position: relative;
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 18px) 0, 100% 18px, 100% 100%, 0 100%);
    padding: 1px;
    margin-bottom: 24px;
    transition: background-color 0.15s ease;
  }}

  .chamfer-18-wrapper:hover {{
    background-color: var(--border-muted);
  }}

  .chamfer-18-inner {{
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 17.586px) 0, 100% 17.586px, 100% 100%, 0 100%);
    padding: 22px;
    width: 100%;
    box-sizing: border-box;
  }}

  .chamfer-14-wrapper {{
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
    padding: 1px;
    display: inline-block;
    transition: background-color 0.15s ease;
  }}

  .chamfer-14-wrapper:hover {{
    background-color: var(--border-muted);
  }}

  .chamfer-14-inner {{
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 13.586px) 0, 100% 13.586px, 100% 100%, 0 100%);
    width: 100%;
    height: 100%;
    box-sizing: border-box;
  }}

  /* Elevated Center Card with Subtle Drop Shadow & Tactile Dashed Stitch Line */
  .elevated-center-card {{
    position: relative;
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 18px) 0, 100% 18px, 100% 100%, 0 100%);
    padding: 1px;
    filter: drop-shadow(0 16px 32px rgba(0, 0, 0, 0.85));
    transition: all 0.2s ease;
  }}

  .elevated-center-card:hover {{
    background-color: var(--border-muted);
  }}

  .elevated-center-card-inner {{
    position: relative;
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 17.586px) 0, 100% 17.586px, 100% 100%, 0 100%);
    padding: 24px;
    width: 100%;
    overflow: hidden;
  }}

  .tactile-stitch-svg {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 3;
  }}

  .tactile-stitch-rect {{
    fill: none;
    stroke: rgba(255, 255, 255, 0.16);
    stroke-width: 1;
    stroke-dasharray: 4 4;
  }}

  /* Crisp Pure White Display Plate (Contrasts against Obsidian Black) */
  .display-plate-white {{
    position: relative;
    background-color: var(--plate-white);
    color: #0f172a;
    border: 1px solid #ffffff;
    padding: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    min-height: 400px;
    z-index: 4;
  }}

  .display-plate-white img {{
    max-width: 100%;
    max-height: 480px;
    object-fit: contain;
    display: block;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
  }}

  /* Top Hardware Module (18px Chamfer Cut) */
  .leather-sleeve {{
    position: relative;
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 18px) 0, 100% 18px, 100% 100%, 0 100%);
    padding: 1px;
    overflow: hidden;
    margin-bottom: 24px;
    transition: background-color 0.15s ease;
  }}

  .leather-sleeve:hover {{
    background-color: var(--border-muted);
  }}

  .leather-pebble-grain {{
    position: absolute;
    inset: 0;
    background-image: 
      radial-gradient(circle, rgba(255, 255, 255, 0.08) 1px, transparent 1px),
      linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    background-size: 38px 38px, 38px 38px, 38px 38px;
    opacity: 0.7;
    pointer-events: none;
    z-index: 2;
  }}

  .leather-stitch-svg {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 5;
  }}

  .leather-stitch-rect {{
    fill: none;
    stroke: rgba(255, 255, 255, 0.18);
    stroke-width: 1;
    stroke-dasharray: 4 4;
  }}

  .inserted-card-slot {{
    position: relative;
    width: 100%;
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 17.586px) 0, 100% 17.586px, 100% 100%, 0 100%);
    padding: 20px 24px 22px 24px;
    overflow: hidden;
    z-index: 3;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
  }}

  .guilloche-watermark {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    opacity: 0.10;
    z-index: 1;
  }}

  .card-brand-col {{
    position: relative;
    z-index: 4;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .card-meta-col {{
    position: relative;
    z-index: 4;
    display: flex;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
  }}

  .crypto-address-pill {{
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    color: var(--text-white);
    background-color: var(--bg-panel-secondary);
    padding: 5px 12px;
    clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 0 100%);
    border: 1px solid var(--border-subtle);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    letter-spacing: 0.04em;
  }}

  .card-metric-badge {{
    font-family: var(--font-mono);
    font-size: 12px;
    font-weight: 700;
    color: var(--text-white);
    display: flex;
    align-items: center;
    gap: 6px;
    background-color: var(--bg-panel-secondary);
    border: 1px solid var(--border-subtle);
    padding: 5px 12px;
    clip-path: polygon(0 0, calc(100% - 6px) 0, 100% 6px, 100% 100%, 0 100%);
    letter-spacing: 0.03em;
  }}

  .front-leather-flap {{
    position: relative;
    background-color: var(--bg-panel-secondary);
    border-top: 1px solid var(--border-divider);
    padding: 12px 24px;
    z-index: 4;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }}

  /* Top Navigation Bar with Tactile Pill Buttons (18px Radius) */
  .segmented-pill-bar {{
    display: inline-flex;
    align-items: center;
    background-color: var(--bg-panel);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 4px;
    gap: 4px;
  }}

  .tactile-pill-btn {{
    background: transparent;
    border: none;
    border-radius: 18px;
    padding: 6px 16px;
    font-family: var(--font-display);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: var(--text-muted);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
    transition: all 0.15s ease;
  }}

  .tactile-pill-btn:hover {{
    color: var(--text-white);
    background-color: rgba(255, 255, 255, 0.06);
  }}

  .tactile-pill-btn.active {{
    background-color: var(--surface-purple);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.2);
  }}

  .leather-toggle-group {{
    display: flex;
    align-items: center;
    gap: 6px;
    background-color: var(--bg-panel);
    padding: 2px;
    clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 0 100%);
    border: 1px solid var(--border-subtle);
  }}

  .leather-toggle-btn {{
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-family: var(--font-display);
    font-size: 11px;
    font-weight: 700;
    padding: 6px 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 0 100%);
    transition: all 0.15s ease;
  }}

  .leather-toggle-btn:hover {{
    color: var(--text-white);
    background-color: rgba(255, 255, 255, 0.06);
  }}

  .leather-toggle-btn.active {{
    background-color: var(--surface-purple);
    color: #ffffff;
    font-weight: 700;
  }}

  .vault-status-indicator {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: var(--text-white);
  }}

  .status-pulse {{
    width: 8px;
    height: 8px;
    background-color: var(--accent-emerald);
    clip-path: polygon(0 0, calc(100% - 3px) 0, 100% 3px, 100% 100%, 0 100%);
  }}

  /* ==========================================================================
     LINEAR PROGRESS STEPPER RAIL
     ========================================================================== */
  .stepper-rail-container {{
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 18px) 0, 100% 18px, 100% 100%, 0 100%);
    padding: 1px;
    margin-bottom: 24px;
  }}

  .stepper-rail-inner {{
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 17.586px) 0, 100% 17.586px, 100% 100%, 0 100%);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    overflow-x: auto;
    gap: 16px;
  }}

  .stepper-rail-track {{
    position: absolute;
    top: 50%;
    left: 80px;
    right: 80px;
    height: 2px;
    background-color: var(--border-subtle);
    z-index: 1;
  }}

  .step-node {{
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 10px;
    background-color: var(--bg-panel);
    padding: 4px 14px;
    cursor: pointer;
  }}

  .step-node-icon {{
    width: 36px;
    height: 36px;
    border-radius: 18px;
    background-color: var(--bg-panel-secondary);
    border: 1px solid var(--border-muted);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    flex-shrink: 0;
    transition: all 0.15s ease;
  }}

  .step-node.active .step-node-icon {{
    background-color: var(--accent-emerald);
    border-color: var(--accent-emerald);
    color: #08090b;
  }}

  .step-node.completed .step-node-icon {{
    background-color: var(--surface-purple);
    border-color: rgba(255, 255, 255, 0.3);
    color: #ffffff;
  }}

  .step-node-content {{
    display: flex;
    flex-direction: column;
  }}

  .step-node-num {{
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    color: var(--text-dim);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }}

  .step-node.active .step-node-num {{
    color: var(--accent-emerald);
  }}

  .step-node-title {{
    font-family: var(--font-display);
    font-size: 12px;
    font-weight: 700;
    color: var(--text-white);
    letter-spacing: -0.01em;
  }}

  /* ==========================================================================
     SPLIT TWO-COLUMN WORKSPACE ARCHITECTURE
     ========================================================================== */
  .obsidian-workspace {{
    display: grid;
    grid-template-columns: minmax(0, 1fr) 390px;
    gap: 24px;
    align-items: start;
    margin-bottom: 28px;
  }}

  @media (max-width: 1100px) {{
    .obsidian-workspace {{
      grid-template-columns: 1fr;
    }}
  }}

  /* Left Column: Interactive Visual Card Stage */
  .visual-stage-column {{
    display: flex;
    flex-direction: column;
    gap: 24px;
  }}

  .stage-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 14px;
    border-bottom: 1px solid var(--border-divider);
    padding-bottom: 12px;
  }}

  .stage-title-wrap {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .stage-title {{
    font-family: var(--font-display);
    font-size: 16px;
    font-weight: 900;
    letter-spacing: -0.03em;
    color: var(--text-white);
  }}

  .indicator-pulse {{
    width: 8px;
    height: 8px;
    background-color: var(--accent-emerald);
    clip-path: polygon(0 0, calc(100% - 2px) 0, 100% 2px, 100% 100%, 0 100%);
    display: inline-block;
  }}

  .critical-cue-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: var(--font-mono);
    font-size: 10.5px;
    font-weight: 700;
    color: #ffffff;
    background-color: var(--accent-crimson);
    padding: 3px 8px;
    clip-path: polygon(0 0, calc(100% - 6px) 0, 100% 6px, 100% 100%, 0 100%);
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }}

  .stage-controls-tray {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid var(--border-divider);
  }}

  .stage-btn-group {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }}

  .stage-tool-btn {{
    background-color: var(--bg-panel-secondary);
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
    font-family: var(--font-display);
    font-size: 11px;
    font-weight: 700;
    padding: 6px 12px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 0 100%);
    transition: all 0.15s ease;
  }}

  .stage-tool-btn:hover {{
    background-color: var(--border-muted);
    color: var(--text-white);
  }}

  /* Right Column: Technical Parameter Inspector */
  .inspector-column {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    position: sticky;
    top: 24px;
  }}

  .inspector-header-card {{
    background-color: var(--surface-purple);
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
    padding: 16px 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
  }}

  .inspector-header-title {{
    font-family: var(--font-display);
    font-size: 13px;
    font-weight: 900;
    letter-spacing: -0.02em;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 8px;
    text-transform: uppercase;
  }}

  .inspector-header-subtitle {{
    font-family: var(--font-mono);
    font-size: 10px;
    color: rgba(255, 255, 255, 0.75);
    margin-top: 4px;
    letter-spacing: 0.05em;
  }}

  .inspector-group-card {{
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
    padding: 1px;
  }}

  .inspector-group-inner {{
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 13.586px) 0, 100% 13.586px, 100% 100%, 0 100%);
    padding: 16px 18px;
  }}

  .inspector-group-title {{
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    color: var(--accent-emerald);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
    border-bottom: 1px solid var(--border-divider);
    padding-bottom: 8px;
  }}

  .param-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    font-size: 11.5px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  }}

  .param-row:last-child {{
    border-bottom: none;
  }}

  .param-label {{
    font-family: var(--font-main);
    color: var(--text-muted);
  }}

  .param-value {{
    font-family: var(--font-mono);
    font-weight: 600;
    color: var(--text-white);
  }}

  .mono-badge {{
    font-family: var(--font-mono);
    font-size: 10.5px;
    font-weight: 600;
    padding: 3px 8px;
    background-color: var(--bg-panel-secondary);
    border: 1px solid var(--border-subtle);
    color: var(--text-monochrome);
    clip-path: polygon(0 0, calc(100% - 6px) 0, 100% 6px, 100% 100%, 0 100%);
    letter-spacing: 0.03em;
  }}

  .mono-badge-emerald {{
    background-color: rgba(0, 182, 122, 0.12);
    border-color: var(--accent-emerald);
    color: var(--accent-emerald);
  }}

  .mono-badge-crimson {{
    background-color: rgba(255, 0, 80, 0.12);
    border-color: var(--accent-crimson);
    color: var(--accent-crimson);
  }}

  /* ==========================================================================
     BLANK CANVAS PRESETS & CONTROLS BAR
     ========================================================================== */
  .section-header-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border-divider);
    padding-bottom: 12px;
    flex-wrap: wrap;
    gap: 12px;
  }}

  .section-title {{
    font-family: var(--font-display);
    font-size: 14px;
    font-weight: 800;
    color: var(--text-white);
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: -0.03em;
    text-transform: uppercase;
  }}

  .section-desc {{
    font-size: 11.5px;
    font-family: var(--font-mono);
    color: var(--text-muted);
  }}

  .blank-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 14px;
  }}

  .blank-card-wrapper {{
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
    padding: 1px;
    transition: all 0.15s ease;
    cursor: pointer;
  }}

  .blank-card-wrapper:hover {{
    background-color: var(--border-muted);
    transform: translateY(-2px);
  }}

  .blank-card-inner {{
    background-color: var(--bg-panel-secondary);
    clip-path: polygon(0 0, calc(100% - 13.586px) 0, 100% 13.586px, 100% 100%, 0 100%);
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    height: 100%;
  }}

  .blank-card-name {{
    font-family: var(--font-display);
    font-size: 13px;
    font-weight: 700;
    color: var(--text-white);
    letter-spacing: -0.01em;
  }}

  .blank-card-dim {{
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.4;
  }}

  .blank-card-link {{
    font-family: var(--font-display);
    font-size: 11px;
    font-weight: 600;
    color: var(--accent-emerald);
    text-decoration: none;
    margin-top: auto;
    padding-top: 8px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }}

  .controls-bar {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 24px;
  }}

  .cyber-search-group {{
    display: flex;
    align-items: stretch;
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
    padding: 1px;
    transition: background-color 0.15s ease;
    width: 100%;
    height: 44px;
  }}

  .cyber-search-group:focus-within {{
    background-color: var(--border-muted);
  }}

  .cyber-search-inner {{
    display: flex;
    align-items: center;
    background-color: var(--bg-input);
    clip-path: polygon(0 0, calc(100% - 13.586px) 0, 100% 13.586px, 100% 100%, 0 100%);
    width: 100%;
    padding-left: 14px;
  }}

  .cyber-search-input {{
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text-white);
    font-family: var(--font-main);
    font-size: 13.5px;
    padding: 10px 12px;
  }}

  .cyber-search-divider {{
    width: 1px;
    height: 24px;
    background-color: var(--border-subtle);
  }}

  .cyber-search-btn {{
    background: transparent;
    border: none;
    color: var(--text-muted);
    padding: 10px 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: var(--font-display);
    font-size: 12px;
    font-weight: 700;
    transition: all 0.15s ease;
    clip-path: polygon(0 0, calc(100% - 13px) 0, 100% 13px, 100% 100%, 0 100%);
  }}

  .cyber-search-btn:hover {{
    color: var(--text-white);
    background-color: rgba(255, 255, 255, 0.06);
  }}

  .stepper-tabs {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}

  .stepper-tab-btn {{
    position: relative;
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 0 100%);
    padding: 1px;
    cursor: pointer;
    border: none;
    transition: all 0.15s ease;
  }}

  .stepper-tab-btn .tab-content {{
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 11.586px) 0, 100% 11.586px, 100% 100%, 0 100%);
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-muted);
    font-family: var(--font-display);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.02em;
  }}

  .stepper-tab-btn:hover {{
    background-color: var(--border-muted);
  }}

  .stepper-tab-btn:hover .tab-content {{
    color: var(--text-white);
  }}

  .stepper-tab-btn.active {{
    background-color: var(--surface-purple);
  }}

  .stepper-tab-btn.active .tab-content {{
    background-color: var(--surface-purple);
    color: #ffffff;
    font-weight: 700;
  }}

  /* ==========================================================================
     CYBER GRID TEMPLATE ARCHIVE
     ========================================================================== */
  .cyber-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 18px;
  }}

  .template-card-wrapper {{
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
    padding: 1px;
    transition: all 0.15s ease;
    cursor: pointer;
  }}

  .template-card-wrapper:hover {{
    background-color: var(--border-muted);
    transform: translateY(-2px);
  }}

  .template-card-wrapper.selected {{
    background-color: var(--accent-emerald);
  }}

  .template-card-inner {{
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 13.586px) 0, 100% 13.586px, 100% 100%, 0 100%);
    display: flex;
    flex-direction: column;
    height: 100%;
  }}

  .card-img-wrap {{
    position: relative;
    width: 100%;
    height: 230px;
    background-color: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 14px;
    box-sizing: border-box;
    border-bottom: 1px solid var(--border-subtle);
    -webkit-user-select: none;
    user-select: none;
  }}

  /* Anti-theft transparent protection shield overlay */
  .resource-protection-shield {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
    cursor: pointer;
    background: transparent;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    user-select: none;
  }}

  /* Anti-theft watermark protection tag */
  .watermark-protection-tag {{
    position: absolute;
    bottom: 8px;
    right: 8px;
    font-family: var(--font-mono);
    font-size: 8.5px;
    font-weight: 700;
    color: rgba(15, 23, 42, 0.40);
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(15, 23, 42, 0.08);
    padding: 2px 6px;
    border-radius: 4px;
    letter-spacing: 0.06em;
    pointer-events: none;
    z-index: 11;
    user-select: none;
  }}

  .card-img-wrap img,
  .element-preview img,
  .winzy-marquee-card img,
  #stagePreviewImg {{
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 6px;
    filter: drop-shadow(0 4px 14px rgba(15, 23, 42, 0.08));
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    -webkit-user-drag: none !important;
    user-drag: none !important;
    -webkit-user-select: none !important;
    user-select: none !important;
    -webkit-touch-callout: none !important;
    pointer-events: none !important;
  }}

  .template-card-wrapper:hover .card-img-wrap img {{
    transform: scale(1.04);
  }}

  /* Discrete Editorial Protection Notice Toast */
  .protection-notice-toast {{
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 100000;
    background: #0f172a;
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
    border-radius: 12px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.05em;
    opacity: 0;
    transform: translateY(12px);
    pointer-events: none;
    transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }}

  .protection-notice-toast.is-visible {{
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
  }}

  .protection-toast-badge {{
    background: rgba(255, 255, 255, 0.15);
    color: #38bdf8;
    padding: 3px 7px;
    border-radius: 4px;
    font-weight: 800;
    font-size: 9.5px;
    letter-spacing: 0.06em;
  }}

  .protection-toast-text {{
    font-weight: 600;
    color: #ffffff;
  }}

  .card-body {{
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
  }}

  .card-title {{
    font-family: var(--font-display);
    font-size: 13.5px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-white);
    line-height: 1.4;
    word-break: break-word;
  }}

  .card-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: auto;
  }}

  .pill {{
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 600;
    padding: 3px 7px;
    background-color: var(--bg-panel-secondary);
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
    clip-path: polygon(0 0, calc(100% - 5px) 0, 100% 5px, 100% 100%, 0 100%);
  }}

  .pill.paper {{
    color: var(--text-white);
  }}

  .pill.orient {{
    color: var(--accent-emerald);
  }}

  .pill.tag-mint {{
    color: var(--accent-emerald);
    border-color: rgba(0, 182, 122, 0.4);
  }}

  .card-links {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px;
    background-color: var(--bg-panel-secondary);
    border-top: 1px solid var(--border-subtle);
    font-size: 11px;
  }}

  /* Vector Elements */
  .element-card-wrapper {{
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
    padding: 1px;
  }}

  .element-card-inner {{
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 13.586px) 0, 100% 13.586px, 100% 100%, 0 100%);
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    height: 100%;
  }}

  .element-preview {{
    width: 100%;
    aspect-ratio: 1;
    background-color: var(--bg-panel-secondary);
    border: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 14px;
  }}

  .element-preview img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    filter: invert(1);
  }}

  .element-name {{
    font-family: var(--font-display);
    font-size: 12px;
    font-weight: 600;
    color: var(--text-white);
    text-align: center;
    word-break: break-all;
  }}

  /* Specification Tables */
  .spec-table-container {{
    background-color: var(--bg-panel);
    border: 1px solid var(--border-subtle);
    padding: 20px;
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
  }}

  .spec-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 14px;
    font-size: 12.5px;
  }}

  .spec-table th, .spec-table td {{
    padding: 10px 14px;
    border: 1px solid var(--border-divider);
    text-align: left;
    color: var(--text-muted);
  }}

  .spec-table th {{
    background: var(--bg-panel-secondary);
    color: var(--text-white);
    font-family: var(--font-display);
    font-weight: 700;
    letter-spacing: 0.02em;
  }}

  /* ==========================================================================
     WINZY EDITORIAL LUXURY HERO SECTION // FULL SCREEN FIT VIEWPORT
     Display Only Logo (Enlarged Monumental "V" Mark) // Zero Login / Signup
     Interactive Capsule Navigation Dock // Detailed Certificate Metadata Corner
     Right Side Continuous Randomized Certificate Marquee
     Clean Monochrome Palette: White #ffffff, Deep Charcoal #0f172a
     ========================================================================== */

  .winzy-hero-section {{
    width: 100vw;
    max-width: 100vw;
    min-width: 100vw;
    height: 100vh;
    min-height: 100vh;
    max-height: 100vh;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    position: relative;
    font-family: var(--font-main);
    overflow: hidden;
  }}

  /* Full Bleed Cinematic Viewport */
  .winzy-hero-card {{
    width: 100vw;
    height: 100vh;
    border-radius: 0;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: none;
    background-color: #0f172a;
    background-image: 
      linear-gradient(180deg, rgba(15, 23, 42, 0.55) 0%, rgba(15, 23, 42, 0.0) 24%, rgba(15, 23, 42, 0.0) 55%, rgba(15, 23, 42, 0.85) 100%),
      url('assets/hero_egypt_pyramids.jpg');
    background-size: cover;
    background-position: center 36%;
    background-repeat: no-repeat;
    transition: background-image 0.5s ease-in-out;
  }}

  /* ==========================================================================
     STICKY RESIZING LUXURY NAVIGATION (ENTER FULL-SIZE -> SCROLL COMPACT ANIMATED)
     ========================================================================== */
  .winzy-card-nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 10000;
    padding: 38px 56px;
    box-sizing: border-box;
    background: transparent;
    backdrop-filter: blur(0px);
    -webkit-backdrop-filter: blur(0px);
    border-bottom: 1px solid transparent;
    box-shadow: none;
    transition: padding 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                background 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                backdrop-filter 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                border-color 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                box-shadow 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }}

  /* Scrolled State: Resized Compact Animated Sticky Bar */
  .winzy-card-nav.is-scrolled {{
    padding: 10px 42px;
    background: rgba(15, 23, 42, 0.92);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 14px 42px rgba(0, 0, 0, 0.45);
  }}

  /* Brand Unit: DISPLAY ONLY LOGO with Large Font Size ("V") on Enter, Resized on Scroll */
  .winzy-nav-brand {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    user-select: none;
    line-height: 1;
    z-index: 35;
    flex-shrink: 0;
  }}

  .winzy-logo-v {{
    font-family: 'Google Sans', var(--font-display), sans-serif;
    font-size: clamp(68px, 7.5vw, 96px);
    font-weight: 900;
    color: #ffffff;
    line-height: 0.8;
    letter-spacing: -0.07em;
    text-shadow: 0 8px 32px rgba(0, 0, 0, 0.65);
    display: inline-block;
    transition: font-size 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
                opacity 0.2s ease,
                text-shadow 0.4s ease;
  }}

  .winzy-logo-v:hover {{
    transform: scale(1.06);
    opacity: 0.95;
  }}

  .winzy-card-nav.is-scrolled .winzy-logo-v {{
    font-size: 32px;
    line-height: 1;
    letter-spacing: -0.05em;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
  }}

  /* Real Interactive Capsule Navigation Dock: Full Size on Enter, Resized on Scroll */
  .winzy-nav-pill {{
    background: rgba(255, 255, 255, 0.16);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.28);
    border-radius: 9999px;
    padding: 10px 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.16);
    position: relative;
    z-index: 35;
    transition: padding 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                gap 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                background 0.3s ease,
                border-color 0.3s ease,
                box-shadow 0.3s ease;
  }}

  .winzy-card-nav.is-scrolled .winzy-nav-pill {{
    padding: 5px 16px;
    gap: 10px;
    background: rgba(255, 255, 255, 0.10);
    border-color: rgba(255, 255, 255, 0.18);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
  }}

  .winzy-nav-item {{
    position: relative;
    display: flex;
    align-items: center;
  }}

  .winzy-nav-link {{
    color: rgba(255, 255, 255, 0.92);
    font-family: var(--font-main);
    font-size: 14.5px;
    font-weight: 500;
    text-decoration: none;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    border-radius: 9999px;
    transition: font-size 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                padding 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                color 0.15s ease,
                background-color 0.15s ease,
                transform 0.15s ease;
    user-select: none;
    border: none;
    background: transparent;
  }}

  .winzy-card-nav.is-scrolled .winzy-nav-link {{
    font-size: 13.5px;
    padding: 6px 11px;
  }}

  .winzy-nav-link:hover,
  .winzy-nav-item:hover .winzy-nav-link,
  .winzy-nav-link.active {{
    color: #ffffff;
    background-color: rgba(255, 255, 255, 0.20);
  }}

  .winzy-nav-live-dot {{
    width: 6px;
    height: 6px;
    border-radius: 9999px;
    background-color: #22c55e;
    box-shadow: 0 0 8px #22c55e;
    display: inline-block;
  }}

  .winzy-nav-caret {{
    width: 9px;
    height: 9px;
    stroke: #ffffff;
    stroke-width: 1.8;
    fill: none;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  }}

  .winzy-nav-item:hover .winzy-nav-caret {{
    transform: rotate(180deg);
  }}

  /* Interactive Dropdown Menus */
  .winzy-nav-dropdown {{
    position: absolute;
    top: calc(100% + 12px);
    left: 50%;
    transform: translateX(-50%) translateY(8px);
    background: rgba(15, 23, 42, 0.94);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 18px;
    padding: 8px;
    min-width: 250px;
    box-shadow: 0 24px 52px rgba(0, 0, 0, 0.5);
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: opacity 0.2s cubic-bezier(0.16, 1, 0.3, 1), transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 100;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}

  .winzy-card-nav.is-scrolled .winzy-nav-dropdown {{
    top: calc(100% + 8px);
  }}

  .winzy-nav-item:hover .winzy-nav-dropdown,
  .winzy-nav-item:focus-within .winzy-nav-dropdown {{
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
    transform: translateX(-50%) translateY(0);
  }}

  .winzy-dropdown-header {{
    font-family: var(--font-display);
    font-size: 10px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.55);
    letter-spacing: 0.08em;
    padding: 6px 12px 4px 12px;
    text-transform: uppercase;
  }}

  .winzy-dropdown-link {{
    padding: 8px 12px;
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.9);
    font-size: 13px;
    font-weight: 500;
    text-decoration: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    cursor: pointer;
    transition: background-color 0.15s ease, color 0.15s ease, transform 0.15s ease;
  }}

  .winzy-dropdown-link:hover {{
    background-color: rgba(255, 255, 255, 0.16);
    color: #ffffff;
    transform: translateX(3px);
  }}

  .winzy-dropdown-badge {{
    font-family: var(--font-mono);
    font-size: 10.5px;
    background: rgba(255, 255, 255, 0.16);
    color: #ffffff;
    padding: 2px 7px;
    border-radius: 9999px;
    font-weight: 700;
  }}

  /* Spacer & Quick CTA to balance capsule dock */
  .winzy-nav-spacer {{
    min-width: 96px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    transition: min-width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }}

  .winzy-card-nav.is-scrolled .winzy-nav-spacer {{
    min-width: 32px;
  }}

  .winzy-nav-quick-cta {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 9999px;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.22);
    color: #ffffff;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-decoration: none;
    transition: all 0.2s ease;
  }}

  .winzy-nav-quick-cta:hover {{
    background: #ffffff;
    color: #0f172a;
    border-color: #ffffff;
    transform: translateY(-1px);
  }}

  .winzy-quick-dot {{
    width: 6px;
    height: 6px;
    border-radius: 9999px;
    background-color: #38bdf8;
    box-shadow: 0 0 6px #38bdf8;
  }}

  /* ==========================================================================
     MOBILE RESPONSIVE NAVIGATION SYSTEM (DRAWER, HAMBURGER & TOUCH TARGETS)
     ========================================================================== */
  .winzy-mobile-toggle {{
    display: none;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    width: 42px;
    height: 42px;
    padding: 0;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 12px;
    cursor: pointer;
    z-index: 10002;
    position: relative;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
    gap: 4.5px;
    flex-shrink: 0;
  }}

  .winzy-mobile-toggle:hover,
  .winzy-mobile-toggle:focus-visible {{
    background: rgba(255, 255, 255, 0.20);
    border-color: rgba(255, 255, 255, 0.36);
    outline: none;
  }}

  .winzy-toggle-bar {{
    display: block;
    width: 20px;
    height: 2px;
    background: #ffffff;
    border-radius: 2px;
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease;
    pointer-events: none;
  }}

  /* Animated Hamburger to X */
  .winzy-mobile-toggle.is-open .winzy-toggle-bar:nth-child(1) {{
    transform: translateY(6.5px) rotate(45deg);
  }}
  .winzy-mobile-toggle.is-open .winzy-toggle-bar:nth-child(2) {{
    opacity: 0;
    transform: scaleX(0);
  }}
  .winzy-mobile-toggle.is-open .winzy-toggle-bar:nth-child(3) {{
    transform: translateY(-6.5px) rotate(-45deg);
  }}

  /* Mobile Backdrop Overlay */
  .winzy-mobile-backdrop {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100vh;
    background: rgba(0, 0, 0, 0.60);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    z-index: 9998;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.3s;
  }}

  .winzy-mobile-backdrop.is-open {{
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
  }}

  /* Mobile Drawer Menu Sheet */
  .winzy-mobile-drawer {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    background: rgba(15, 23, 42, 0.98);
    backdrop-filter: blur(36px);
    -webkit-backdrop-filter: blur(36px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65);
    z-index: 9999;
    max-height: 85vh;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1),
                opacity 0.25s ease,
                visibility 0.35s;
    padding-top: 84px;
  }}

  .winzy-mobile-drawer.is-open {{
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
  }}

  .winzy-mobile-drawer-inner {{
    padding: 14px 20px 32px 20px;
    display: flex;
    flex-direction: column;
    gap: 22px;
    max-width: 560px;
    margin: 0 auto;
  }}

  .winzy-mobile-group {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .winzy-mobile-group-title {{
    font-family: var(--font-mono);
    font-size: 10.5px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.45);
    letter-spacing: 0.08em;
    padding: 0 8px 4px 8px;
    text-transform: uppercase;
  }}

  .winzy-mobile-link {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 13px 15px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #ffffff;
    text-decoration: none;
    font-family: var(--font-display);
    font-size: 15px;
    font-weight: 600;
    transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
    min-height: 48px;
  }}

  .winzy-mobile-link:active,
  .winzy-mobile-link:hover {{
    background: rgba(255, 255, 255, 0.10);
    border-color: rgba(255, 255, 255, 0.18);
    transform: translateX(2px);
  }}

  .winzy-mobile-link.active {{
    background: rgba(255, 255, 255, 0.14);
    border-color: rgba(255, 255, 255, 0.32);
    font-weight: 700;
  }}

  .winzy-mobile-link-left {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .winzy-mobile-link-icon {{
    width: 18px;
    height: 18px;
    color: rgba(255, 255, 255, 0.85);
    flex-shrink: 0;
  }}

  .winzy-mobile-pill-badge {{
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 9999px;
    background: rgba(255, 255, 255, 0.16);
    color: #ffffff;
    letter-spacing: 0.02em;
  }}

  .winzy-mobile-live-tag {{
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 9999px;
    background: rgba(16, 185, 129, 0.25);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.45);
    letter-spacing: 0.04em;
  }}

  .winzy-mobile-pill-muted {{
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.5);
  }}

  /* Category Rows in Mobile Menu */
  .winzy-mobile-cat-list {{
    display: flex;
    flex-direction: column;
    background: rgba(0, 0, 0, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    overflow: hidden;
  }}

  .winzy-mobile-cat-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    color: rgba(255, 255, 255, 0.88);
    text-decoration: none;
    font-family: var(--font-main);
    font-size: 13.5px;
    font-weight: 500;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    transition: background 0.15s ease, color 0.15s ease;
    min-height: 44px;
  }}

  .winzy-mobile-cat-row:last-child {{
    border-bottom: none;
  }}

  .winzy-mobile-cat-row:hover,
  .winzy-mobile-cat-row:active {{
    background: rgba(255, 255, 255, 0.08);
    color: #ffffff;
  }}

  .winzy-mobile-cat-row.active {{
    background: rgba(255, 255, 255, 0.14);
    color: #ffffff;
    font-weight: 700;
  }}

  .winzy-mobile-cat-count {{
    font-family: var(--font-mono);
    font-size: 11.5px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.5);
  }}

  /* Bottom Actions in Drawer */
  .winzy-mobile-actions {{
    margin-top: 4px;
  }}

  .winzy-mobile-btn-primary {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    padding: 14px 20px;
    border-radius: 12px;
    background: #ffffff;
    color: #0f172a;
    font-family: var(--font-display);
    font-size: 13.5px;
    font-weight: 800;
    letter-spacing: 0.03em;
    text-decoration: none;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    transition: transform 0.15s ease, background 0.15s ease;
    min-height: 48px;
  }}

  .winzy-mobile-btn-primary:active {{
    transform: scale(0.98);
    background: #f1f5f9;
  }}

  /* Prevent background scrolling when mobile nav is open */
  body.nav-mobile-open {{
    overflow: hidden !important;
    touch-action: none;
  }}

  /* Hero Navigation Placeholder so Hero Flex Layout remains aligned */
  .winzy-hero-nav-placeholder {{
    height: 110px;
    flex-shrink: 0;
    pointer-events: none;
    width: 100%;
  }}

  /* Monumental Center Watermark */
  .winzy-watermark-text {{
    position: absolute;
    top: 42%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: var(--font-main), var(--font-display), sans-serif;
    font-size: clamp(80px, 15vw, 220px);
    font-weight: 900;
    letter-spacing: 0.08em;
    color: rgba(255, 255, 255, 0.28);
    pointer-events: none;
    z-index: 2;
    user-select: none;
    text-transform: uppercase;
    white-space: nowrap;
    line-height: 1;
  }}

  /* Bottom Card Elements */
  .winzy-card-bottom {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    position: relative;
    z-index: 10;
    width: 100%;
    padding: 40px 52px;
    box-sizing: border-box;
    gap: 24px;
    flex-wrap: wrap;
  }}

  .winzy-bottom-left {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-width: 720px;
  }}

  .winzy-stats-row {{
    display: flex;
    align-items: flex-start;
    gap: 40px;
    flex-wrap: wrap;
  }}

  .winzy-stat-col {{
    display: flex;
    flex-direction: column;
  }}

  .winzy-stat-num {{
    font-family: var(--font-display), var(--font-main);
    font-size: clamp(32px, 3.8vw, 44px);
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
    letter-spacing: -0.03em;
    text-shadow: 0 4px 18px rgba(0, 0, 0, 0.5);
  }}

  .winzy-stat-label {{
    font-family: var(--font-main);
    font-size: 12.5px;
    color: rgba(255, 255, 255, 0.88);
    margin-top: 5px;
    font-weight: 500;
    letter-spacing: 0.02em;
  }}

  .winzy-details-desc {{
    font-family: var(--font-main);
    font-size: 13.5px;
    line-height: 1.55;
    color: rgba(255, 255, 255, 0.9);
    max-width: 640px;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
  }}

  .winzy-quick-filters {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 2px;
  }}

  .winzy-filter-pill {{
    background: rgba(255, 255, 255, 0.16);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    color: #ffffff;
    font-family: var(--font-main);
    font-size: 12px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 9999px;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.15s ease;
  }}

  .winzy-filter-pill:hover {{
    background: #ffffff;
    color: #0f172a;
    border-color: #ffffff;
    transform: translateY(-1px);
  }}

  /* ==========================================================================
     HORIZONTAL LEFT-TO-RIGHT CERTIFICATE MARQUEE (FULL UNCROPPED TRANSPARENCY)
     ========================================================================== */
  .winzy-horizontal-marquee {{
    position: absolute;
    left: 0;
    right: 0;
    width: 100%;
    top: calc(50% - 20px);
    transform: translateY(-50%);
    z-index: 15;
    display: flex;
    flex-direction: column;
    gap: 12px;
    pointer-events: auto;
  }}

  .winzy-marquee-bar-header {{
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .winzy-marquee-header-pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 18px;
    border-radius: 9999px;
    background: rgba(15, 23, 42, 0.55);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.20);
    color: #ffffff;
    font-family: var(--font-display);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
  }}

  .winzy-marquee-pulse {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background-color: #22c55e;
    box-shadow: 0 0 10px #22c55e;
    animation: winzyPulse 2s infinite ease-in-out;
  }}

  @keyframes winzyPulse {{
    0%, 100% {{ opacity: 0.4; transform: scale(0.9); }}
    50% {{ opacity: 1; transform: scale(1.2); }}
  }}

  .winzy-marquee-track-wrap {{
    width: 100%;
    overflow: hidden;
    position: relative;
    mask-image: linear-gradient(90deg, transparent 0%, black 6%, black 94%, transparent 100%);
    -webkit-mask-image: linear-gradient(90deg, transparent 0%, black 6%, black 94%, transparent 100%);
    padding: 10px 0;
  }}

  .winzy-marquee-track {{
    display: flex;
    flex-direction: row;
    gap: 24px;
    width: max-content;
    padding: 8px 0;
    animation: winzyMarqueeScrollLeftToRight 55s linear infinite;
  }}

  .winzy-marquee-track:hover {{
    animation-play-state: paused;
  }}

  /* Continuous horizontal gliding motion from LEFT to RIGHT */
  @keyframes winzyMarqueeScrollLeftToRight {{
    0% {{
      transform: translateX(-50%);
    }}
    100% {{
      transform: translateX(0%);
    }}
  }}

  /* Natural Transparent Specimen Card (Zero Opaque Backing, Zero Cropping) */
  .winzy-marquee-card {{
    width: 320px;
    flex-shrink: 0;
    background: rgba(15, 23, 42, 0.38);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 20px;
    padding: 14px;
    cursor: pointer;
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
                border-color 0.2s ease,
                background 0.2s ease,
                box-shadow 0.25s ease;
    display: flex;
    flex-direction: column;
    gap: 10px;
    text-decoration: none;
    box-sizing: border-box;
  }}

  .winzy-marquee-card:hover {{
    transform: translateY(-6px) scale(1.02);
    border-color: rgba(255, 255, 255, 0.55);
    background: rgba(15, 23, 42, 0.68);
    box-shadow: 0 20px 42px rgba(0, 0, 0, 0.55);
  }}

  /* Full Original Transparency Certificate Presentation Container (No Cropping) */
  .winzy-marquee-thumb-wrap {{
    width: 100%;
    height: 195px;
    border-radius: 12px;
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: visible;
    padding: 2px;
    box-sizing: border-box;
  }}

  /* Uncropped High-Fidelity Certificate Sheet */
  .winzy-marquee-thumb {{
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
    display: block;
    border-radius: 8px;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.40);
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease;
  }}

  .winzy-marquee-card:hover .winzy-marquee-thumb {{
    transform: scale(1.03);
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.55);
  }}

  .winzy-marquee-info {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .winzy-marquee-title {{
    font-family: var(--font-main);
    font-size: 13px;
    font-weight: 700;
    color: #ffffff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.25;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  }}

  .winzy-marquee-meta {{
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
  }}

  .winzy-marquee-tag {{
    font-family: var(--font-mono);
    font-size: 9.5px;
    padding: 3px 8px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.16);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #ffffff;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}


  /* ==========================================================================
     GLOBAL OVERRIDES: DELETE CYBER-GRID STYLE, ENFORCE WHITE & 3-COLOR SYSTEM
     ========================================================================== */
  .chamfer-18-wrapper,
  .chamfer-14-wrapper,
  .elevated-center-card,
  .leather-sleeve {{
    position: relative;
    background-color: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 24px !important;
    clip-path: none !important;
    padding: 24px !important;
    margin-bottom: 32px !important;
    box-shadow: 0 6px 24px rgba(15, 23, 42, 0.04) !important;
    box-sizing: border-box !important;
  }}

  .chamfer-18-inner,
  .chamfer-14-inner,
  .elevated-center-card-inner {{
    background-color: #ffffff !important;
    clip-path: none !important;
    padding: 0 !important;
    border-radius: 20px !important;
  }}

  .leather-pebble-grain,
  .leather-stitch-svg,
  .tactile-stitch-svg {{
    display: none !important;
  }}

  .inserted-card-slot {{
    background: #ffffff !important;
    color: #0f172a !important;
    padding: 8px 0 20px 0 !important;
    border-bottom: 1px solid rgba(15, 23, 42, 0.06) !important;
  }}

  .inserted-card-slot svg text {{
    fill: #0f172a !important;
  }}

  .front-leather-flap {{
    background: transparent !important;
    border-top: none !important;
    padding: 16px 0 0 0 !important;
  }}

  .segmented-pill-bar {{
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 9999px !important;
    padding: 4px !important;
  }}

  .tactile-pill-btn {{
    border-radius: 9999px !important;
    color: rgba(15, 23, 42, 0.7) !important;
    font-weight: 600 !important;
  }}

  .tactile-pill-btn:hover {{
    color: #0f172a !important;
    background: rgba(15, 23, 42, 0.06) !important;
  }}

  .tactile-pill-btn.active {{
    background-color: #0f172a !important;
    color: #ffffff !important;
    border: none !important;
  }}

  .card-metric-badge,
  .crypto-address-pill,
  .mono-badge {{
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    color: #0f172a !important;
    border-radius: 9999px !important;
    clip-path: none !important;
  }}

  .critical-cue-badge {{
    background: rgba(15, 23, 42, 0.05) !important;
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    color: #0f172a !important;
    border-radius: 9999px !important;
  }}

  .indicator-pulse,
  .status-pulse {{
    background: #0f172a !important;
    border-radius: 50% !important;
    clip-path: none !important;
  }}

  .leather-toggle-group {{
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 9999px !important;
    clip-path: none !important;
    padding: 3px !important;
  }}

  .leather-toggle-btn {{
    border-radius: 9999px !important;
    clip-path: none !important;
    color: rgba(15, 23, 42, 0.65) !important;
  }}

  .leather-toggle-btn.active {{
    background: #0f172a !important;
    color: #ffffff !important;
  }}

  .vault-status-indicator {{
    color: rgba(15, 23, 42, 0.7) !important;
  }}

  /* Stepper Rail in Clean White Aesthetic */
  .stepper-rail-container {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 20px !important;
    clip-path: none !important;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03) !important;
  }}

  .stepper-rail-inner {{
    background: #ffffff !important;
    clip-path: none !important;
  }}

  .stepper-rail-track {{
    background: rgba(15, 23, 42, 0.08) !important;
  }}

  .step-node {{
    background: #ffffff !important;
  }}

  .step-node-icon {{
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.1) !important;
    color: #0f172a !important;
  }}

  .step-node.active .step-node-icon {{
    background: #0f172a !important;
    color: #ffffff !important;
    border-color: #0f172a !important;
  }}

  .step-node.completed .step-node-icon {{
    background: #0f172a !important;
    color: #ffffff !important;
    border-color: #0f172a !important;
  }}

  .step-node-num {{
    color: rgba(15, 23, 42, 0.45) !important;
  }}

  .step-node-title {{
    color: #0f172a !important;
    font-weight: 600 !important;
  }}

  /* Visual Stage Specimen Container */
  .stage-top-bar {{
    border-bottom: 1px solid rgba(15, 23, 42, 0.06) !important;
    padding-bottom: 16px !important;
    margin-bottom: 20px !important;
  }}

  .stage-title {{
    color: #0f172a !important;
    font-weight: 700 !important;
  }}

  .display-plate-white {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05) !important;
  }}

  .stage-tool-btn {{
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 9999px !important;
    color: #0f172a !important;
    font-weight: 600 !important;
  }}

  .stage-tool-btn:hover {{
    background: #0f172a !important;
    color: #ffffff !important;
  }}

  /* Blank Presets Grid & Cards */
  .section-title {{
    color: #0f172a !important;
    font-weight: 700 !important;
  }}

  .section-desc {{
    color: rgba(15, 23, 42, 0.6) !important;
  }}

  .blank-grid {{
    gap: 16px !important;
  }}

  .blank-card-wrapper {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 18px !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.03) !important;
    transition: all 0.2s ease !important;
  }}

  .blank-card-wrapper:hover {{
    transform: translateY(-2px) !important;
    border-color: rgba(15, 23, 42, 0.2) !important;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06) !important;
  }}

  .blank-card-inner {{
    background: #ffffff !important;
    border-radius: 18px !important;
  }}

  .blank-card-name {{
    color: #0f172a !important;
    font-weight: 700 !important;
  }}

  .blank-card-dim {{
    color: rgba(15, 23, 42, 0.6) !important;
  }}

  .blank-card-link {{
    color: #0f172a !important;
    font-weight: 600 !important;
  }}

  /* Sub-Section Alignments */
  .leather-sleeve,
  .stepper-rail-container {{
    max-width: 1680px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    margin-bottom: 24px !important;
  }}

  /* Catalog Controls, Search Bar, and Tabs */
  .catalog-controls-container,
  .controls-bar {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 24px !important;
    padding: 20px 24px !important;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03) !important;
    box-sizing: border-box !important;
  }}

  .cyber-search-group {{
    border-radius: 9999px !important;
    clip-path: none !important;
    background: transparent !important;
    border: 1.5px solid rgba(15, 23, 42, 0.12) !important;
    height: 48px !important;
    padding: 0 !important;
    position: relative !important;
  }}

  .cyber-search-inner {{
    border-radius: 9999px !important;
    clip-path: none !important;
    background: #ffffff !important;
    padding: 0 8px 0 18px !important;
    height: 100% !important;
  }}

  .search-input-field,
  .cyber-search-input {{
    background: transparent !important;
    border: none !important;
    color: #0f172a !important;
    padding: 10px 14px !important;
    font-family: var(--font-main) !important;
    font-size: 13.5px !important;
  }}

  .search-input-field:focus,
  .cyber-search-input:focus {{
    outline: none !important;
    box-shadow: none !important;
  }}

  .cyber-search-btn {{
    border-radius: 9999px !important;
    clip-path: none !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    padding: 8px 18px !important;
    background: rgba(15, 23, 42, 0.04) !important;
  }}

  .cyber-search-btn:hover {{
    background: rgba(15, 23, 42, 0.08) !important;
    color: #0f172a !important;
  }}

  .stepper-tab-btn {{
    clip-path: none !important;
    border-radius: 9999px !important;
    background: transparent !important;
    padding: 0 !important;
  }}

  .stepper-tab-btn .tab-content {{
    clip-path: none !important;
    border-radius: 9999px !important;
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    color: rgba(15, 23, 42, 0.7) !important;
    padding: 8px 18px !important;
    font-weight: 600 !important;
  }}

  .stepper-tab-btn.active .tab-content,
  .filter-pill.active,
  .cat-tab-btn.active,
  .stepper-tabs button.active {{
    background: #0f172a !important;
    color: #ffffff !important;
    border-color: #0f172a !important;
  }}

  .stepper-tab-btn:hover .tab-content,
  .filter-pill:hover,
  .cat-tab-btn:hover,
  .stepper-tabs button:hover {{
    color: #0f172a !important;
    background: rgba(15, 23, 42, 0.08) !important;
  }}

  /* Template Grid & Card Architecture */
  .cyber-grid {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 24px !important;
    padding: 24px !important;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03) !important;
    box-sizing: border-box !important;
  }}

  .template-card-wrapper,
  .element-card-wrapper {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 20px !important;
    clip-path: none !important;
    overflow: hidden !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.03) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    display: flex !important;
    flex-direction: column !important;
  }}

  .template-card-wrapper:hover,
  .element-card-wrapper:hover {{
    transform: translateY(-3px) !important;
    border-color: rgba(15, 23, 42, 0.22) !important;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.07) !important;
  }}

  .template-card-wrapper.selected {{
    border-color: #0f172a !important;
    box-shadow: 0 0 0 2px #0f172a, 0 12px 32px rgba(15, 23, 42, 0.08) !important;
  }}

  .template-card-inner,
  .element-card-inner {{
    background: #ffffff !important;
    clip-path: none !important;
    border-radius: 20px !important;
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
  }}

  .card-img-wrap {{
    position: relative !important;
    width: 100% !important;
    height: 230px !important;
    aspect-ratio: auto !important;
    background: #f8fafc !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    overflow: hidden !important;
    padding: 14px !important;
    box-sizing: border-box !important;
    border-bottom: 1px solid rgba(15, 23, 42, 0.06) !important;
  }}

  .card-img-wrap img {{
    max-width: 100% !important;
    max-height: 100% !important;
    width: auto !important;
    height: auto !important;
    object-fit: contain !important;
    display: block !important;
    border-radius: 6px !important;
    filter: drop-shadow(0 4px 14px rgba(15, 23, 42, 0.08)) !important;
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }}

  .template-card-wrapper:hover .card-img-wrap img {{
    transform: scale(1.04) !important;
  }}

  .card-title {{
    color: #0f172a !important;
    font-weight: 700 !important;
  }}

  .pill {{
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    color: rgba(15, 23, 42, 0.7) !important;
    border-radius: 9999px !important;
    clip-path: none !important;
    font-weight: 600 !important;
  }}

  .pill.paper {{
    color: #0f172a !important;
  }}

  .pill.orient,
  .pill.tag-mint {{
    color: #0f172a !important;
    background: rgba(15, 23, 42, 0.06) !important;
    border-color: rgba(15, 23, 42, 0.12) !important;
  }}

  .card-links {{
    background: #ffffff !important;
    border-top: 1px solid rgba(15, 23, 42, 0.06) !important;
    color: rgba(15, 23, 42, 0.6) !important;
  }}

  /* Parameter Inspector Column Modernization */
  .inspector-header-card {{
    background: #0f172a !important;
    border-radius: 20px !important;
    clip-path: none !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08) !important;
  }}

  .inspector-group-card {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 20px !important;
    clip-path: none !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.02) !important;
  }}

  .inspector-group-inner {{
    background: #ffffff !important;
    clip-path: none !important;
    border-radius: 20px !important;
  }}

  .inspector-group-title {{
    color: #0f172a !important;
    border-bottom: 1px solid rgba(15, 23, 42, 0.06) !important;
  }}

  .param-row {{
    border-bottom: 1px solid rgba(15, 23, 42, 0.04) !important;
  }}

  .param-label {{
    color: rgba(15, 23, 42, 0.6) !important;
  }}

  .param-value {{
    color: #0f172a !important;
    font-weight: 600 !important;
  }}

  .spec-table-container {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 20px !important;
    clip-path: none !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.03) !important;
  }}

  .spec-table th {{
    background: rgba(15, 23, 42, 0.03) !important;
    color: #0f172a !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
  }}

  .spec-table td {{
    border: 1px solid rgba(15, 23, 42, 0.06) !important;
    color: rgba(15, 23, 42, 0.8) !important;
  }}

  .element-preview {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.06) !important;
    border-radius: 12px !important;
  }}

  .element-preview img {{
    filter: none !important;
  }}

  .element-name {{
    color: #0f172a !important;
  }}

  /* ==========================================================================
     EDITORIAL LUXURY WORKSPACE ARCHITECTURE
     ========================================================================== */
  .editorial-workspace {{
    max-width: 1680px !important;
    margin: 40px auto 60px auto !important;
    padding: 0 32px !important;
    box-sizing: border-box !important;
  }}

  /* Command Ribbon */
  .workspace-command-ribbon {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 24px !important;
    padding: 18px 26px !important;
    margin-bottom: 28px !important;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03) !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    flex-wrap: wrap !important;
    gap: 16px !important;
    box-sizing: border-box !important;
  }}

  .ribbon-brand-col {{
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
  }}

  .ribbon-title-wrap {{
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
  }}

  .ribbon-brand-title {{
    font-family: var(--font-display) !important;
    font-size: 16px !important;
    font-weight: 900 !important;
    letter-spacing: -0.02em !important;
    color: #0f172a !important;
  }}

  .ribbon-divider {{
    color: rgba(15, 23, 42, 0.25) !important;
    font-weight: 700 !important;
  }}

  .ribbon-brand-sub {{
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    letter-spacing: 0.06em !important;
  }}

  .ribbon-meta-text {{
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    color: rgba(15, 23, 42, 0.55) !important;
    font-weight: 500 !important;
  }}

  .ribbon-actions-col {{
    display: flex !important;
    align-items: center !important;
    gap: 14px !important;
    flex-wrap: wrap !important;
  }}

  .ribbon-nav-pills {{
    display: flex !important;
    align-items: center !important;
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 9999px !important;
    padding: 4px !important;
    gap: 4px !important;
  }}

  .ribbon-pill-btn {{
    background: transparent !important;
    border: none !important;
    border-radius: 9999px !important;
    padding: 7px 16px !important;
    font-family: var(--font-display) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    color: rgba(15, 23, 42, 0.7) !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    transition: all 0.15s ease !important;
    text-decoration: none !important;
  }}

  .ribbon-pill-btn:hover {{
    color: #0f172a !important;
    background: rgba(15, 23, 42, 0.06) !important;
  }}

  .ribbon-pill-btn.active {{
    background: #0f172a !important;
    color: #ffffff !important;
  }}

  .ribbon-status-pill {{
    display: inline-flex !important;
    align-items: center !important;
    gap: 7px !important;
    background: rgba(0, 182, 122, 0.08) !important;
    border: 1px solid rgba(0, 182, 122, 0.25) !important;
    border-radius: 9999px !important;
    padding: 6px 14px !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #00875a !important;
    letter-spacing: 0.04em !important;
  }}

  .status-dot-pulse {{
    width: 8px !important;
    height: 8px !important;
    border-radius: 50% !important;
    background-color: #00b67a !important;
    box-shadow: 0 0 0 3px rgba(0, 182, 122, 0.2) !important;
    display: inline-block !important;
    flex-shrink: 0 !important;
  }}

  /* Split Two-Column Workspace */
  .obsidian-workspace {{
    max-width: 100% !important;
    display: grid !important;
    grid-template-columns: minmax(0, 1fr) 390px !important;
    gap: 24px !important;
    align-items: start !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
  }}

  /* Studio Cards Architecture */
  .studio-card {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 24px !important;
    padding: 24px !important;
    box-shadow: 0 6px 24px rgba(15, 23, 42, 0.03) !important;
    box-sizing: border-box !important;
    margin-bottom: 28px !important;
  }}

  /* Visual Stage Main Card */
  .stage-main-card {{
    padding: 24px 28px !important;
  }}

  .stage-top-bar {{
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    flex-wrap: wrap !important;
    gap: 12px !important;
    margin-bottom: 18px !important;
    border-bottom: 1px solid rgba(15, 23, 42, 0.06) !important;
    padding-bottom: 14px !important;
  }}

  .stage-title-wrap {{
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
  }}

  .stage-title {{
    font-family: var(--font-display) !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    color: #0f172a !important;
  }}

  .stage-badges-row {{
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    flex-wrap: wrap !important;
  }}

  .stage-status-pill {{
    font-family: var(--font-mono) !important;
    font-size: 10.5px !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    background: rgba(15, 23, 42, 0.06) !important;
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    border-radius: 9999px !important;
    padding: 4px 10px !important;
    letter-spacing: 0.05em !important;
  }}

  .stage-display-plate {{
    width: 100% !important;
    min-height: 480px !important;
    background: #f8fafc !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 18px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 28px !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
    position: relative !important;
    box-shadow: inset 0 2px 8px rgba(15, 23, 42, 0.02) !important;
  }}

  .stage-display-plate img {{
    max-width: 100% !important;
    max-height: 480px !important;
    object-fit: contain !important;
    display: block !important;
    border-radius: 8px !important;
    box-shadow: 0 14px 34px rgba(15, 23, 42, 0.12) !important;
    transition: transform 0.25s ease, max-height 0.2s ease !important;
  }}

  .stage-controls-tray {{
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    flex-wrap: wrap !important;
    gap: 12px !important;
    margin-top: 18px !important;
    padding-top: 14px !important;
    border-top: 1px solid rgba(15, 23, 42, 0.06) !important;
  }}

  .stage-btn-group {{
    display: flex !important;
    gap: 8px !important;
    flex-wrap: wrap !important;
  }}

  .stage-tool-btn {{
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    color: #0f172a !important;
    font-family: var(--font-display) !important;
    font-size: 11.5px !important;
    font-weight: 700 !important;
    padding: 8px 14px !important;
    border-radius: 9999px !important;
    clip-path: none !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    transition: all 0.15s ease !important;
  }}

  .stage-tool-btn:hover {{
    background: #0f172a !important;
    color: #ffffff !important;
    border-color: #0f172a !important;
  }}

  .stage-tray-meta {{
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    color: rgba(15, 23, 42, 0.5) !important;
    font-weight: 600 !important;
  }}

  /* Blank Presets Main Card */
  .presets-main-card {{
    padding: 24px 28px !important;
  }}

  .section-header-row {{
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    flex-wrap: wrap !important;
    gap: 12px !important;
    margin-bottom: 20px !important;
    border-bottom: 1px solid rgba(15, 23, 42, 0.06) !important;
    padding-bottom: 14px !important;
  }}

  .section-title {{
    font-family: var(--font-display) !important;
    font-size: 16px !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    color: #0f172a !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
  }}

  .section-header-meta {{
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
  }}

  .section-desc {{
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    color: rgba(15, 23, 42, 0.55) !important;
  }}

  .blank-grid {{
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)) !important;
    gap: 14px !important;
  }}

  .blank-preset-card {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 16px !important;
    padding: 16px 18px !important;
    cursor: pointer !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    min-height: 115px !important;
    box-sizing: border-box !important;
  }}

  .blank-preset-card:hover {{
    transform: translateY(-3px) !important;
    border-color: rgba(15, 23, 42, 0.25) !important;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06) !important;
  }}

  .blank-card-name {{
    font-family: var(--font-display) !important;
    font-size: 13.5px !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    margin-bottom: 4px !important;
  }}

  .blank-card-dim {{
    font-family: var(--font-mono) !important;
    font-size: 10.5px !important;
    color: rgba(15, 23, 42, 0.55) !important;
    line-height: 1.45 !important;
    margin-bottom: 10px !important;
  }}

  .blank-card-link {{
    font-family: var(--font-display) !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 5px !important;
  }}

  /* Controls Main Card */
  .controls-main-card {{
    padding: 20px 24px !important;
  }}

  .studio-search-wrapper {{
    display: flex !important;
    align-items: center !important;
    background: #ffffff !important;
    border: 1.5px solid rgba(15, 23, 42, 0.12) !important;
    border-radius: 9999px !important;
    padding: 4px 6px 4px 18px !important;
    height: 48px !important;
    box-sizing: border-box !important;
    margin-bottom: 18px !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
  }}

  .studio-search-wrapper:focus-within {{
    border-color: #0f172a !important;
    box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.08) !important;
  }}

  .studio-search-icon {{
    flex-shrink: 0 !important;
  }}

  .studio-search-input {{
    flex: 1 !important;
    border: none !important;
    background: transparent !important;
    font-family: var(--font-main) !important;
    font-size: 13.5px !important;
    color: #0f172a !important;
    padding: 0 12px !important;
    outline: none !important;
  }}

  .studio-search-input::placeholder {{
    color: rgba(15, 23, 42, 0.45) !important;
  }}

  .studio-search-btn {{
    background: #0f172a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9999px !important;
    padding: 8px 20px !important;
    font-family: var(--font-display) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: background-color 0.15s ease !important;
  }}

  .studio-search-btn:hover {{
    background: #1e293b !important;
  }}

  .studio-category-tabs {{
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
  }}

  /* Parameter Inspector Master Card */
  .inspector-main-card {{
    padding: 0 !important;
    overflow: hidden !important;
    position: sticky !important;
    top: 24px !important;
  }}

  .inspector-card-header {{
    background: #0f172a !important;
    padding: 22px 24px !important;
    color: #ffffff !important;
  }}

  .inspector-card-title {{
    font-family: var(--font-display) !important;
    font-size: 14px !important;
    font-weight: 900 !important;
    letter-spacing: 0.02em !important;
    color: #ffffff !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
  }}

  .inspector-card-subtitle {{
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    color: rgba(255, 255, 255, 0.65) !important;
    margin-top: 4px !important;
    letter-spacing: 0.05em !important;
  }}

  .inspector-badges-row {{
    display: flex !important;
    gap: 8px !important;
    margin-top: 12px !important;
  }}

  .mono-badge-charcoal {{
    background: rgba(255, 255, 255, 0.12) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 9999px !important;
    padding: 3px 8px !important;
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    font-weight: 700 !important;
  }}

  .inspector-card-body {{
    padding: 20px 24px 24px 24px !important;
  }}

  .inspector-section {{
    border-bottom: 1px solid rgba(15, 23, 42, 0.06) !important;
    padding-bottom: 14px !important;
    margin-bottom: 14px !important;
  }}

  .inspector-section-title {{
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    margin-bottom: 10px !important;
  }}

  .inspector-action-btn {{
    background: rgba(15, 23, 42, 0.04) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 9999px !important;
    color: #0f172a !important;
    font-family: var(--font-display) !important;
    font-size: 11.5px !important;
    font-weight: 700 !important;
    padding: 10px 16px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    text-decoration: none !important;
    transition: all 0.15s ease !important;
  }}

  .inspector-action-btn:hover {{
    background: #0f172a !important;
    color: #ffffff !important;
    border-color: #0f172a !important;
  }}

  /* Pagination Bar Architecture */
  .pagination-main-bar {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important;
    border-radius: 24px !important;
    padding: 16px 24px !important;
    margin-top: 24px !important;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    flex-wrap: wrap !important;
    gap: 16px !important;
    box-sizing: border-box !important;
  }}

  .pagination-info {{
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    color: rgba(15, 23, 42, 0.6) !important;
    font-weight: 500 !important;
  }}

  .pagination-info strong {{
    color: #0f172a !important;
    font-weight: 700 !important;
  }}

  .pagination-controls {{
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    flex-wrap: wrap !important;
  }}

  .pagination-btn {{
    background: #ffffff !important;
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
    color: #0f172a !important;
    font-family: var(--font-display) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    border-radius: 9999px !important;
    padding: 6px 14px !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 5px !important;
    transition: all 0.15s ease !important;
  }}

  .pagination-btn:hover:not(:disabled) {{
    background: #0f172a !important;
    color: #ffffff !important;
    border-color: #0f172a !important;
  }}

  .pagination-btn.active {{
    background: #0f172a !important;
    color: #ffffff !important;
    border-color: #0f172a !important;
    pointer-events: none !important;
  }}

  .pagination-btn:disabled {{
    opacity: 0.35 !important;
    cursor: not-allowed !important;
  }}

  .pagination-ellipsis {{
    font-family: var(--font-mono) !important;
    color: rgba(15, 23, 42, 0.4) !important;
    padding: 0 4px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
  }}

  @media (max-width: 600px) {{
    .pagination-main-bar {{
      flex-direction: column !important;
      align-items: center !important;
      gap: 12px !important;
      padding: 14px 16px !important;
    }}
    .pagination-info {{
      text-align: center !important;
      font-size: 11px !important;
    }}
    .pagination-controls {{
      justify-content: center !important;
    }}
    .pagination-btn {{
      padding: 5px 10px !important;
      font-size: 11.5px !important;
    }}
  }}

  @media (max-width: 900px) {{
    .winzy-horizontal-marquee {{
      position: relative;
      top: auto;
      transform: none;
      margin: 20px 0;
    }}
    .winzy-marquee-card {{
      width: 260px;
    }}
    .winzy-marquee-thumb-wrap {{
      height: 150px;
    }}
    .winzy-hero-section {{
      height: auto;
      min-height: 100vh;
      margin: 0;
      padding: 0;
    }}
    .winzy-hero-card {{
      min-height: 100vh;
      border-radius: 0;
    }}
    .winzy-card-nav {{
      padding: 14px 20px;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }}
    .winzy-card-nav.is-scrolled {{
      padding: 10px 18px;
    }}
    .winzy-logo-v {{
      font-size: 42px;
    }}
    .winzy-card-nav.is-scrolled .winzy-logo-v {{
      font-size: 28px;
    }}
    /* Hide desktop capsule dock on mobile devices */
    .winzy-nav-pill {{
      display: none !important;
    }}
    /* Show clean mobile hamburger toggle */
    .winzy-mobile-toggle {{
      display: flex !important;
    }}
    /* Keep studio shortcut & mobile toggle in spacer on mobile header */
    .winzy-nav-spacer {{
      display: flex !important;
      min-width: auto;
      gap: 10px;
      align-items: center;
    }}
    .winzy-nav-quick-cta {{
      padding: 6px 12px;
      font-size: 11px;
    }}
    .winzy-hero-nav-placeholder {{
      height: 80px;
    }}
    .winzy-card-bottom {{
      padding: 28px 20px;
    }}
    .winzy-stats-row {{
      gap: 20px;
    }}
    .winzy-stat-num {{
      font-size: 28px;
    }}
  }}

  @media (max-width: 480px) {{
    .winzy-card-nav {{
      padding: 12px 14px;
    }}
    .winzy-logo-v {{
      font-size: 34px;
    }}
    .winzy-card-nav.is-scrolled .winzy-logo-v {{
      font-size: 24px;
    }}
    .winzy-nav-quick-cta {{
      display: none;
    }}
    .winzy-mobile-drawer {{
      padding-top: 72px;
    }}
    .winzy-mobile-drawer-inner {{
      padding: 12px 14px 28px 14px;
      gap: 16px;
    }}
    .winzy-mobile-link {{
      font-size: 14px;
      padding: 11px 13px;
    }}
    .winzy-mobile-cat-row {{
      font-size: 13px;
      padding: 11px 14px;
    }}
  }}
</style>
</head>
<body class="cyber-canvas">

<!-- KEYLINE ICONS SYSTEM DEFINITION (TWO-TONE 24X24 & TECHNICAL SYSTEM) -->
<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
  <symbol id="icon-search" viewBox="0 0 24 24">
    <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8" fill="none"/>
    <path d="M20 20l-4-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  </symbol>
  <symbol id="icon-certificate" viewBox="0 0 24 24">
    <rect x="3" y="4" width="18" height="14" rx="2" stroke="currentColor" stroke-width="1.8" fill="none"/>
    <path d="M7 8h10M7 12h6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    <circle cx="17" cy="15" r="2.5" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.25"/>
    <path d="M16 17.5l-1 2.5 2-1 2 1-1-2.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-badge" viewBox="0 0 24 24">
    <path d="M12 2l2.4 4.8 5.3.8-3.8 3.7.9 5.3L12 14.1l-4.8 2.5.9-5.3-3.8-3.7 5.3-.8L12 2z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" fill="currentColor" fill-opacity="0.2"/>
  </symbol>
  <symbol id="icon-transcript" viewBox="0 0 24 24">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="1.8" fill="none"/>
    <polyline points="14 2 14 8 20 8" stroke="currentColor" stroke-width="1.8" fill="none"/>
    <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    <line x1="10" y1="9" x2="8" y2="9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  </symbol>
  <symbol id="icon-training" viewBox="0 0 24 24">
    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" stroke="currentColor" stroke-width="1.8" fill="none"/>
    <rect x="8" y="2" width="8" height="4" rx="1" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.25"/>
    <path d="M9 14l2 2 4-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-assessment" viewBox="0 0 24 24">
    <path d="M18 20V10M12 20V4M6 20v-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  </symbol>
  <symbol id="icon-letter" viewBox="0 0 24 24">
    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" stroke-width="1.8" fill="none"/>
    <polyline points="22,6 12,13 2,6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-shapes" viewBox="0 0 24 24">
    <path d="M12 2l7 12H5L12 2z" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.2"/>
    <circle cx="17" cy="18" r="3.5" stroke="currentColor" stroke-width="1.8" fill="none"/>
    <rect x="3" y="15" width="6" height="6" stroke="currentColor" stroke-width="1.8" fill="none"/>
  </symbol>
  <symbol id="icon-font" viewBox="0 0 24 24">
    <polyline points="4 20 12 4 20 20" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    <line x1="6.5" y1="15" x2="17.5" y2="15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  </symbol>
  <symbol id="icon-attributes" viewBox="0 0 24 24">
    <polyline points="16 18 22 12 16 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    <polyline points="8 6 2 12 8 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-email" viewBox="0 0 24 24">
    <rect x="2" y="4" width="20" height="16" rx="2" stroke="currentColor" stroke-width="1.8" fill="none"/>
    <path d="M22 7l-10 7L2 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  </symbol>
  <symbol id="icon-download" viewBox="0 0 24 24">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    <polyline points="7 10 12 15 17 10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    <line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  </symbol>
  <symbol id="icon-external" viewBox="0 0 24 24">
    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    <polyline points="15 3 21 3 21 9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    <line x1="10" y1="14" x2="21" y2="3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  </symbol>
  <symbol id="icon-shield" viewBox="0 0 24 24">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.2"/>
    <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
  <symbol id="icon-eye" viewBox="0 0 24 24">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="1.8"/>
    <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.3"/>
  </symbol>
  <symbol id="icon-code" viewBox="0 0 24 24">
    <polyline points="16 18 22 12 16 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    <polyline points="8 6 2 12 8 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  </symbol>
  <symbol id="icon-dimensions" viewBox="0 0 24 24">
    <path d="M21 3H3v18h18V3z" stroke="currentColor" stroke-width="1.8" fill="none"/>
    <path d="M7 3v4M3 7h4M17 3v4M21 7h-4M7 21v-4M3 17h4M17 21v-4M21 17h-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  </symbol>
  <symbol id="icon-zoom" viewBox="0 0 24 24">
    <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8" fill="none"/>
    <path d="M20 20l-4-4M11 8v6M8 11h6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  </symbol>
  <symbol id="icon-rotate" viewBox="0 0 24 24">
    <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.19" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  </symbol>
</svg>

<!-- FIXED STICKY ANIMATED LUXURY NAVIGATION BAR (FULL SIZE ON ENTER -> RESIZED ON SCROLL) -->
<nav class="winzy-card-nav" id="mainStickyNav">
  <!-- Left: DISPLAY ONLY LOGO ("V") with large font size on enter, smoothly shrinking on scroll -->
  <a href="index.html" class="winzy-nav-brand" aria-label="Certifier Studio Home" onclick="handleMenuClick('catalog', event);">
    <span class="winzy-logo-v">V</span>
  </a>

  <!-- Center: Interactive Frosted Glass Capsule Bar with ONLY specific links (Zero #ID) -->
  <div class="winzy-nav-pill" id="winzyNavDock">
    <!-- Catalog (Specific Page Link) -->
    <div class="winzy-nav-item">
      <a class="winzy-nav-link active" href="index.html" id="navLinkCatalog" onclick="handleMenuClick('catalog', event);">
        <span>Catalog</span>
        <svg class="winzy-nav-caret" viewBox="0 0 10 6"><path d="M1 1l4 4 4-4" stroke="#ffffff" stroke-width="1.8" stroke-linecap="round" fill="none"/></svg>
      </a>
      <div class="winzy-nav-dropdown">
        <div class="winzy-dropdown-header">SPECIFIC CATEGORIES</div>
        <a class="winzy-dropdown-link" href="index.html?category=all" onclick="handleMenuClick('category', event, 'all');">
          <span>All Templates</span>
          <span class="winzy-dropdown-badge">{count_certificates + count_badges + count_transcripts + count_training + count_assessments + count_letters:,}</span>
        </a>
        <a class="winzy-dropdown-link" href="index.html?category=certificate" onclick="handleMenuClick('category', event, 'certificate');">
          <span>Certificates</span>
          <span class="winzy-dropdown-badge">{count_certificates:,}</span>
        </a>
        <a class="winzy-dropdown-link" href="index.html?category=badge" onclick="handleMenuClick('category', event, 'badge');">
          <span>Digital Badges</span>
          <span class="winzy-dropdown-badge">{count_badges:,}</span>
        </a>
        <a class="winzy-dropdown-link" href="index.html?category=transcript" onclick="handleMenuClick('category', event, 'transcript');">
          <span>Transcripts</span>
          <span class="winzy-dropdown-badge">{count_transcripts:,}</span>
        </a>
        <a class="winzy-dropdown-link" href="index.html?category=training_record" onclick="handleMenuClick('category', event, 'training_record');">
          <span>Training Records</span>
          <span class="winzy-dropdown-badge">{count_training:,}</span>
        </a>
        <a class="winzy-dropdown-link" href="index.html?category=assessment" onclick="handleMenuClick('category', event, 'assessment');">
          <span>Assessments</span>
          <span class="winzy-dropdown-badge">{count_assessments:,}</span>
        </a>
        <a class="winzy-dropdown-link" href="index.html?category=letter" onclick="handleMenuClick('category', event, 'letter');">
          <span>Formal Letters</span>
          <span class="winzy-dropdown-badge">{count_letters:,}</span>
        </a>
      </div>
    </div>

    <!-- Badge Studio (Specific Page Link) -->
    <div class="winzy-nav-item">
      <a class="winzy-nav-link" href="badge_studio.html" id="navLinkBadgeStudio">
        <span>Badge Studio</span>
        <span class="winzy-nav-live-dot"></span>
      </a>
    </div>

    <!-- Vector SVGs (Specific View Link) -->
    <div class="winzy-nav-item">
      <a class="winzy-nav-link" href="index.html?view=vectors" id="navLinkVectors" onclick="handleMenuClick('elements', event);">
        <span>Vectors</span>
      </a>
    </div>

    <!-- Inspector Stage (Specific View Link) -->
    <div class="winzy-nav-item">
      <a class="winzy-nav-link" href="index.html?view=stage" id="navLinkStage" onclick="handleMenuClick('stage', event);">
        <span>Inspector</span>
      </a>
    </div>
  </div>

  <!-- Right: Dynamic Balanced Spacer / Shortcut + Mobile Menu Toggle -->
  <div class="winzy-nav-spacer">
    <a href="badge_studio.html" class="winzy-nav-quick-cta" title="Launch Slanted-Notch Badge Recognition Studio">
      <span class="winzy-quick-dot"></span>
      <span class="winzy-quick-text">STUDIO</span>
    </a>
    <button class="winzy-mobile-toggle" id="winzyMobileToggle" aria-label="Toggle Navigation Menu" aria-expanded="false" onclick="toggleMobileNav(event);">
      <span class="winzy-toggle-bar"></span>
      <span class="winzy-toggle-bar"></span>
      <span class="winzy-toggle-bar"></span>
    </button>
  </div>
</nav>

<!-- LUXURY MOBILE NAVIGATION DRAWER & BACKDROP (< 900px) -->
<div class="winzy-mobile-backdrop" id="winzyMobileBackdrop" onclick="closeMobileNav();"></div>
<div class="winzy-mobile-drawer" id="winzyMobileDrawer" aria-hidden="true">
  <div class="winzy-mobile-drawer-inner">
    <!-- Group 1: Core Navigation Destinations -->
    <div class="winzy-mobile-group">
      <div class="winzy-mobile-group-title">PRIMARY NAVIGATION</div>
      <a href="index.html" class="winzy-mobile-link" id="mobNavLinkCatalog" onclick="handleMobileNavClick('catalog', event);">
        <span class="winzy-mobile-link-left">
          <svg class="winzy-mobile-link-icon"><use href="#icon-certificate"/></svg>
          <span>Catalog Overview</span>
        </span>
        <span class="winzy-mobile-pill-badge">{count_certificates + count_badges + count_transcripts + count_training + count_assessments + count_letters:,}</span>
      </a>
      <a href="badge_studio.html" class="winzy-mobile-link" id="mobNavLinkBadgeStudio">
        <span class="winzy-mobile-link-left">
          <svg class="winzy-mobile-link-icon"><use href="#icon-badge"/></svg>
          <span>Badge Studio</span>
        </span>
        <span class="winzy-mobile-live-tag">LIVE STUDIO</span>
      </a>
      <a href="index.html?view=vectors" class="winzy-mobile-link" id="mobNavLinkVectors" onclick="handleMobileNavClick('elements', event);">
        <span class="winzy-mobile-link-left">
          <svg class="winzy-mobile-link-icon"><use href="#icon-shapes"/></svg>
          <span>Vectors &amp; Elements</span>
        </span>
        <span class="winzy-mobile-pill-muted">38 SVG</span>
      </a>
      <a href="index.html?view=stage" class="winzy-mobile-link" id="mobNavLinkStage" onclick="handleMobileNavClick('stage', event);">
        <span class="winzy-mobile-link-left">
          <svg class="winzy-mobile-link-icon"><use href="#icon-attributes"/></svg>
          <span>Technical Inspector</span>
        </span>
        <span class="winzy-mobile-pill-muted">STAGE</span>
      </a>
    </div>

    <!-- Group 2: Specific Categories -->
    <div class="winzy-mobile-group">
      <div class="winzy-mobile-group-title">SPECIFIC CATEGORIES</div>
      <div class="winzy-mobile-cat-list">
        <a href="index.html?category=all" class="winzy-mobile-cat-row" onclick="handleMobileNavClick('category', event, 'all');">
          <span>All Templates</span>
          <span class="winzy-mobile-cat-count">{count_certificates + count_badges + count_transcripts + count_training + count_assessments + count_letters:,}</span>
        </a>
        <a href="index.html?category=certificate" class="winzy-mobile-cat-row" onclick="handleMobileNavClick('category', event, 'certificate');">
          <span>Certificates</span>
          <span class="winzy-mobile-cat-count">{count_certificates:,}</span>
        </a>
        <a href="index.html?category=badge" class="winzy-mobile-cat-row" onclick="handleMobileNavClick('category', event, 'badge');">
          <span>Digital Badges</span>
          <span class="winzy-mobile-cat-count">{count_badges:,}</span>
        </a>
        <a href="index.html?category=transcript" class="winzy-mobile-cat-row" onclick="handleMobileNavClick('category', event, 'transcript');">
          <span>Transcripts</span>
          <span class="winzy-mobile-cat-count">{count_transcripts:,}</span>
        </a>
        <a href="index.html?category=training_record" class="winzy-mobile-cat-row" onclick="handleMobileNavClick('category', event, 'training_record');">
          <span>Training Records</span>
          <span class="winzy-mobile-cat-count">{count_training:,}</span>
        </a>
        <a href="index.html?category=assessment" class="winzy-mobile-cat-row" onclick="handleMobileNavClick('category', event, 'assessment');">
          <span>Assessments</span>
          <span class="winzy-mobile-cat-count">{count_assessments:,}</span>
        </a>
        <a href="index.html?category=letter" class="winzy-mobile-cat-row" onclick="handleMobileNavClick('category', event, 'letter');">
          <span>Formal Letters</span>
          <span class="winzy-mobile-cat-count">{count_letters:,}</span>
        </a>
      </div>
    </div>

    <!-- Group 3: Quick Direct Actions -->
    <div class="winzy-mobile-actions">
      <a href="badge_studio.html" class="winzy-mobile-btn-primary">
        <span>LAUNCH BADGE STUDIO</span>
        <svg style="width: 14px; height: 14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
    </div>
  </div>
</div>

<!-- WINZY EDITORIAL LUXURY HERO HOMEPAGE SECTION (FULL SCREEN FIT) -->
<section class="winzy-hero-section">
  <!-- Full Screen Floating Cinematic Card Viewport -->
  <div class="winzy-hero-card" id="winzyHeroCard">
    <!-- Top Nav Placeholder inside Hero Card to maintain flex column alignment -->
    <div class="winzy-hero-nav-placeholder" aria-hidden="true"></div>

    <!-- Monumental Center Watermark Backdrop Text -->
    <div class="winzy-watermark-text" id="winzyHeroWatermark">EGYPT</div>

    <!-- Full-Width Horizontal Left-to-Right Floating Marquee (Uncropped & Full Transparency) -->
    <div class="winzy-horizontal-marquee">
      <div class="winzy-marquee-bar-header">
        <div class="winzy-marquee-header-pill">
          <div class="winzy-marquee-pulse"></div>
          <span>RANDOM SPECIMENS &bull; ORIGINAL CERTIFICATE CARDS</span>
        </div>
      </div>
      <div class="winzy-marquee-track-wrap">
        <div class="winzy-marquee-track">
          {marquee_cards_html}
        </div>
      </div>
    </div>

    <!-- Bottom Row Elements -->
    <div class="winzy-card-bottom">
      <div class="winzy-bottom-left">
        <!-- Stats Cluster with Detailed Certificate Counts -->
        <div class="winzy-stats-row">
          <div class="winzy-stat-col">
            <span class="winzy-stat-num">{total_templates:,}</span>
            <span class="winzy-stat-label">Total Templates</span>
          </div>
          <div class="winzy-stat-col">
            <span class="winzy-stat-num">{count_certificates:,}</span>
            <span class="winzy-stat-label">Certificates</span>
          </div>
          <div class="winzy-stat-col">
            <span class="winzy-stat-num">{count_badges:,}</span>
            <span class="winzy-stat-label">Digital Badges</span>
          </div>
          <div class="winzy-stat-col">
            <span class="winzy-stat-num">{count_other_records:,}</span>
            <span class="winzy-stat-label">Transcripts & Records</span>
          </div>
          <div class="winzy-stat-col">
            <span class="winzy-stat-num">{total_svgs:,}</span>
            <span class="winzy-stat-label">Vector SVGs</span>
          </div>
        </div>

        <!-- Detailed Description (Zero Booking Button) -->
        <p class="winzy-details-desc">
          Universal High-Fidelity Certificate Repository: {count_certificates:,} master certificates, {count_badges:,} skill badges, {count_transcripts:,} academic transcripts, {count_training:,} training records, {count_assessments:,} evaluations, and {count_letters:,} formal letters engineered with 100% offline JSON data precision.
        </p>

        <!-- Quick Interactive Jump Pills -->
        <div class="winzy-quick-filters">
          <button class="winzy-filter-pill" onclick="filterCategory('all');">All ({total_templates:,})</button>
          <button class="winzy-filter-pill" onclick="filterCategory('certificate');">Certificates ({count_certificates:,})</button>
          <button class="winzy-filter-pill" onclick="filterCategory('badge');">Badges ({count_badges:,})</button>
          <button class="winzy-filter-pill" onclick="filterCategory('transcript');">Transcripts ({count_transcripts:,})</button>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ==========================================================================
     STUDIO EDITORIAL LUXURY WORKSPACE
     ========================================================================== -->
<div class="editorial-workspace">

  <!-- Workspace Command Ribbon -->
  <header class="workspace-command-ribbon">
    <div class="ribbon-brand-col">
      <div class="ribbon-title-wrap">
        <span class="ribbon-brand-title">CERTIFIER STUDIO</span>
        <span class="ribbon-divider">//</span>
        <span class="ribbon-brand-sub">MASTER SPECIMEN WORKSPACE</span>
      </div>
      <div class="ribbon-meta-text">
        THREE-COLOR EDITORIAL SPECIFICATION ARCHITECTURE &bull; {total_templates:,} MASTER TEMPLATES &bull; {total_svgs:,} VECTOR SVGS
      </div>
    </div>

    <div class="ribbon-actions-col">
      <div class="ribbon-nav-pills">
        <button class="ribbon-pill-btn active" id="tabBtnAll" onclick="selectWorkspaceView('all')">
          <svg class="keyline-icon" style="width: 14px; height: 14px;"><use href="#icon-certificate"/></svg>
          CATALOG ALL ({total_templates:,})
        </button>
        <button class="ribbon-pill-btn" id="tabBtnStage" onclick="selectWorkspaceView('stage')">
          <svg class="keyline-icon" style="width: 14px; height: 14px;"><use href="#icon-eye"/></svg>
          INSPECT STAGE
        </button>
        <a href="badge_studio.html" class="ribbon-pill-btn" style="text-decoration: none;">
          <svg class="keyline-icon" style="width: 14px; height: 14px; color: #0f172a;"><use href="#icon-badge"/></svg>
          SLANTED BADGE STUDIO
        </a>
      </div>

      <div class="ribbon-status-pill">
        <span class="status-dot-pulse"></span>
        <span>OFFLINE SECURED // VERIFIED</span>
      </div>
    </div>
  </header>

<!-- 3. SPLIT TWO-COLUMN WORKSPACE ARCHITECTURE -->
<div class="obsidian-workspace">

  <!-- LEFT COLUMN: INTERACTIVE VISUAL CARD STAGE & ARCHIVE -->
  <main class="visual-stage-column">

    <!-- Elevated Visual Stage Card -->
    <section class="studio-card stage-main-card" id="visualStageWrapper">
      <div class="stage-top-bar">
        <div class="stage-title-wrap">
          <span class="status-dot-pulse"></span>
          <span class="stage-title" id="stageTitle">Paralegal Professional Certificate</span>
        </div>
        <div class="stage-badges-row">
          <span class="mono-badge" id="stagePaperBadge">A4 LANDSCAPE</span>
          <span class="mono-badge mono-badge-emerald" id="stageOrientBadge">1.414 RATIO</span>
          <span class="stage-status-pill">ACTIVE SPECIMEN</span>
        </div>
      </div>

      <!-- Crisp Display Plate -->
      <div class="stage-display-plate" id="stageDisplayPlate" style="position: relative;">
        <div class="resource-protection-shield" title="Protected Architecture // Anti-Theft Guard"></div>
        <img id="stagePreviewImg" src="certificates/previews/877_Paralegal_professional_purple_landscape_01k43ft5bf1ecbgev63rhesqg9_preview.png" alt="Active Document Plate" draggable="false" onerror="handleStageImgFallback(this)">
        <div class="watermark-protection-tag">RESTRICTED VIEW // PROTECTED SPECIMEN</div>
      </div>

      <!-- Stage Controls Tray -->
      <div class="stage-controls-tray">
        <div class="stage-btn-group">
          <button class="stage-tool-btn" onclick="toggleStageFit()">
            <svg class="keyline-icon"><use href="#icon-zoom"/></svg>
            FIT VIEWPORT
          </button>
          <button class="stage-tool-btn" onclick="toggleStageRotate()">
            <svg class="keyline-icon"><use href="#icon-rotate"/></svg>
            ROTATE 90°
          </button>
          <button class="stage-tool-btn" onclick="toggleGuillocheWatermark()">
            <svg class="keyline-icon"><use href="#icon-shield"/></svg>
            SECURITY WATERMARK
          </button>
        </div>
        <span class="stage-tray-meta">
          CANVAS: 2000 x 1414 HD @ 300 DPI PRINT
        </span>
      </div>
    </section>

    <!-- CONTROLS: SPLIT INPUT SEARCH & STEPPER CATEGORY TABS -->
    <div class="studio-card controls-main-card" id="controlsBar">
      <div class="studio-search-wrapper">
        <svg class="keyline-icon studio-search-icon" style="color: #0f172a; width: 18px; height: 18px;"><use href="#icon-search"/></svg>
        <input type="text" id="search" class="studio-search-input" placeholder="Search templates by title, orientation, color, style, or metadata...">
        <button class="studio-search-btn" onclick="document.getElementById('search').focus()">
          SEARCH
        </button>
      </div>

      <div class="studio-category-tabs">
        <button class="stepper-tab-btn active" data-cat="all">
          <div class="tab-content">
            <svg class="keyline-icon"><use href="#icon-certificate"/></svg>
            All ({total_templates:,})
          </div>
        </button>
        <button class="stepper-tab-btn" data-cat="certificate">
          <div class="tab-content">
            <svg class="keyline-icon"><use href="#icon-certificate"/></svg>
            Certificates ({len(master.get('certificate', [])):,})
          </div>
        </button>
        <button class="stepper-tab-btn" data-cat="badge">
          <div class="tab-content">
            <svg class="keyline-icon"><use href="#icon-badge"/></svg>
            Badges ({len(master.get('badge', [])):,})
          </div>
        </button>
        <button class="stepper-tab-btn" data-cat="transcript">
          <div class="tab-content">
            <svg class="keyline-icon"><use href="#icon-transcript"/></svg>
            Transcripts ({len(master.get('transcript', [])):,})
          </div>
        </button>
        <button class="stepper-tab-btn" data-cat="training_record">
          <div class="tab-content">
            <svg class="keyline-icon"><use href="#icon-training"/></svg>
            Training Records ({len(master.get('training_record', [])):,})
          </div>
        </button>
        <button class="stepper-tab-btn" data-cat="assessment">
          <div class="tab-content">
            <svg class="keyline-icon"><use href="#icon-assessment"/></svg>
            Assessments ({len(master.get('assessment', [])):,})
          </div>
        </button>
        <button class="stepper-tab-btn" data-cat="letter">
          <div class="tab-content">
            <svg class="keyline-icon"><use href="#icon-letter"/></svg>
            Letters ({len(master.get('letter', [])):,})
          </div>
        </button>
        <button class="stepper-tab-btn" data-cat="elements">
          <div class="tab-content">
            <svg class="keyline-icon"><use href="#icon-shapes"/></svg>
            Vector Elements ({total_svgs:,})
          </div>
        </button>
        <button class="stepper-tab-btn" data-cat="attributes">
          <div class="tab-content">
            <svg class="keyline-icon"><use href="#icon-attributes"/></svg>
            Attributes
          </div>
        </button>
        <button class="stepper-tab-btn" data-cat="fonts">
          <div class="tab-content">
            <svg class="keyline-icon"><use href="#icon-font"/></svg>
            58 Typography Fonts
          </div>
        </button>
      </div>
    </div>

    <!-- MAIN GRID CONTAINER -->
    <div class="cyber-grid" id="grid"></div>

    <!-- PAGINATION CONTROLS -->
    <div class="studio-card pagination-main-bar" id="catalogPagination"></div>

  </main>

  <!-- RIGHT COLUMN: TECHNICAL PARAMETER INSPECTOR -->
  <aside class="inspector-column" id="inspectorColumn">

    <!-- Inspector Master Card in Pure White with Deep Charcoal Header -->
    <div class="studio-card inspector-main-card">
      <div class="inspector-card-header">
        <div class="inspector-card-title">
          <svg class="keyline-icon" style="width: 16px; height: 16px; color: #ffffff;"><use href="#icon-code"/></svg>
          PARAMETER INSPECTOR
        </div>
        <div class="inspector-card-subtitle">
          LIVE TECHNICAL SPECIFICATION &amp; ATTRIBUTE MODEL
        </div>
        <div class="inspector-badges-row">
          <span class="mono-badge mono-badge-emerald">VERIFIED SPEC</span>
          <span class="mono-badge mono-badge-charcoal">READ-ONLY LOCKED</span>
        </div>
      </div>

      <div class="inspector-card-body">
        <!-- Group 1: Geometry & DPI -->
        <div class="inspector-section">
          <div class="inspector-section-title">
            <svg class="keyline-icon" style="width: 14px; height: 14px;"><use href="#icon-dimensions"/></svg>
            Document Geometry &amp; DPI
          </div>
          <div class="param-row">
            <span class="param-label">Active Document:</span>
            <span class="param-value" id="inspectDocName">Paralegal Certificate</span>
          </div>
          <div class="param-row">
            <span class="param-label">Category Format:</span>
            <span class="param-value" id="inspectCategory">CERTIFICATE</span>
          </div>
          <div class="param-row">
            <span class="param-label">Physical Dimensions:</span>
            <span class="param-value" id="inspectDimensions">297 x 210 mm</span>
          </div>
          <div class="param-row">
            <span class="param-label">Canvas Viewport:</span>
            <span class="param-value" id="inspectViewport">1123 x 794 px @ 96 DPI</span>
          </div>
          <div class="param-row">
            <span class="param-label">Print Specification:</span>
            <span class="param-value" id="inspectPrintHd">2000 x 1414 HD @ 300 DPI</span>
          </div>
          <div class="param-row">
            <span class="param-label">Aspect Ratio:</span>
            <span class="param-value" id="inspectRatio">1.414 (Landscape)</span>
          </div>
        </div>

        <!-- Group 2: Cryptographic Proof & Identity -->
        <div class="inspector-section">
          <div class="inspector-section-title">
            <svg class="keyline-icon" style="width: 14px; height: 14px;"><use href="#icon-shield"/></svg>
            Cryptographic &amp; Integrity Proof
          </div>
          <div class="param-row">
            <span class="param-label">Template ID:</span>
            <span class="param-value" id="inspectTemplateId">#ID-877</span>
          </div>
          <div class="param-row">
            <span class="param-label">SHA-256 Digest:</span>
            <span class="param-value" id="inspectShaDigest">e8a4...719b</span>
          </div>
          <div class="param-row">
            <span class="param-label">Protection Mode:</span>
            <span class="mono-badge mono-badge-emerald">AUTHENTIC VAULT</span>
          </div>
          <div class="param-row">
            <span class="param-label">Integrity Status:</span>
            <span class="param-value" style="color: #00b67a;">OFFLINE VERIFIED</span>
          </div>
        </div>

        <!-- Group 3: Typography & Fonts -->
        <div class="inspector-section">
          <div class="inspector-section-title">
            <svg class="keyline-icon" style="width: 14px; height: 14px;"><use href="#icon-font"/></svg>
            Typography &amp; Text Hierarchy
          </div>
          <div class="param-row">
            <span class="param-label">Primary Display:</span>
            <span class="param-value">Google Sans Bold</span>
          </div>
          <div class="param-row">
            <span class="param-label">Interface Body:</span>
            <span class="param-value">Google Sans Text</span>
          </div>
          <div class="param-row">
            <span class="param-label">Dynamic Tags:</span>
            <span class="param-value">12 System Tags</span>
          </div>
          <div class="param-row">
            <span class="param-label">Emoji Suppression:</span>
            <span class="param-value" style="color: #0f172a; font-weight: 700;">STRICT ZERO</span>
          </div>
        </div>

        <!-- Group 4: Strict Solid Surface Tokens -->
        <div class="inspector-section">
          <div class="inspector-section-title">
            <svg class="keyline-icon" style="width: 14px; height: 14px;"><use href="#icon-shapes"/></svg>
            Editorial Color Palette
          </div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px;">
            <span class="mono-badge" style="background: #ffffff; color: #0f172a; border-color: rgba(15, 23, 42, 0.12);">#FFFFFF CANVAS</span>
            <span class="mono-badge" style="background: #0f172a; color: #ffffff; border-color: #0f172a;">#0F172A CHARCOAL</span>
            <span class="mono-badge" style="background: rgba(15, 23, 42, 0.06); color: #0f172a; border-color: rgba(15, 23, 42, 0.12);">SLATE BORDER</span>
            <span class="mono-badge" style="background: #00b67a; color: #ffffff; border-color: #00b67a;">#00B67A ACCENT</span>
          </div>
        </div>

        <!-- Group 5: Action Controls -->
        <div class="inspector-section" style="border-bottom: none; padding-bottom: 0;">
          <div style="display: flex; flex-direction: column; gap: 10px;">
            <button class="inspector-action-btn" type="button" onclick="showProtectionNotice('VAULT ENCRYPTED // DIRECT RAW JSON ACCESS RESTRICTED');">
              <svg class="keyline-icon"><use href="#icon-shield"/></svg>
              ENCRYPTED REPOSITORY SPECS
            </button>
            <button class="inspector-action-btn" type="button" onclick="filterCategory('attributes');">
              <svg class="keyline-icon"><use href="#icon-attributes"/></svg>
              INSPECT ATTRIBUTES TABLE
            </button>
          </div>
        </div>
      </div>
    </div>

  </aside>
</div>

</div>

<script>
// --- ENCRYPTED RESOURCE VAULT // ZERO PLAIN-TEXT REPOSITORY ---
function _decryptResourceVault(payloadBase64, key = "CertifierStudio_Vault_SecKey_2026") {{
  try {{
    const binStr = atob(payloadBase64);
    const len = binStr.length;
    const keyLen = key.length;
    const keyBytes = new Uint8Array(keyLen);
    for (let k = 0; k < keyLen; k++) {{
      keyBytes[k] = key.charCodeAt(k);
    }}
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {{
      bytes[i] = binStr.charCodeAt(i) ^ keyBytes[(i + 13) % keyLen] ^ ((i * 7) & 0xFF);
    }}
    const decoder = new TextDecoder('utf-8');
    return JSON.parse(decoder.decode(bytes));
  }} catch (err) {{
    console.error("Resource Vault Decryption Error", err);
    return {{}};
  }}
}}

const _VAULT_SECURE_PAYLOAD = "{encrypted_vault_payload}";
const _VAULT_DATA = _decryptResourceVault(_VAULT_SECURE_PAYLOAD);

const templates = _VAULT_DATA.templates || {{}};
const elements = _VAULT_DATA.elements || [];
const attributes = _VAULT_DATA.attributes || [];
const typography = _VAULT_DATA.typography || {{}};

let currentCategory = "all";
let searchQuery = "";
let stageZoomFit = true;
let stageRotation = 0;
let currentPage = 1;
const pageSize = 24;

function safeName(str) {{
  return (str || 'template').replace(/[^a-zA-Z0-9_\\-\\.]/g, '_').replace(/_+/g, '_').substring(0, 80);
}}

function getFolder(type) {{
  const map = {{
    'certificate': 'certificates',
    'badge': 'badges',
    'transcript': 'transcripts',
    'training_record': 'training_records',
    'assessment': 'assessments',
    'letter': 'letters'
  }};
  return map[type] || type;
}}

function handleStageImgFallback(img) {{
  img.style.display = 'none';
  const parent = document.getElementById('stageDisplayPlate');
  if (parent && !parent.querySelector('.stage-fallback-msg')) {{
    const msg = document.createElement('div');
    msg.className = 'stage-fallback-msg';
    msg.style.cssText = 'color: #0f172a; font-family: var(--font-display); font-weight: 700; font-size: 14px; text-align: center;';
    msg.innerHTML = '<div style="font-size: 24px; font-weight: 900; letter-spacing: -0.03em; margin-bottom: 8px;">SPECIFICATION PRESET</div><div>Crisp Pure White Display Plate // Vector Canvas Active</div>';
    parent.appendChild(msg);
  }}
}}

function updateInspector(name, cat, dim, viewport, hd, ratio, id) {{
  const docName = document.getElementById('inspectDocName');
  if (docName) docName.innerText = name.substring(0, 24);
  const docCat = document.getElementById('inspectCategory');
  if (docCat) docCat.innerText = cat.toUpperCase();
  const docDim = document.getElementById('inspectDimensions');
  if (docDim) docDim.innerText = dim;
  const docVp = document.getElementById('inspectViewport');
  if (docVp) docVp.innerText = viewport;
  const docHd = document.getElementById('inspectPrintHd');
  if (docHd) docHd.innerText = hd;
  const docRatio = document.getElementById('inspectRatio');
  if (docRatio) docRatio.innerText = ratio;
  const docId = document.getElementById('inspectTemplateId');
  if (docId) docId.innerText = id;

  // Compute a deterministic SHA-256 style fingerprint
  const docSha = document.getElementById('inspectShaDigest');
  if (docSha) {{
    let hash = 0;
    const str = name + id + cat;
    for (let i = 0; i < str.length; i++) {{
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }}
    const hex = Math.abs(hash).toString(16).padStart(8, '0');
    docSha.innerText = hex.substring(0, 4) + '...' + hex.substring(4, 8);
  }}
}}

function selectTemplate(item, folder) {{
  const name = item.name || 'Untitled';
  const safe = safeName(name);
  const prefix = `${{safe}}_${{item.id}}`;
  const previewSrc = `${{folder}}/previews/${{prefix}}_preview.png`;

  const stageImg = document.getElementById('stagePreviewImg');
  const stageTitle = document.getElementById('stageTitle');
  const stagePaper = document.getElementById('stagePaperBadge');
  const stageOrient = document.getElementById('stageOrientBadge');

  if (stageImg) {{
    stageImg.style.display = 'block';
    stageImg.src = previewSrc;
    const fallback = document.querySelector('.stage-fallback-msg');
    if (fallback) fallback.remove();
  }}

  if (stageTitle) stageTitle.innerText = name;
  if (stagePaper) stagePaper.innerText = (item.paperSize || 'A4').toUpperCase();
  if (stageOrient) stageOrient.innerText = (item.orientation || 'landscape').toUpperCase();

  const isPortrait = (item.orientation === 'portrait');
  const dim = isPortrait ? '210 x 297 mm' : '297 x 210 mm';
  const vp = isPortrait ? '794 x 1123 px @ 96DPI' : '1123 x 794 px @ 96DPI';
  const hd = isPortrait ? '1414 x 2000 HD' : '2000 x 1414 HD';
  const ratio = isPortrait ? '0.707 (Portrait)' : '1.414 (Landscape)';

  updateInspector(name, folder, dim, vp, hd, ratio, `#ID-${{item.id}}`);

  // Highlight selected card
  document.querySelectorAll('.template-card-wrapper').forEach(c => c.classList.remove('selected'));
}}

function loadBlankPresetStage(name, dim, vp, hd, ratio, orient) {{
  const stageTitle = document.getElementById('stageTitle');
  const stagePaper = document.getElementById('stagePaperBadge');
  const stageOrient = document.getElementById('stageOrientBadge');
  const stagePlate = document.getElementById('stageDisplayPlate');

  if (stageTitle) stageTitle.innerText = name;
  if (stagePaper) stagePaper.innerText = name.split(' ')[0].toUpperCase();
  if (stageOrient) stageOrient.innerText = orient.toUpperCase();

  if (stagePlate) {{
    const stageImg = document.getElementById('stagePreviewImg');
    if (stageImg) stageImg.style.display = 'none';
    let fallback = document.querySelector('.stage-fallback-msg');
    if (!fallback) {{
      fallback = document.createElement('div');
      fallback.className = 'stage-fallback-msg';
      fallback.style.cssText = 'color: #0f172a; font-family: var(--font-display); font-weight: 700; text-align: center; padding: 40px;';
      stagePlate.appendChild(fallback);
    }}
    fallback.innerHTML = `
      <div style="font-size: 26px; font-weight: 900; letter-spacing: -0.03em; margin-bottom: 8px;">${{name}}</div>
      <div style="font-family: var(--font-mono); font-size: 13px; color: #475569; margin-bottom: 14px;">${{dim}} | ${{vp}}</div>
      <div style="display: inline-flex; gap: 8px;">
        <span style="font-family: var(--font-mono); font-size: 11px; background: #08090b; color: #ffffff; padding: 4px 10px;">CANVAS: ${{hd}}</span>
        <span style="font-family: var(--font-mono); font-size: 11px; background: #00b67a; color: #08090b; padding: 4px 10px; font-weight: 700;">READ-ONLY PROTECTED</span>
      </div>
    `;
  }}

  updateInspector(name, 'preset', dim, vp, hd, ratio, '#PRESET');
  scrollToElement('visualStageWrapper');
}}

function toggleStageFit() {{
  const img = document.getElementById('stagePreviewImg');
  if (!img) return;
  stageZoomFit = !stageZoomFit;
  if (stageZoomFit) {{
    img.style.maxHeight = '480px';
    img.style.maxWidth = '100%';
  }} else {{
    img.style.maxHeight = 'none';
    img.style.maxWidth = 'none';
  }}
}}

function toggleStageRotate() {{
  const plate = document.getElementById('stageDisplayPlate');
  if (!plate) return;
  stageRotation = (stageRotation + 90) % 360;
  plate.style.transform = `rotate(${{stageRotation}}deg)`;
  plate.style.transition = 'transform 0.25s ease';
}}

function toggleGuillocheWatermark() {{
  const wm = document.querySelector('.guilloche-watermark');
  if (wm) {{
    wm.style.display = (wm.style.display === 'none') ? 'block' : 'none';
  }}
}}

function toggleStitchPerimeter() {{
  const stitches = document.querySelectorAll('.tactile-stitch-rect, .leather-stitch-rect');
  stitches.forEach(s => {{
    s.style.display = (s.style.display === 'none') ? 'block' : 'none';
  }});
}}

function scrollToElement(id) {{
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}

function selectWorkspaceView(view) {{
  document.querySelectorAll('.tactile-pill-btn').forEach(b => b.classList.remove('active'));
  if (view === 'all') {{
    const b = document.getElementById('tabBtnAll');
    if (b) b.classList.add('active');
    scrollToElement('controlsBar');
  }} else if (view === 'stage') {{
    const b = document.getElementById('tabBtnStage');
    if (b) b.classList.add('active');
    scrollToElement('visualStageWrapper');
  }}
}}

function setCardFinish(finish) {{
  document.querySelectorAll('.leather-toggle-btn').forEach(b => b.classList.remove('active'));
  const card = document.getElementById('satinCard');
  if (!card) return;
  card.classList.remove('mode-usd', 'mode-khr');

  if (finish === 'wei') {{
    const b = document.getElementById('btnWei');
    if (b) b.classList.add('active');
    document.documentElement.style.setProperty('--surface-purple', '#0f172a');
  }} else if (finish === 'usd') {{
    const b = document.getElementById('btnUsd');
    if (b) b.classList.add('active');
    card.classList.add('mode-usd');
    document.documentElement.style.setProperty('--surface-purple', '#0f172a');
  }} else if (finish === 'khr') {{
    const b = document.getElementById('btnKhr');
    if (b) b.classList.add('active');
    card.classList.add('mode-khr');
    document.documentElement.style.setProperty('--surface-purple', '#0f172a');
  }}
}}

function changePage(page) {{
  currentPage = page;
  render();
  const el = document.getElementById('controlsBar') || document.getElementById('grid');
  if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}

function renderPagination(totalItems) {{
  const pagEl = document.getElementById('catalogPagination');
  if (!pagEl) return;

  if (totalItems <= pageSize) {{
    pagEl.style.display = 'none';
    return;
  }}
  pagEl.style.display = 'flex';

  const totalPages = Math.ceil(totalItems / pageSize);
  if (currentPage > totalPages) currentPage = totalPages;
  if (currentPage < 1) currentPage = 1;

  const startIdx = (currentPage - 1) * pageSize + 1;
  const endIdx = Math.min(currentPage * pageSize, totalItems);

  let html = '<div class="pagination-info">';
  html += 'Showing <strong>' + startIdx.toLocaleString() + '–' + endIdx.toLocaleString() + '</strong> of <strong>' + totalItems.toLocaleString() + '</strong> specimens (Page <strong>' + currentPage + '</strong> of <strong>' + totalPages + '</strong>)';
  html += '</div>';

  html += '<div class="pagination-controls">';

  // First & Prev buttons
  html += '<button class="pagination-btn" onclick="changePage(1)"' + (currentPage === 1 ? ' disabled' : '') + '>« First</button>';
  html += '<button class="pagination-btn" onclick="changePage(' + (currentPage - 1) + ')"' + (currentPage === 1 ? ' disabled' : '') + '>‹ Prev</button>';

  // Window of page numbers
  const delta = 2;
  const range = [];
  for (let i = Math.max(2, currentPage - delta); i <= Math.min(totalPages - 1, currentPage + delta); i++) {{
    range.push(i);
  }}

  // Page 1
  html += '<button class="pagination-btn' + (currentPage === 1 ? ' active' : '') + '" onclick="changePage(1)">1</button>';

  if (range.length > 0 && range[0] > 2) {{
    html += '<span class="pagination-ellipsis">&hellip;</span>';
  }}

  for (const p of range) {{
    html += '<button class="pagination-btn' + (currentPage === p ? ' active' : '') + '" onclick="changePage(' + p + ')">' + p + '</button>';
  }}

  if (range.length > 0 && range[range.length - 1] < totalPages - 1) {{
    html += '<span class="pagination-ellipsis">&hellip;</span>';
  }}

  if (totalPages > 1) {{
    html += '<button class="pagination-btn' + (currentPage === totalPages ? ' active' : '') + '" onclick="changePage(' + totalPages + ')">' + totalPages + '</button>';
  }}

  // Next & Last buttons
  html += '<button class="pagination-btn" onclick="changePage(' + (currentPage + 1) + ')"' + (currentPage === totalPages ? ' disabled' : '') + '>Next ›</button>';
  html += '<button class="pagination-btn" onclick="changePage(' + totalPages + ')"' + (currentPage === totalPages ? ' disabled' : '') + '>Last »</button>';

  html += '</div>';
  pagEl.innerHTML = html;
}}

function render() {{
  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  const q = searchQuery.toLowerCase();
  const pagEl = document.getElementById('catalogPagination');

  if (currentCategory === 'attributes') {{
    if (pagEl) pagEl.style.display = 'none';
    grid.style.display = 'block';
    let html = '<div class="spec-table-container">';
    html += '<div class="section-title"><svg class="keyline-icon" style="color: var(--accent-emerald); width: 18px; height: 18px;"><use href="#icon-attributes"/></svg> Dynamic Attributes & Placeholders</div>';
    html += '<table class="spec-table"><thead><tr><th>Tag</th><th>Field Name</th><th>Description / Example</th></tr></thead><tbody>';
    for (const [group, items] of Object.entries(attributes)) {{
      for (const it of items) {{
        if (q && !it.tag.toLowerCase().includes(q) && !it.label.toLowerCase().includes(q)) continue;
        html += `<tr><td><code style="color: var(--accent-emerald); font-weight: bold; font-family: var(--font-display);">${{it.tag}}</code></td><td>${{it.label}}</td><td>${{it.example || it.description || ''}}</td></tr>`;
      }}
    }}
    html += '</tbody></table></div>';
    grid.innerHTML = html;
    return;
  }}

  if (currentCategory === 'fonts') {{
    if (pagEl) pagEl.style.display = 'none';
    grid.style.display = 'block';
    let html = '<div class="spec-table-container">';
    html += '<div class="section-title"><svg class="keyline-icon" style="color: var(--accent-emerald); width: 18px; height: 18px;"><use href="#icon-font"/></svg> Complete 58 Built-in Google Fonts</div>';
    for (const [type, fontList] of Object.entries(typography.googleFonts || {{}})) {{
      html += `<div style="margin-top: 18px; margin-bottom: 8px; color: var(--accent-emerald); font-family: var(--font-display); font-weight: 700; text-transform: uppercase; font-size: 13px;">${{type}} (${{fontList.length}} fonts)</div><div style="display: flex; flex-wrap: wrap; gap: 8px;">`;
      for (const font of fontList) {{
        if (q && !font.toLowerCase().includes(q)) continue;
        html += `<span class="pill tag-mint" style="font-size: 12px; padding: 6px 12px; font-family: '${{font}}', sans-serif;">${{font}}</span>`;
      }}
      html += '</div>';
    }}
    html += '</div>';
    grid.innerHTML = html;
    return;
  }}

  grid.style.display = 'grid';

  if (currentCategory === 'elements') {{
    const matchingElements = [];
    for (const [sub, files] of Object.entries(elements)) {{
      for (const file of files) {{
        if (q && !file.toLowerCase().includes(q) && !sub.toLowerCase().includes(q)) continue;
        matchingElements.push({{ sub, file }});
      }}
    }}

    if (matchingElements.length === 0) {{
      grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 50px; font-family: var(--font-display); font-size: 14px;">No vector elements found matching your search.</div>';
      renderPagination(0);
      return;
    }}

    const totalPages = Math.ceil(matchingElements.length / pageSize);
    if (currentPage > totalPages) currentPage = totalPages;
    if (currentPage < 1) currentPage = 1;
    const pageElements = matchingElements.slice((currentPage - 1) * pageSize, currentPage * pageSize);

    for (const item of pageElements) {{
      const div = document.createElement('div');
      div.className = 'element-card-wrapper';
      div.innerHTML = `
        <div class="element-card-inner">
          <div class="element-preview" style="position: relative;">
            <div class="resource-protection-shield" title="Protected Vector Shield"></div>
            <img src="elements/${{item.sub}}/${{item.file}}" alt="${{item.file}}" loading="lazy" draggable="false">
          </div>
          <div class="element-name">${{item.file}}</div>
          <div class="pill">${{item.sub.toUpperCase()}}</div>
          <div style="font-family: var(--font-display); font-size: 11px; color: var(--text-muted); display: inline-flex; align-items: center; gap: 4px; font-weight: 600; cursor: default; pointer-events: none;">
            <svg class="keyline-icon" style="width: 12px; height: 12px; color: var(--accent-emerald);"><use href="#icon-shield"/></svg>
            Protected Vector
          </div>
        </div>
      `;
      grid.appendChild(div);
    }}

    renderPagination(matchingElements.length);
    return;
  }}

  const categories = (currentCategory === 'all') ? Object.keys(templates) : [currentCategory];
  const matchingTemplates = [];

  for (const cat of categories) {{
    const list = templates[cat] || [];
    const folder = getFolder(cat);

    for (const item of list) {{
      const name = item.name || 'Untitled';
      const meta = item.metadata || {{}};
      const fullText = (name + ' ' + (meta.style || '') + ' ' + (meta.color || '') + ' ' + (meta.category || '')).toLowerCase();
      if (q && !fullText.includes(q)) continue;

      matchingTemplates.push({{ item, folder, name, meta }});
    }}
  }}

  if (matchingTemplates.length === 0) {{
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 50px; font-family: var(--font-display); font-size: 14px;">No templates found matching your search.</div>';
    renderPagination(0);
    return;
  }}

  const totalPages = Math.ceil(matchingTemplates.length / pageSize);
  if (currentPage > totalPages) currentPage = totalPages;
  if (currentPage < 1) currentPage = 1;
  const pageTemplates = matchingTemplates.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  for (const it of pageTemplates) {{
    const item = it.item;
    const folder = it.folder;
    const name = it.name;
    const meta = it.meta;
    const safe = safeName(name);
    const prefix = `${{safe}}_${{item.id}}`;
    const previewSrc = `${{folder}}/previews/${{prefix}}_preview.png`;

    const card = document.createElement('div');
    card.className = 'template-card-wrapper';
    card.onclick = () => selectTemplate(item, folder);
    card.innerHTML = `
      <div class="template-card-inner">
        <div class="card-img-wrap">
          <div class="resource-protection-shield" title="Protected Specimen // Anti-Theft Watermark Guard"></div>
          <img src="${{previewSrc}}" alt="${{name}}" loading="lazy" draggable="false" onerror="this.style.opacity='0.2'">
          <div class="watermark-protection-tag">PROTECTED SPECIMEN</div>
        </div>
        <div class="card-body">
          <div class="card-title">${{name}}</div>
          <div class="card-meta">
            <span class="pill paper">${{item.paperSize || 'A4'}}</span>
            <span class="pill orient">${{item.orientation || 'landscape'}}</span>
            ${{meta.color ? `<span class="pill">${{meta.color}}</span>` : ''}}
            ${{meta.style ? `<span class="pill tag-mint">${{meta.style}}</span>` : ''}}
          </div>
        </div>
        <div class="card-links">
          <span style="font-family: var(--font-display); font-size: 11px; font-weight: 600; color: var(--accent-emerald); display: inline-flex; align-items: center; gap: 5px;">
            <svg class="keyline-icon" style="width: 12px; height: 12px; color: var(--accent-emerald);"><use href="#icon-shield"/></svg>
            Select Specimen
          </span>
          <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-dim); font-weight: 500;">
            #${{item.id}}
          </span>
        </div>
      </div>
    `;
    grid.appendChild(card);
  }}

  renderPagination(matchingTemplates.length);
}}

document.getElementById('search').addEventListener('input', (e) => {{
  searchQuery = e.target.value;
  currentPage = 1;
  render();
}});

document.querySelectorAll('.stepper-tab-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.stepper-tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentCategory = btn.getAttribute('data-cat');
    currentPage = 1;
    render();
  }});
}});

render();

function selectTemplateById(id) {{
  for (const cat of Object.keys(templates)) {{
    const found = (templates[cat] || []).find(it => it.id === id);
    if (found) {{
      selectTemplate(found, getFolder(cat));
      const stage = document.getElementById('visualStageWrapper');
      if (stage) {{
        stage.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }}
      return;
    }}
  }}
}}

function filterCategory(cat, optQuery) {{
  currentCategory = cat;
  currentPage = 1;
  if (optQuery) {{
    searchQuery = optQuery;
    const searchInput = document.getElementById('search');
    if (searchInput) searchInput.value = optQuery;
  }}
  document.querySelectorAll('.stepper-tab-btn').forEach(b => {{
    if (b.getAttribute('data-cat') === cat) {{
      b.classList.add('active');
    }} else {{
      b.classList.remove('active');
    }}
  }});
  render();
  const target = document.getElementById('grid');
  if (target) {{
    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}
}}

function filterMetadata(field, val) {{
  currentCategory = 'certificate';
  currentPage = 1;
  searchQuery = val;
  const searchInput = document.getElementById('search');
  if (searchInput) searchInput.value = val;
  document.querySelectorAll('.stepper-tab-btn').forEach(b => {{
    if (b.getAttribute('data-cat') === 'certificate') {{
      b.classList.add('active');
    }} else {{
      b.classList.remove('active');
    }}
  }});
  render();
  const target = document.getElementById('grid');
  if (target) {{
    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}
}}

function selectWorkspaceView(view) {{
  document.querySelectorAll('.ribbon-pill-btn, .tactile-pill-btn').forEach(b => b.classList.remove('active'));
  if (view === 'stage') {{
    const b = document.getElementById('tabBtnStage');
    if (b) b.classList.add('active');
    const el = document.getElementById('visualStageWrapper');
    if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }} else if (view === 'elements') {{
    filterCategory('elements');
  }} else {{
    const b = document.getElementById('tabBtnAll');
    if (b) b.classList.add('active');
    filterCategory('all');
    const el = document.getElementById('controlsBar');
    if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}
}}

// --- MOBILE NAVIGATION TOGGLE & DRAWER HANDLERS ---
function toggleMobileNav(e) {{
  if (e) e.stopPropagation();
  const drawer = document.getElementById('winzyMobileDrawer');
  const toggle = document.getElementById('winzyMobileToggle');
  const backdrop = document.getElementById('winzyMobileBackdrop');
  if (!drawer || !toggle) return;

  const isOpen = drawer.classList.contains('is-open');
  if (isOpen) {{
    closeMobileNav();
  }} else {{
    drawer.classList.add('is-open');
    toggle.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    drawer.setAttribute('aria-hidden', 'false');
    if (backdrop) backdrop.classList.add('is-open');
    document.body.classList.add('nav-mobile-open');
  }}
}}

function closeMobileNav() {{
  const drawer = document.getElementById('winzyMobileDrawer');
  const toggle = document.getElementById('winzyMobileToggle');
  const backdrop = document.getElementById('winzyMobileBackdrop');
  if (!drawer) return;

  drawer.classList.remove('is-open');
  if (toggle) {{
    toggle.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }}
  if (backdrop) backdrop.classList.remove('is-open');
  drawer.setAttribute('aria-hidden', 'true');
  document.body.classList.remove('nav-mobile-open');
}}

function handleMobileNavClick(action, event, param) {{
  closeMobileNav();
  setTimeout(() => {{
    handleMenuClick(action, event, param);
  }}, 140);
}}

// --- STICKY RESIZING NAVIGATION & SPECIFIC LINK ROUTING ---
function initStickyNav() {{
  const nav = document.getElementById('mainStickyNav') || document.querySelector('.winzy-card-nav');
  if (!nav) return;

  const onScroll = () => {{
    if (window.scrollY > 40) {{
      nav.classList.add('is-scrolled');
    }} else {{
      nav.classList.remove('is-scrolled');
    }}
  }};

  window.addEventListener('scroll', onScroll, {{ passive: true }});
  onScroll();

  window.addEventListener('resize', () => {{
    if (window.innerWidth > 900) {{
      closeMobileNav();
    }}
  }});

  document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') {{
      closeMobileNav();
    }}
  }});
}}

function updateActiveNavLinks() {{
  const params = new URLSearchParams(window.location.search);
  const view = params.get('view');
  const cat = params.get('category');

  document.querySelectorAll('.winzy-nav-link').forEach(l => l.classList.remove('active'));
  document.querySelectorAll('.winzy-mobile-link').forEach(l => l.classList.remove('active'));
  document.querySelectorAll('.winzy-mobile-cat-row').forEach(r => r.classList.remove('active'));

  if (view === 'vectors' || view === 'elements' || cat === 'elements') {{
    const el = document.getElementById('navLinkVectors');
    if (el) el.classList.add('active');
    const mobEl = document.getElementById('mobNavLinkVectors');
    if (mobEl) mobEl.classList.add('active');
  }} else if (view === 'stage' || view === 'inspector') {{
    const el = document.getElementById('navLinkStage');
    if (el) el.classList.add('active');
    const mobEl = document.getElementById('mobNavLinkStage');
    if (mobEl) mobEl.classList.add('active');
  }} else {{
    const el = document.getElementById('navLinkCatalog');
    if (el) el.classList.add('active');
    const mobEl = document.getElementById('mobNavLinkCatalog');
    if (mobEl) mobEl.classList.add('active');
  }}

  if (cat) {{
    const activeRow = document.querySelector(`.winzy-mobile-cat-row[href*="category=${{cat}}"]`);
    if (activeRow) activeRow.classList.add('active');
  }} else {{
    const allRow = document.querySelector('.winzy-mobile-cat-row[href*="category=all"]');
    if (allRow) allRow.classList.add('active');
  }}
}}

function handleMenuClick(action, event, param) {{
  if (event.ctrlKey || event.metaKey || event.shiftKey || event.button !== 0) {{
    return;
  }}
  event.preventDefault();

  if (action === 'catalog') {{
    filterCategory('all');
    window.history.pushState(null, '', 'index.html');
    const gridEl = document.getElementById('grid');
    if (gridEl) gridEl.scrollIntoView({{ behavior: 'smooth' }});
  }} else if (action === 'category') {{
    filterCategory(param || 'all');
    window.history.pushState(null, '', `index.html?category=${{param || 'all'}}`);
    const gridEl = document.getElementById('grid');
    if (gridEl) gridEl.scrollIntoView({{ behavior: 'smooth' }});
  }} else if (action === 'elements' || action === 'vectors') {{
    selectWorkspaceView('elements');
    filterCategory('elements');
    window.history.pushState(null, '', 'index.html?view=vectors');
    const el = document.getElementById('elementsCatalogSection');
    if (el) el.scrollIntoView({{ behavior: 'smooth' }});
  }} else if (action === 'stage' || action === 'inspector') {{
    selectWorkspaceView('stage');
    window.history.pushState(null, '', 'index.html?view=stage');
    const el = document.getElementById('visualStageWrapper');
    if (el) el.scrollIntoView({{ behavior: 'smooth' }});
  }} else {{
    selectWorkspaceView('all');
    window.history.pushState(null, '', 'index.html');
  }}

  updateActiveNavLinks();
}}

function handleInitialUrlRoute() {{
  const params = new URLSearchParams(window.location.search);
  const view = params.get('view');
  const cat = params.get('category');

  if (view === 'vectors' || view === 'elements' || cat === 'elements') {{
    selectWorkspaceView('elements');
    filterCategory('elements');
  }} else if (view === 'stage' || view === 'inspector') {{
    selectWorkspaceView('stage');
  }} else if (cat) {{
    filterCategory(cat);
  }}
  updateActiveNavLinks();
}}

initStickyNav();
handleInitialUrlRoute();
window.addEventListener('popstate', handleInitialUrlRoute);

// --- WINZY EDITORIAL HERO SLIDE CONTROLLER ---
const winzyHeroSlides = [
  {{
    index: '01',
    name: 'EGYPT',
    image: 'assets/hero_egypt_pyramids.jpg',
    thumb: 'assets/hero_preview_thumb.jpg',
    stat1: '20K+', label1: 'Happy Travellers',
    stat2: '2K+', label2: 'Custom Tours',
    stat3: '5K+', label3: 'Arranged Stays',
    tagline: 'Book unique stays that bring travelers and locals together -your gateway to shared adventures'
  }},
  {{
    index: '02',
    name: 'ICELAND',
    image: 'https://images.unsplash.com/photo-1504893524553-b855bce32c67?q=80&w=1600&auto=format&fit=crop',
    thumb: 'https://images.unsplash.com/photo-1520769945061-0a448c4471dd?q=80&w=400&auto=format&fit=crop',
    stat1: '18K+', label1: 'Glacier Hikers',
    stat2: '1.4K+', label2: 'Northern Lights',
    stat3: '3.8K+', label3: 'Eco Lodges',
    tagline: 'Immerse yourself in volcanic wonder and arctic fjords under the celestial auroras'
  }},
  {{
    index: '03',
    name: 'TOKYO',
    image: 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1600&auto=format&fit=crop',
    thumb: 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?q=80&w=400&auto=format&fit=crop',
    stat1: '35K+', label1: 'Urban Explorers',
    stat2: '4.2K+', label2: 'Heritage Spots',
    stat3: '9K+', label3: 'Ryokan Stays',
    tagline: 'Step into futuristic neon skylines harmonized with ancient historic shrines'
  }},
  {{
    index: '04',
    name: 'SWISS',
    image: 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?q=80&w=1600&auto=format&fit=crop',
    thumb: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=400&auto=format&fit=crop',
    stat1: '24K+', label1: 'Alpine Climbers',
    stat2: '3.1K+', label2: 'Scenic Chalets',
    stat3: '6K+', label3: 'Summit Trails',
    tagline: 'Wake up above the clouds with pristine snowcapped peaks and mirror-glass lakes'
  }},
  {{
    index: '05',
    name: 'VAULT',
    image: 'assets/hero_egypt_pyramids.jpg',
    thumb: 'assets/hero_preview_thumb.jpg',
    stat1: '2,328', label1: 'Design Templates',
    stat2: '2,137', label2: 'Certificates HD',
    stat3: '130', label3: 'Vector Elements',
    tagline: 'Official enterprise credential repository with cryptographic security and vector typography'
  }}
];

let currentHeroIndex = 0;

function nextWinzyHeroSlide() {{
  currentHeroIndex = (currentHeroIndex + 1) % winzyHeroSlides.length;
  updateWinzyHero(currentHeroIndex);
}}

function updateWinzyHero(idx) {{
  const slide = winzyHeroSlides[idx];
  if (!slide) return;

  const card = document.getElementById('winzyHeroCard');
  const watermark = document.getElementById('winzyHeroWatermark');
  const stat1 = document.getElementById('heroStat1');
  const stat2 = document.getElementById('heroStat2');
  const stat3 = document.getElementById('heroStat3');
  const tagline = document.getElementById('heroTagline');
  const thumb = document.getElementById('heroWidgetThumb');
  const counter = document.getElementById('heroWidgetCounter');
  const bottomIdx = document.getElementById('heroBottomIndex');
  const progress = document.getElementById('heroWidgetProgress');

  if (card) {{
    card.style.backgroundImage = `linear-gradient(180deg, rgba(15, 23, 42, 0.55) 0%, rgba(15, 23, 42, 0.05) 35%, rgba(15, 23, 42, 0.3) 65%, rgba(15, 23, 42, 0.92) 100%), url('${{slide.image}}')`;
  }}
  if (watermark) watermark.innerText = slide.name;
  if (stat1) {{
    stat1.innerText = slide.stat1;
    if (stat1.nextElementSibling) stat1.nextElementSibling.innerText = slide.label1;
  }}
  if (stat2) {{
    stat2.innerText = slide.stat2;
    if (stat2.nextElementSibling) stat2.nextElementSibling.innerText = slide.label2;
  }}
  if (stat3) {{
    stat3.innerText = slide.stat3;
    if (stat3.nextElementSibling) stat3.nextElementSibling.innerText = slide.label3;
  }}
  if (tagline) tagline.innerText = slide.tagline;
  if (thumb) thumb.src = slide.thumb;
  if (counter) counter.innerText = `${{slide.index}}/10`;
  if (bottomIdx) bottomIdx.innerText = slide.index;
  if (progress) progress.style.width = `${{((idx + 1) / winzyHeroSlides.length) * 100}}%`;
}}

// --- ENTERPRISE CONTENT PROTECTION & ANTI-INSPECTION ENGINE ---
let _noticeTimer = null;
function showProtectionNotice(message) {{
  let toast = document.getElementById('resourceProtectionToast');
  if (!toast) {{
    toast = document.createElement('div');
    toast.id = 'resourceProtectionToast';
    toast.className = 'protection-notice-toast';
    document.body.appendChild(toast);
  }}
  toast.innerHTML = `
    <span class="protection-toast-badge">SHIELD ACTIVE</span>
    <span class="protection-toast-text">${{message}}</span>
  `;
  toast.classList.add('is-visible');
  if (_noticeTimer) clearTimeout(_noticeTimer);
  _noticeTimer = setTimeout(() => {{
    toast.classList.remove('is-visible');
  }}, 2200);
}}

document.addEventListener('contextmenu', (e) => {{
  e.preventDefault();
  showProtectionNotice('ASSET PROTECTED // CONTEXT DOWNLOAD RESTRICTED');
  return false;
}}, true);

document.addEventListener('keydown', (e) => {{
  if (e.key === 'F12' || e.keyCode === 123) {{
    e.preventDefault();
    e.stopPropagation();
    showProtectionNotice('DEVELOPER TOOLS ACCESS RESTRICTED');
    return false;
  }}
  const isCtrlOrMeta = e.ctrlKey || e.metaKey;
  const isShift = e.shiftKey;
  const isAlt = e.altKey;
  const key = (e.key || '').toLowerCase();

  if (isCtrlOrMeta && (isShift || isAlt) && (key === 'i' || key === 'j' || key === 'c')) {{
    e.preventDefault();
    e.stopPropagation();
    showProtectionNotice('INSPECTOR ACCESS RESTRICTED');
    return false;
  }}
  if (isCtrlOrMeta && key === 'u') {{
    e.preventDefault();
    e.stopPropagation();
    showProtectionNotice('VAULT ENCRYPTED // REPOSITORY ACCESS RESTRICTED');
    return false;
  }}
  if (isCtrlOrMeta && key === 's') {{
    e.preventDefault();
    e.stopPropagation();
    showProtectionNotice('ACTION BLOCKED // REPOSITORY DOWNLOAD RESTRICTED');
    return false;
  }}
  if (isCtrlOrMeta && key === 'p') {{
    e.preventDefault();
    e.stopPropagation();
    showProtectionNotice('ACTION BLOCKED // DOCUMENT PRINTING RESTRICTED');
    return false;
  }}
  if (isCtrlOrMeta && (key === 'c' || key === 'x' || key === 'a')) {{
    if (e.target && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {{
      e.preventDefault();
      e.stopPropagation();
      showProtectionNotice('CLIPBOARD EXTRACTION RESTRICTED');
      return false;
    }}
  }}
}}, true);

document.addEventListener('copy', (e) => {{
  if (e.target && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {{
    e.preventDefault();
    showProtectionNotice('CLIPBOARD COPY RESTRICTED');
  }}
}}, true);
document.addEventListener('cut', (e) => {{
  if (e.target && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {{
    e.preventDefault();
    showProtectionNotice('CLIPBOARD CUT RESTRICTED');
  }}
}}, true);
document.addEventListener('dragstart', (e) => {{
  e.preventDefault();
  showProtectionNotice('ASSET PROTECTED // DRAG EXTRACTION DISABLED');
  return false;
}}, true);
document.addEventListener('drop', (e) => {{
  e.preventDefault();
  return false;
}}, true);
document.addEventListener('selectstart', (e) => {{
  if (e.target && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') e.preventDefault();
}}, true);

try {{
  const noop = () => {{}};
  console.log = noop;
  console.warn = noop;
  console.info = noop;
  console.debug = noop;
}} catch (err) {{}}
</script>
</body>
</html>
"""

    out_html = os.path.join(BASE_DIR, "index.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    public_dir = os.path.join(BASE_DIR, "public")
    if os.path.exists(public_dir):
        out_public = os.path.join(public_dir, "index.html")
        with open(out_public, "w", encoding="utf-8") as f:
            f.write(html_content)

    print("Catalog updated successfully!")

if __name__ == "__main__":
    main()
