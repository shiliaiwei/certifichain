import json
import os
import shutil

BASE_DIR = "/Users/Apple16/Downloads/cetif"
OUT_DIR = os.path.join(BASE_DIR, "Templates")
os.makedirs(OUT_DIR, exist_ok=True)

CATEGORIES = [
    ("certificates", "01 Certificates"),
    ("badges", "02 Badges"),
    ("transcripts", "03 Transcripts"),
    ("training_records", "04 Training Records"),
    ("assessments", "05 Assessments"),
    ("letters", "06 Letters"),
]

def safe_filename(name):
    import re
    clean = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', name)
    return clean.strip('_')[:80]

def organize():
    total_copied = 0

    for cat_slug, cat_display in CATEGORIES:
        catalog_file = os.path.join(BASE_DIR, "catalogs", f"{cat_slug}.json")
        if not os.path.exists(catalog_file):
            continue

        with open(catalog_file, "r", encoding="utf-8") as f:
            items = json.load(f)

        src_cat_dir = os.path.join(BASE_DIR, cat_slug)
        src_previews = os.path.join(src_cat_dir, "previews")
        src_json = os.path.join(src_cat_dir, "json")

        # Map existing preview and json files by template id
        preview_map = {}
        if os.path.exists(src_previews):
            for f in os.listdir(src_previews):
                for it in items:
                    tid = it["id"]
                    if tid in f:
                        preview_map[tid] = os.path.join(src_previews, f)
                        break

        json_map = {}
        if os.path.exists(src_json):
            for f in os.listdir(src_json):
                for it in items:
                    tid = it["id"]
                    if tid in f:
                        json_map[tid] = os.path.join(src_json, f)
                        break

        cat_target = os.path.join(OUT_DIR, cat_display)

        for it in items:
            tid = it["id"]
            name = it.get("name", "template")
            safe = safe_filename(name)
            prefix = f"{safe}_{tid}"

            orientation = it.get("orientation")
            if orientation in ["landscape", "portrait"]:
                dest_dir = os.path.join(cat_target, orientation.capitalize())
            else:
                dest_dir = cat_target

            dest_images = os.path.join(dest_dir, "images")
            dest_schemas = os.path.join(dest_dir, "templates_json")
            os.makedirs(dest_images, exist_ok=True)
            os.makedirs(dest_schemas, exist_ok=True)

            # Link/Copy Image Preview
            if tid in preview_map:
                src_img = preview_map[tid]
                ext = os.path.splitext(src_img)[1] or ".png"
                dst_img = os.path.join(dest_images, f"{prefix}{ext}")
                if not os.path.exists(dst_img):
                    try:
                        os.link(src_img, dst_img)
                    except Exception:
                        shutil.copy2(src_img, dst_img)
                total_copied += 1

            # Link/Copy JSON Schema
            if tid in json_map:
                src_j = json_map[tid]
                dst_j = os.path.join(dest_schemas, f"{prefix}.json")
                if not os.path.exists(dst_j):
                    try:
                        os.link(src_j, dst_j)
                    except Exception:
                        shutil.copy2(src_j, dst_j)
                total_copied += 1

    print(f"Successfully organized all templates into {OUT_DIR}")

if __name__ == "__main__":
    organize()
