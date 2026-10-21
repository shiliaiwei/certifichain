import json
import glob
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def update_json_file(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)

    bg = data.get("background")
    modified = False

    if bg is None:
        data["background"] = {"type": "color", "value": "#ffffff"}
        modified = True
    elif isinstance(bg, dict):
        if bg.get("value") != "#ffffff":
            bg["value"] = "#ffffff"
            modified = True
    elif isinstance(bg, str):
        data["background"] = {"type": "color", "value": "#ffffff"}
        modified = True

    if modified:
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    return False

def main():
    cats = ["certificates", "badges", "transcripts", "training_records", "assessments", "letters"]
    updated_cat_count = 0
    total_cat_files = 0

    for cat in cats:
        pattern = os.path.join(BASE_DIR, cat, "json", "*.json")
        files = glob.glob(pattern)
        total_cat_files += len(files)
        for p in files:
            if update_json_file(p):
                updated_cat_count += 1

    print(f"Categories JSON files updated: {updated_cat_count} / {total_cat_files}")

    tpl_pattern_1 = os.path.join(BASE_DIR, "Templates", "*", "*", "*.json")
    tpl_pattern_2 = os.path.join(BASE_DIR, "Templates", "*", "*", "*", "*.json")
    tpl_files = glob.glob(tpl_pattern_1) + glob.glob(tpl_pattern_2)
    updated_tpl_count = 0

    for p in tpl_files:
        if update_json_file(p):
            updated_tpl_count += 1

    print(f"Templates JSON files updated: {updated_tpl_count} / {len(tpl_files)}")

if __name__ == "__main__":
    main()
