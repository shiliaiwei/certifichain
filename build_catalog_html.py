import json
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_guilloche_svg(w=1200, h=160):
    """Generate authentic mathematical banknote guilloche wave patterns & rosettes."""
    lines = []
    # 1. Interlocking sinusoidal wave bands (12 harmonic layers)
    for i in range(12):
        pts = []
        for x in range(0, w + 12, 12):
            y = 75 + 26 * math.sin(x * 0.018 + i * 0.35) + 14 * math.cos(x * 0.042 - i * 0.28)
            pts.append(f"{x},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="rgba(255,255,255,0.38)" stroke-width="0.65"/>')

    # 2. Counter-harmonic security wave bands (8 inverse layers)
    for i in range(8):
        pts = []
        for x in range(0, w + 15, 15):
            y = 75 - 20 * math.sin(x * 0.024 - i * 0.45) + 10 * math.sin(x * 0.065 + i * 0.3)
            pts.append(f"{x},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="rgba(255,255,255,0.28)" stroke-width="0.55"/>')

    # 3. Left Guilloche Rosette
    for i in range(7):
        R, r, p = 52 + i * 4, 18, 28
        pts = []
        for step in range(181):
            t = math.radians(step * 4)
            x = (R - r) * math.cos(t) + p * math.cos((R - r) * t / r) + 160
            y = (R - r) * math.sin(t) - p * math.sin((R - r) * t / r) + 80
            pts.append(f"{x:.1f},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="rgba(255,255,255,0.32)" stroke-width="0.6"/>')

    # 4. Right Guilloche Rosette
    for i in range(7):
        R, r, p = 52 + i * 4, 18, 28
        pts = []
        for step in range(181):
            t = math.radians(step * 4)
            x = (R - r) * math.cos(t) + p * math.cos((R - r) * t / r) + (w - 160)
            y = (R - r) * math.sin(t) - p * math.sin((R - r) * t / r) + 80
            pts.append(f"{x:.1f},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="rgba(255,255,255,0.32)" stroke-width="0.6"/>')

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

    # Email templates
    email_path = os.path.join(BASE_DIR, "email_templates", "email_templates.json")
    emails_data = []
    if os.path.exists(email_path):
        try:
            with open(email_path, "r", encoding="utf-8") as f:
                emails_data = json.load(f)
        except Exception:
            pass

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

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Certifier Studio // Cyber-Grid & Banknote Guilloche Catalog</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,400&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  /* .TECH DOMAINS & 3D Skeuomorphic Leather Tokens */
  :root {{
    /* Surfaces */
    --bg-canvas: #08090b;
    --bg-panel: #0d0e11;
    --bg-panel-secondary: #121316;
    --bg-input: rgb(15, 16, 18);

    /* Borders */
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-muted: rgb(112, 112, 112);
    --border-divider: rgba(255, 255, 255, 0.06);

    /* Typography */
    --text-white: #ffffff;
    --text-primary: #f4f4f5;
    --text-muted: #8c9099;
    --text-dim: #555963;

    /* Accents */
    --accent-mint: #d2e2b9;
    --accent-mint-hover: #e0eed0;
    --accent-orange: #f25a38;
    --accent-success: #10b981;

    /* Fonts */
    --font-main: "DM Sans", -apple-system, BlinkMacSystemFont, sans-serif;
    --font-display: "Space Grotesk", "DM Sans", sans-serif;

    /* 3D Skeuomorphic Leather */
    --leather-highlight: #6b22a8;
    --leather-body: #4c1482;
    --leather-shadow: #380c63;
    --leather-deep: #260742;
    --leather-thread: #e9d5ff;
    --satin-usd: #059669;
    --satin-khr: #a855f7;
    --satin-wei: #0098ea;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background-color: var(--bg-canvas);
    background-image: 
      linear-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
    background-size: 38px 38px;
    background-position: center top;
    color: var(--text-primary);
    font-family: var(--font-main);
    min-height: 100vh;
    padding: 24px;
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

  /* 3D SKEUOMORPHIC PURPLE LEATHER SLEEVE (TOP BAR / NAV) */
  .leather-sleeve {{
    position: relative;
    background: linear-gradient(180deg, var(--leather-highlight) 0%, var(--leather-body) 45%, var(--leather-deep) 100%);
    border-radius: 38px;
    box-shadow: 
      0 24px 48px -12px rgba(45, 10, 80, 0.55),
      0 12px 24px -6px rgba(30, 5, 55, 0.40),
      inset 0 2px 4px rgba(255, 255, 255, 0.35),
      inset 0 -3px 8px rgba(0, 0, 0, 0.55);
    padding: 16px 20px 22px 20px;
    overflow: hidden;
    margin-bottom: 28px;
  }}

  .leather-pebble-grain {{
    position: absolute;
    inset: 0;
    border-radius: 38px;
    background-image: 
      radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.38) 1px, transparent 1px),
      radial-gradient(circle at 0% 0%, rgba(0, 0, 0, 0.5) 1px, transparent 1px);
    background-size: 6px 6px, 8px 8px;
    mix-blend-mode: overlay;
    opacity: 0.22;
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
    stroke: var(--leather-thread);
    stroke-width: 1.25;
    stroke-dasharray: 4 4;
    stroke-linecap: round;
    opacity: 0.55;
    filter: drop-shadow(0px 1px 1px rgba(0, 0, 0, 0.65));
  }}

  /* Inserted Physical Card (Tier 2) */
  .inserted-card-slot {{
    position: relative;
    width: 97%;
    margin: 0 auto;
    border-radius: 24px 24px 18px 18px;
    background: linear-gradient(135deg, #0284c7 0%, #0098ea 35%, #0369a1 70%, #0c4a6e 100%);
    box-shadow: 
      0 -4px 16px rgba(0, 0, 0, 0.35),
      inset 0 1.5px 2px rgba(255, 255, 255, 0.65),
      inset 0 -2px 4px rgba(0, 0, 0, 0.25);
    padding: 18px 24px 44px 24px;
    overflow: hidden;
    transition: background 0.35s ease;
    z-index: 3;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
  }}

  .inserted-card-slot.mode-usd {{
    background: linear-gradient(135deg, #059669 0%, #047857 35%, #065f46 70%, #064e3b 100%);
  }}

  .inserted-card-slot.mode-khr {{
    background: linear-gradient(135deg, #c084fc 0%, #a855f7 35%, #7e22ce 70%, #4c1d95 100%);
  }}

  .card-specular-sheen {{
    position: absolute;
    inset: 0;
    background: linear-gradient(108deg, rgba(255, 255, 255, 0.28) 0%, transparent 42%, rgba(255, 255, 255, 0.10) 100%);
    pointer-events: none;
    z-index: 2;
  }}

  .guilloche-watermark {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    mix-blend-mode: overlay;
    opacity: 0.30;
    filter: contrast(1.35) brightness(1.1);
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
    gap: 16px;
    flex-wrap: wrap;
  }}

  .crypto-address-pill {{
    font-family: var(--font-display);
    font-size: 11px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.85);
    background: rgba(0, 0, 0, 0.4);
    padding: 5px 12px;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    letter-spacing: 0.05em;
  }}

  .card-metric-badge {{
    font-family: var(--font-display);
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  /* Front Overlapping Flap (Tier 3) */
  .front-leather-flap {{
    position: relative;
    margin-top: -30px;
    background: linear-gradient(180deg, var(--leather-body) 0%, var(--leather-deep) 100%);
    border-radius: 20px 20px 30px 30px;
    box-shadow: 
      0 -8px 20px -4px rgba(25, 4, 45, 0.65),
      inset 0 2px 2px rgba(255, 255, 255, 0.38),
      inset 0 -3px 6px rgba(0, 0, 0, 0.50);
    padding: 14px 24px;
    z-index: 4;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }}

  .scooped-rim-highlight {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1.5px;
    background: linear-gradient(90deg, transparent 5%, rgba(255, 255, 255, 0.45) 50%, transparent 95%);
    z-index: 6;
  }}

  .scooped-lip-svg {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 12px;
    overflow: visible;
    pointer-events: none;
    z-index: 7;
  }}

  .scooped-lip-path {{
    fill: none;
    stroke: var(--leather-thread);
    stroke-width: 1.25;
    stroke-dasharray: 4 4;
    stroke-linecap: round;
    opacity: 0.55;
    filter: drop-shadow(0px 1px 1px rgba(0, 0, 0, 0.65));
  }}

  .leather-toggle-group {{
    display: flex;
    align-items: center;
    gap: 4px;
    background: rgba(0, 0, 0, 0.45);
    padding: 4px;
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.6);
  }}

  .leather-toggle-btn {{
    background: transparent;
    border: none;
    color: #cbd5e1;
    font-family: var(--font-display);
    font-size: 11px;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: all 0.2s;
  }}

  .leather-toggle-btn.active {{
    background: linear-gradient(180deg, #ffffff 0%, #e2e8f0 100%);
    color: #0f172a;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35), inset 0 1px 1px #ffffff;
  }}

  .leather-toggle-btn.mode-usd.active {{
    background: linear-gradient(180deg, #10b981 0%, #059669 100%);
    color: #ffffff;
  }}

  .leather-toggle-btn.mode-khr.active {{
    background: linear-gradient(180deg, #c084fc 0%, #9333ea 100%);
    color: #ffffff;
  }}

  .vault-status-indicator {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-display);
    font-size: 12px;
    color: var(--leather-thread);
  }}

  .status-pulse {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 8px #10b981;
  }}

  /* .TECH DOMAINS NESTED INSET CHAMFER ARCHITECTURE */

  /* 18px Chamfer (Hero / Presets Section) */
  .chamfer-18-wrapper {{
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 18px) 0, 100% 18px, 100% 100%, 0 100%);
    padding: 1px;
    margin-bottom: 24px;
    transition: background-color 0.2s ease;
  }}

  .chamfer-18-wrapper:hover {{
    background-color: var(--accent-mint);
  }}

  .chamfer-18-inner {{
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 17.586px) 0, 100% 17.586px, 100% 100%, 0 100%);
    padding: 22px;
    width: 100%;
  }}

  .section-header-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border-divider);
    padding-bottom: 12px;
  }}

  .section-title {{
    font-family: var(--font-display);
    font-size: 15px;
    font-weight: 700;
    color: var(--accent-mint);
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
  }}

  .section-desc {{
    font-size: 12px;
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
    transition: all 0.2s;
  }}

  .blank-card-wrapper:hover {{
    background-color: var(--accent-mint);
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
  }}

  .blank-card-dim {{
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.4;
  }}

  .blank-card-link {{
    font-family: var(--font-display);
    font-size: 11px;
    font-weight: 600;
    color: var(--accent-mint);
    text-decoration: none;
    margin-top: auto;
    padding-top: 6px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }}

  .blank-card-link:hover {{
    text-decoration: underline;
  }}

  /* CONTROLS: SPLIT INPUT SEARCH & STEPPER CATEGORY TABS */
  .controls-bar {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 24px;
  }}

  .cyber-search-group {{
    display: flex;
    align-items: stretch;
    background-color: var(--border-muted);
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
    padding: 1px;
    transition: background-color 0.2s ease;
  }}

  .cyber-search-group:focus-within {{
    background-color: var(--accent-mint);
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
    font-size: 14px;
    padding: 12px 14px;
  }}

  .cyber-search-divider {{
    width: 1px;
    height: 24px;
    background-color: var(--border-muted);
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
    transition: all 0.2s;
  }}

  .cyber-search-btn:hover {{
    color: var(--accent-mint);
    background-color: rgba(210, 226, 185, 0.08);
  }}

  /* Stepper Category Tabs */
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
    transition: all 0.2s;
  }}

  .stepper-tab-btn .tab-content {{
    background-color: var(--bg-panel-secondary);
    clip-path: polygon(0 0, calc(100% - 11.586px) 0, 100% 11.586px, 100% 100%, 0 100%);
    padding: 8px 14px;
    display: flex;
    align-items: center;
    gap: 7px;
    color: var(--text-muted);
    font-family: var(--font-display);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.02em;
  }}

  .stepper-tab-btn:hover {{
    background-color: var(--accent-mint);
  }}

  .stepper-tab-btn:hover .tab-content {{
    color: var(--text-white);
  }}

  .stepper-tab-btn.active {{
    background-color: var(--accent-mint);
  }}

  .stepper-tab-btn.active .tab-content {{
    background-color: var(--accent-mint);
    color: #08090b;
    font-weight: 700;
  }}

  /* TEMPLATE CARDS GRID */
  .cyber-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(285px, 1fr));
    gap: 20px;
  }}

  .chamfer-14-wrapper,
  .template-card-wrapper {{
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
    padding: 1px;
    transition: all 0.25s ease;
  }}

  .chamfer-14-wrapper:hover,
  .template-card-wrapper:hover {{
    background-color: var(--accent-mint);
    transform: translateY(-3px);
  }}

  .chamfer-14-inner,
  .template-card-inner {{
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 13.586px) 0, 100% 13.586px, 100% 100%, 0 100%);
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }}

  .card-img-wrap {{
    background: #020617;
    position: relative;
    padding-top: 70%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 1px solid var(--border-divider);
  }}

  .card-img-wrap img {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 8px;
  }}

  .card-body {{
    padding: 16px;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .card-title {{
    font-family: var(--font-display);
    font-size: 14px;
    font-weight: 700;
    color: var(--text-white);
    line-height: 1.35;
    word-break: break-word;
  }}

  .card-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: auto;
  }}

  .pill {{
    font-family: var(--font-display);
    font-size: 10px;
    font-weight: 600;
    padding: 3px 8px;
    background: var(--bg-panel-secondary);
    border: 1px solid var(--border-subtle);
    color: var(--text-muted);
    letter-spacing: 0.04em;
    clip-path: polygon(0 0, calc(100% - 6px) 0, 100% 6px, 100% 100%, 0 100%);
  }}

  .pill.paper {{
    background: rgba(30, 58, 138, 0.45);
    border-color: rgba(59, 130, 246, 0.4);
    color: #93c5fd;
  }}

  .pill.orient {{
    background: rgba(6, 78, 59, 0.45);
    border-color: rgba(16, 185, 129, 0.4);
    color: #6ee7b7;
  }}

  .pill.tag-mint {{
    background: rgba(210, 226, 185, 0.15);
    border-color: var(--accent-mint);
    color: var(--accent-mint);
  }}

  .card-links {{
    display: flex;
    justify-content: space-between;
    padding: 11px 16px;
    background: rgba(0, 0, 0, 0.35);
    border-top: 1px solid var(--border-divider);
  }}

  .card-links a {{
    font-family: var(--font-display);
    font-size: 11px;
    font-weight: 600;
    color: var(--accent-mint);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    transition: color 0.15s;
  }}

  .card-links a:hover {{
    color: var(--accent-mint-hover);
    text-decoration: underline;
  }}

  /* ELEMENT CARD */
  .element-card-wrapper {{
    background-color: var(--border-subtle);
    clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 0 100%);
    padding: 1px;
    transition: all 0.2s;
  }}

  .element-card-wrapper:hover {{
    background-color: var(--accent-mint);
    transform: translateY(-2px);
  }}

  .element-card-inner {{
    background-color: var(--bg-panel);
    clip-path: polygon(0 0, calc(100% - 11.586px) 0, 100% 11.586px, 100% 100%, 0 100%);
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    text-align: center;
  }}

  .element-preview {{
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .element-preview img {{
    max-width: 100%;
    max-height: 100%;
    filter: invert(1);
  }}

  .element-name {{
    font-family: var(--font-display);
    font-size: 11px;
    color: var(--text-muted);
    word-break: break-all;
  }}

  /* SPECIFICATION TABLES */
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
    font-size: 13px;
  }}

  .spec-table th, .spec-table td {{
    padding: 10px 14px;
    border: 1px solid var(--border-divider);
    text-align: left;
  }}

  .spec-table th {{
    background: var(--bg-panel-secondary);
    color: var(--accent-mint);
    font-family: var(--font-display);
    font-weight: 700;
  }}
</style>
</head>
<body class="cyber-canvas">

<!-- KEYLINE ICONS SYSTEM DEFINITION -->
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
</svg>

<!-- 3D SKEUOMORPHIC PURPLE TEXTURED LEATHER & BANKNOTE GUILLOCHE TOP BAR -->
<header class="leather-sleeve">
  <!-- Micro-Radial Pebble Grain Overlay -->
  <div class="leather-pebble-grain"></div>

  <!-- Perimeter Simulated Thread Stitching -->
  <svg class="leather-stitch-svg" xmlns="http://www.w3.org/2000/svg">
    <rect class="leather-stitch-rect" x="9" y="9" width="calc(100% - 18px)" height="calc(100% - 18px)" rx="30" ry="30"/>
  </svg>

  <!-- Tier 2: Inserted Physical Satin Card -->
  <div class="inserted-card-slot" id="satinCard">
    <!-- Specular Sheen Overlay -->
    <div class="card-specular-sheen"></div>

    <!-- Mathematical Banknote Guilloche Security Watermark -->
    {guilloche_svg}

    <!-- Left Brand Unit: Official Typographic Badge -->
    <div class="card-brand-col">
      <div style="display: flex; align-items: center; gap: 8px;">
        <!-- Single-line Corporate Typographic Badge -->
        <svg width="122" height="30" viewBox="0 0 122 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <text x="0" y="24" fill="#ffffff" font-size="24" font-family="'Space Grotesk', system-ui, sans-serif" font-weight="900" letter-spacing="-0.03em" textLength="72" lengthAdjust="spacingAndGlyphs">SHILIAI</text>
          <rect x="75" y="4" width="44" height="23" rx="6" fill="#ffffff" />
          <text id="badgeWeiText" x="97" y="21" text-anchor="middle" fill="#0077b5" font-size="14" font-family="'Space Grotesk', system-ui, sans-serif" font-weight="900" letter-spacing="-0.01em">WEI</text>
        </svg>
        <span class="crypto-address-pill">
          <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-shield"/></svg>
          0x71C84...F29A // CERT-VAULT
        </span>
      </div>
      <div style="font-family: var(--font-display); font-size: 13px; color: rgba(255,255,255,0.9); font-weight: 600; margin-top: 2px;">
        Certifier Local HD Design Studio & Template Archive
      </div>
    </div>

    <!-- Right Metric Unit -->
    <div class="card-meta-col">
      <div class="card-metric-badge">
        <svg class="keyline-icon" style="width: 18px; height: 18px;"><use href="#icon-certificate"/></svg>
        <span>{total_templates} TEMPLATES</span>
      </div>
      <div class="card-metric-badge" style="font-size: 12px; opacity: 0.85;">
        <svg class="keyline-icon" style="width: 16px; height: 16px;"><use href="#icon-shapes"/></svg>
        <span>{total_svgs} VECTOR SVGS</span>
      </div>
    </div>
  </div>

  <!-- Tier 3: Front Overlapping Leather Flap with Scooped Lip -->
  <div class="front-leather-flap">
    <!-- Top Specular Rim Highlight -->
    <div class="scooped-rim-highlight"></div>

    <!-- Scooped Curved Edge Thread Stitching -->
    <svg class="scooped-lip-svg" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" viewBox="0 0 360 14">
      <path class="scooped-lip-path" d="M 2 2 Q 180 8 360 2"/>
    </svg>

    <!-- Physical Tactile Currency / Card Finish Toggles -->
    <div class="leather-toggle-group">
      <button class="leather-toggle-btn active" id="btnWei" onclick="setCardFinish('wei')">
        <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-shield"/></svg>
        WEI BLUE
      </button>
      <button class="leather-toggle-btn mode-usd" id="btnUsd" onclick="setCardFinish('usd')">
        <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-certificate"/></svg>
        USD EMERALD
      </button>
      <button class="leather-toggle-btn mode-khr" id="btnKhr" onclick="setCardFinish('khr')">
        <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-badge"/></svg>
        KHR VIOLET
      </button>
    </div>

    <!-- Vault Live Verification Indicator -->
    <div class="vault-status-indicator">
      <div class="status-pulse"></div>
      <span style="font-weight: 700; letter-spacing: 0.04em;">CENTRAL REPOSITORY VERIFIED // OFFLINE READY</span>
    </div>
  </div>
</header>

<!-- START WITH BLANK CANVAS PRESETS (18PX CHAMFERED HERO CONTAINER) -->
<section class="chamfer-18-wrapper">
  <div class="chamfer-18-inner">
    <div class="section-header-row">
      <div class="section-title">
        <svg class="keyline-icon" style="color: var(--accent-mint); width: 18px; height: 18px;"><use href="#icon-dimensions"/></svg>
        Blank Canvas Presets (6 Standard Document Types & Geometries)
      </div>
      <div class="section-desc">Production Dimensions @ 96 DPI & 300 DPI Print HD</div>
    </div>
    <div class="blank-grid">
      <div class="blank-card-wrapper">
        <div class="blank-card-inner">
          <div class="blank-card-name">Certificate (A4 Landscape)</div>
          <div class="blank-card-dim">297 x 210 mm | 1123 x 794 px @ 96DPI<br>2000 x 1414 HD | Ratio 1.414</div>
          <a class="blank-card-link" href="editor_specifications/blank_canvas_presets.json" target="_blank">
            <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-code"/></svg>
            View JSON Model
          </a>
        </div>
      </div>
      <div class="blank-card-wrapper">
        <div class="blank-card-inner">
          <div class="blank-card-name">Certificate (A4 Portrait)</div>
          <div class="blank-card-dim">210 x 297 mm | 794 x 1123 px @ 96DPI<br>1414 x 2000 HD | Ratio 0.707</div>
          <a class="blank-card-link" href="editor_specifications/blank_canvas_presets.json" target="_blank">
            <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-code"/></svg>
            View JSON Model
          </a>
        </div>
      </div>
      <div class="blank-card-wrapper">
        <div class="blank-card-inner">
          <div class="blank-card-name">Certificate (US Letter Landscape)</div>
          <div class="blank-card-dim">11" x 8.5" | 1056 x 816 px @ 96DPI<br>3300 x 2550 px @ 300DPI</div>
          <a class="blank-card-link" href="editor_specifications/blank_canvas_presets.json" target="_blank">
            <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-code"/></svg>
            View JSON Model
          </a>
        </div>
      </div>
      <div class="blank-card-wrapper">
        <div class="blank-card-inner">
          <div class="blank-card-name">Badge (Square 1:1)</div>
          <div class="blank-card-dim">512 x 512 px Viewport<br>1000 x 1000 px Vector Canvas</div>
          <a class="blank-card-link" href="editor_specifications/blank_canvas_presets.json" target="_blank">
            <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-code"/></svg>
            View JSON Model
          </a>
        </div>
      </div>
      <div class="blank-card-wrapper">
        <div class="blank-card-inner">
          <div class="blank-card-name">Transcript (A4 Landscape)</div>
          <div class="blank-card-dim">297 x 210 mm | 1123 x 794 px @ 96DPI<br>3508 x 2480 px @ 300DPI</div>
          <a class="blank-card-link" href="editor_specifications/blank_canvas_presets.json" target="_blank">
            <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-code"/></svg>
            View JSON Model
          </a>
        </div>
      </div>
      <div class="blank-card-wrapper">
        <div class="blank-card-inner">
          <div class="blank-card-name">Training Record (A4 Landscape)</div>
          <div class="blank-card-dim">297 x 210 mm | 1123 x 794 px @ 96DPI<br>Professional CPD Form</div>
          <a class="blank-card-link" href="editor_specifications/blank_canvas_presets.json" target="_blank">
            <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-code"/></svg>
            View JSON Model
          </a>
        </div>
      </div>
      <div class="blank-card-wrapper">
        <div class="blank-card-inner">
          <div class="blank-card-name">Assessment (A4 Landscape)</div>
          <div class="blank-card-dim">297 x 210 mm | 1123 x 794 px @ 96DPI<br>Evaluation & Exam Model</div>
          <a class="blank-card-link" href="editor_specifications/blank_canvas_presets.json" target="_blank">
            <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-code"/></svg>
            View JSON Model
          </a>
        </div>
      </div>
      <div class="blank-card-wrapper">
        <div class="blank-card-inner">
          <div class="blank-card-name">Letter (A4 Portrait)</div>
          <div class="blank-card-dim">210 x 297 mm | 794 x 1123 px @ 96DPI<br>Formal Verification Credential</div>
          <a class="blank-card-link" href="editor_specifications/blank_canvas_presets.json" target="_blank">
            <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-code"/></svg>
            View JSON Model
          </a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- CONTROLS: SPLIT INPUT SEARCH & STEPPER CATEGORY TABS -->
<div class="controls-bar">
  <!-- Split Input Search Container (14px Chamfer Cut) -->
  <div class="cyber-search-group">
    <div class="cyber-search-inner">
      <svg class="keyline-icon" style="color: var(--accent-mint); width: 18px; height: 18px;"><use href="#icon-search"/></svg>
      <input type="text" id="search" class="cyber-search-input" placeholder="Search templates by title, orientation, color, style, or metadata...">
      <div class="cyber-search-divider"></div>
      <button class="cyber-search-btn" onclick="document.getElementById('search').focus()">
        <svg class="keyline-icon"><use href="#icon-search"/></svg>
        SEARCH
      </button>
    </div>
  </div>

  <!-- Stepper Category Tabs (12px Chamfer Cuts) -->
  <div class="stepper-tabs">
    <button class="stepper-tab-btn active" data-cat="all">
      <div class="tab-content">
        <svg class="keyline-icon"><use href="#icon-certificate"/></svg>
        All ({total_templates})
      </div>
    </button>
    <button class="stepper-tab-btn" data-cat="certificate">
      <div class="tab-content">
        <svg class="keyline-icon"><use href="#icon-certificate"/></svg>
        Certificates ({len(master.get('certificate', []))})
      </div>
    </button>
    <button class="stepper-tab-btn" data-cat="badge">
      <div class="tab-content">
        <svg class="keyline-icon"><use href="#icon-badge"/></svg>
        Badges ({len(master.get('badge', []))})
      </div>
    </button>
    <button class="stepper-tab-btn" data-cat="transcript">
      <div class="tab-content">
        <svg class="keyline-icon"><use href="#icon-transcript"/></svg>
        Transcripts ({len(master.get('transcript', []))})
      </div>
    </button>
    <button class="stepper-tab-btn" data-cat="training_record">
      <div class="tab-content">
        <svg class="keyline-icon"><use href="#icon-training"/></svg>
        Training Records ({len(master.get('training_record', []))})
      </div>
    </button>
    <button class="stepper-tab-btn" data-cat="assessment">
      <div class="tab-content">
        <svg class="keyline-icon"><use href="#icon-assessment"/></svg>
        Assessments ({len(master.get('assessment', []))})
      </div>
    </button>
    <button class="stepper-tab-btn" data-cat="letter">
      <div class="tab-content">
        <svg class="keyline-icon"><use href="#icon-letter"/></svg>
        Letters ({len(master.get('letter', []))})
      </div>
    </button>
    <button class="stepper-tab-btn" data-cat="elements">
      <div class="tab-content">
        <svg class="keyline-icon"><use href="#icon-shapes"/></svg>
        Vector Elements ({total_svgs})
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
    <button class="stepper-tab-btn" data-cat="email">
      <div class="tab-content">
        <svg class="keyline-icon"><use href="#icon-email"/></svg>
        Email Templates ({len(emails_data)})
      </div>
    </button>
  </div>
</div>

<!-- MAIN GRID CONTAINER -->
<div class="cyber-grid" id="grid"></div>

<script>
const templates = {json.dumps(master)};
const elements = {json.dumps(elements_data)};
const emails = {json.dumps(emails_data)};
const attributes = {json.dumps(attributes_data)};
const typography = {json.dumps(typography_data)};

let currentCategory = "all";
let searchQuery = "";

function setCardFinish(mode) {{
  const card = document.getElementById('satinCard');
  const weiText = document.getElementById('badgeWeiText');
  document.querySelectorAll('.leather-toggle-btn').forEach(b => b.classList.remove('active'));

  card.classList.remove('mode-usd', 'mode-khr');

  if (mode === 'usd') {{
    card.classList.add('mode-usd');
    weiText.setAttribute('fill', '#047857');
    document.getElementById('btnUsd').classList.add('active');
  }} else if (mode === 'khr') {{
    card.classList.add('mode-khr');
    weiText.setAttribute('fill', '#7e22ce');
    document.getElementById('btnKhr').classList.add('active');
  }} else {{
    weiText.setAttribute('fill', '#0077b5');
    document.getElementById('btnWei').classList.add('active');
  }}
}}

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

function render() {{
  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  const q = searchQuery.toLowerCase();

  if (currentCategory === 'attributes') {{
    grid.style.display = 'block';
    let html = '<div class="spec-table-container">';
    html += '<div class="section-title"><svg class="keyline-icon" style="color: var(--accent-mint); width: 18px; height: 18px;"><use href="#icon-attributes"/></svg> Dynamic Attributes & Placeholders</div>';
    html += '<table class="spec-table"><thead><tr><th>Tag</th><th>Field Name</th><th>Description / Example</th></tr></thead><tbody>';
    for (const [group, items] of Object.entries(attributes)) {{
      for (const it of items) {{
        if (q && !it.tag.toLowerCase().includes(q) && !it.label.toLowerCase().includes(q)) continue;
        html += `<tr><td><code style="color: var(--accent-mint); font-weight: bold; font-family: var(--font-display);">${{it.tag}}</code></td><td>${{it.label}}</td><td>${{it.example || it.description || ''}}</td></tr>`;
      }}
    }}
    html += '</tbody></table></div>';
    grid.innerHTML = html;
    return;
  }}

  if (currentCategory === 'fonts') {{
    grid.style.display = 'block';
    let html = '<div class="spec-table-container">';
    html += '<div class="section-title"><svg class="keyline-icon" style="color: var(--accent-mint); width: 18px; height: 18px;"><use href="#icon-font"/></svg> Complete 58 Built-in Google Fonts</div>';
    for (const [type, fontList] of Object.entries(typography.googleFonts || {{}})) {{
      html += `<div style="margin-top: 18px; margin-bottom: 8px; color: var(--accent-mint); font-family: var(--font-display); font-weight: 700; text-transform: uppercase; font-size: 13px;">${{type}} (${{fontList.length}} fonts)</div><div style="display: flex; flex-wrap: wrap; gap: 8px;">`;
      for (const font of fontList) {{
        if (q && !font.toLowerCase().includes(q)) continue;
        html += `<span class="pill tag-mint" style="font-size: 13px; padding: 6px 12px; font-family: '${{font}}', sans-serif;">${{font}}</span>`;
      }}
      html += '</div>';
    }}
    html += '</div>';
    grid.innerHTML = html;
    return;
  }}

  grid.style.display = 'grid';

  if (currentCategory === 'elements') {{
    for (const [sub, files] of Object.entries(elements)) {{
      for (const file of files) {{
        if (q && !file.toLowerCase().includes(q) && !sub.toLowerCase().includes(q)) continue;
        const div = document.createElement('div');
        div.className = 'element-card-wrapper';
        div.innerHTML = `
          <div class="element-card-inner">
            <div class="element-preview">
              <img src="elements/${{sub}}/${{file}}" alt="${{file}}">
            </div>
            <div class="element-name">${{file}}</div>
            <div class="pill">${{sub.toUpperCase()}}</div>
            <a href="elements/${{sub}}/${{file}}" download style="font-family: var(--font-display); font-size: 11px; color: var(--accent-mint); text-decoration: none; display: inline-flex; align-items: center; gap: 4px; font-weight: 600;">
              <svg class="keyline-icon" style="width: 12px; height: 12px;"><use href="#icon-download"/></svg>
              Download SVG
            </a>
          </div>
        `;
        grid.appendChild(div);
      }}
    }}
    return;
  }}

  if (currentCategory === 'email') {{
    for (const em of emails) {{
      const name = em.name || 'Email Template';
      if (q && !name.toLowerCase().includes(q)) continue;
      const div = document.createElement('div');
      div.className = 'template-card-wrapper';
      const thumb = em.thumbnail ? `https://certifier-production-amplify.s3.eu-west-1.amazonaws.com/public/${{em.thumbnail}}` : '';
      div.innerHTML = `
        <div class="template-card-inner">
          <div class="card-img-wrap">
            <img src="${{thumb}}" alt="${{name}}" loading="lazy" onerror="this.style.display='none'">
          </div>
          <div class="card-body">
            <div class="card-title">${{name}}</div>
            <div class="card-meta">
              <span class="pill">${{em.type || 'email'}}</span>
              <span class="pill tag-mint">${{em.isSystem ? 'System' : 'Custom'}}</span>
            </div>
          </div>
          <div class="card-links">
            <a href="email_templates/email_templates.json" target="_blank">
              <svg class="keyline-icon"><use href="#icon-code"/></svg>
              View JSON
            </a>
          </div>
        </div>
      `;
      grid.appendChild(div);
    }}
    return;
  }}

  const categories = (currentCategory === 'all') ? Object.keys(templates) : [currentCategory];
  let renderedCount = 0;
  const maxRender = 400;

  for (const cat of categories) {{
    const list = templates[cat] || [];
    const folder = getFolder(cat);

    for (const item of list) {{
      const name = item.name || 'Untitled';
      const meta = item.metadata || {{}};
      const fullText = (name + ' ' + (meta.style || '') + ' ' + (meta.color || '') + ' ' + (meta.category || '')).toLowerCase();
      if (q && !fullText.includes(q)) continue;

      if (renderedCount >= maxRender) break;
      renderedCount++;

      const safe = safeName(name);
      const prefix = `${{safe}}_${{item.id}}`;
      const previewSrc = `${{folder}}/previews/${{prefix}}_preview.png`;
      const jsonSrc = `${{folder}}/json/${{prefix}}.json`;

      const card = document.createElement('div');
      card.className = 'template-card-wrapper';
      card.innerHTML = `
        <div class="template-card-inner">
          <div class="card-img-wrap">
            <img src="${{previewSrc}}" alt="${{name}}" loading="lazy" onerror="this.style.opacity='0.2'">
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
            <a href="${{previewSrc}}" target="_blank">
              <svg class="keyline-icon"><use href="#icon-eye"/></svg>
              HD Preview
            </a>
            <a href="${{jsonSrc}}" target="_blank">
              <svg class="keyline-icon"><use href="#icon-code"/></svg>
              Editable JSON
            </a>
          </div>
        </div>
      `;
      grid.appendChild(card);
    }}
  }}

  if (renderedCount === 0) {{
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 50px; font-family: var(--font-display); font-size: 14px;">No templates found matching your search.</div>';
  }}
}}

document.getElementById('search').addEventListener('input', (e) => {{
  searchQuery = e.target.value;
  render();
}});

document.querySelectorAll('.stepper-tab-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.stepper-tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentCategory = btn.getAttribute('data-cat');
    render();
  }});
}});

render();
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
