import urllib.request
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = "/Users/Apple16/Downloads/cetif"
API_BASE = "https://api.certifier.io"
S3_CDN = "https://certifier-production-amplify.s3.eu-west-1.amazonaws.com/public"

HEADERS = {
    "authorization": "eyJraWQiOiJRclpoQXVtQ0VuNDhnUk9YM0V2YkpNN1FsS0ppSHgwTzh0WnBYdjNzV0ZRPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiMU45M09USlNfV0ZUc29sRjNDM3RXQSIsInN1YiI6IjEyZjU5NDI0LTIwYjEtNzA5My1hOTQ1LTRkYjMwY2E3ZDIyMCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tL2V1LXdlc3QtMV9PZXRESnVncmMiLCJjb2duaXRvOnVzZXJuYW1lIjoiMTJmNTk0MjQtMjBiMS03MDkzLWE5NDUtNGRiMzBjYTdkMjIwIiwibm9uY2UiOiJocExuWHJHeUhldzNVWlY2clNBTE15WEZDV1dBR0N4bjNvNjM1QXY4TERMb194VTRVd3JYOE5LRWg0VjR2R0VScHpfM0RhNDAwdUFNeWFnUExpc1QteUdLQWQ0S0podE9kNU9XU0ludjRzdjVDcF84Ti1ULTdQNGxmYml2V2NLaVVmX3dlUGE5cENob3FFSFlVUXVEdjJaRnBMUkxlcEVCbHZYdW5TdzB4SW8iLCJhdWQiOiI1M2gwdTgwcHBwbmlsaDhoMTRrMzE4NTA2MCIsImlkZW50aXRpZXMiOlt7ImRhdGVDcmVhdGVkIjoiMTc5MjM4MTkyNDExOSIsInVzZXJJZCI6IjExMzMxMjc4NDE3Mjk5NDcyNTI2NyIsInByb3ZpZGVyTmFtZSI6Ikdvb2dsZSIsInByb3ZpZGVyVHlwZSI6Ikdvb2dsZSIsImlzc3VlciI6bnVsbCwicHJpbWFyeSI6ImZhbHNlIn1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTc5MjM4MTkyNiwiZXhwIjoxNzkyNDI1MTI2LCJpYXQiOjE3OTIzODE5MjYsImVtYWlsIjoiYWl3ZWkuYWxpYXNAYXRvbWljbWFpbC5pbyJ9.ZdrcTQ0QaNPXpNjGb4whFJbHeaxm6jOFlFtDodYJAC8E06AqcrKwvKJOqyKaRLiUHJbevF6SS1lezNpNtrmgPB1vcW8tJzWpdYWhlx2riS6_Cj_oDNC5BKuFVEoc_IKcr_ZE3qZw-VsJmCVDabhAVBZl0-hnIt9kjKwToCGi3oo8X1WNEERZ028E7JYGHqI5jgiL4OHPlEtAJkKprm2_JxS4l2PWfMLPIgVNsK_FFSb9OKKVO3pEVi9CWSYSQrN9YMLawmbVomVXYX5COGNqjEziK_Xa_H-ZAJJynbPubhpVP5ULamU_-jSgeh4o7yUi9j1yuwxAdstaGJLRyxiAgA",
    "certifier-workspace-id": "01m594kcbepn16jte3y0h9f8xy",
    "certifier-version": "2022-10-26",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

def safe_filename(name):
    clean = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', name)
    return clean.strip('_')[:80]

def download_file(url, target_path):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        return True
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"user-agent": HEADERS["user-agent"]})
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read()
                with open(target_path, "wb") as f:
                    f.write(content)
            return True
        except Exception:
            time.sleep(1)
    return False

def fetch_json(url, headers=None):
    if headers is None:
        headers = HEADERS
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            time.sleep(1)
    return None

def process_template(item, cat_dir):
    tpl_id = item.get("id")
    tpl_name = item.get("name", "template")
    safe_name = safe_filename(tpl_name)
    prefix = f"{safe_name}_{tpl_id}"

    # 1. Fetch full template detail JSON
    detail_file = os.path.join(cat_dir, "json", f"{prefix}.json")
    detail = None
    if os.path.exists(detail_file) and os.path.getsize(detail_file) > 0:
        try:
            with open(detail_file, "r") as f:
                detail = json.load(f)
        except Exception:
            detail = None

    if not detail:
        detail_url = f"{API_BASE}/app/designs/default-templates/{tpl_id}"
        detail = fetch_json(detail_url)
        if detail:
            os.makedirs(os.path.join(cat_dir, "json"), exist_ok=True)
            with open(detail_file, "w", encoding="utf-8") as f:
                json.dump(detail, f, indent=2)

    # 2. Download HD Background
    if detail and "background" in detail and isinstance(detail["background"], dict):
        bg_url_rel = detail["background"].get("url")
        if bg_url_rel:
            bg_full_url = f"{S3_CDN}/{bg_url_rel}"
            ext = os.path.splitext(bg_url_rel)[1] or ".png"
            bg_target = os.path.join(cat_dir, "backgrounds", f"{prefix}_bg{ext}")
            download_file(bg_full_url, bg_target)

    # 3. Download Preview Thumbnail
    thumb_rel = item.get("thumbnail") or (detail.get("thumbnail") if detail else None)
    if thumb_rel:
        thumb_full_url = f"{S3_CDN}/{thumb_rel}"
        ext = os.path.splitext(thumb_rel)[1] or ".png"
        thumb_target = os.path.join(cat_dir, "previews", f"{prefix}_preview{ext}")
        download_file(thumb_full_url, thumb_target)

    return tpl_id

def main():
    cat_dir = os.path.join(BASE_DIR, "certificates")
    os.makedirs(cat_dir, exist_ok=True)

    print("--- Fetching catalog for category: certificate (2,137 templates) ---")
    cat_url = f"{API_BASE}/app/designs/default-templates?size=3000&type=certificate"
    cat_data = fetch_json(cat_url)
    items = cat_data.get("list", []) if cat_data else []
    print(f"Total templates in certificate: {len(items)}")

    cat_catalog_path = os.path.join(BASE_DIR, "catalogs", "certificates.json")
    with open(cat_catalog_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    # Update master_catalog
    master_path = os.path.join(BASE_DIR, "catalogs", "catalog_all.json")
    master_catalog = {}
    if os.path.exists(master_path):
        try:
            with open(master_path, "r") as f:
                master_catalog = json.load(f)
        except Exception:
            pass
    master_catalog["certificate"] = items
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, indent=2)

    print(f"Processing and downloading HD assets for {len(items)} certificate templates with 32 workers...")
    completed = 0
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(process_template, item, cat_dir) for item in items]
        for future in as_completed(futures):
            res = future.result()
            completed += 1
            if completed % 100 == 0 or completed == len(items):
                print(f"[certificates] Progress: {completed}/{len(items)} templates processed")

    print("\nAll 2,137 certificate templates and HD assets processed successfully!")

if __name__ == "__main__":
    main()
