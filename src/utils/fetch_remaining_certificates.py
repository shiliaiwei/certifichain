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

def fetch_json_with_retry(url, max_retries=6):
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = int(e.headers.get("Retry-After", 15))
                # Add slight jitter/wait
                time.sleep(retry_after + 2)
            else:
                time.sleep(2)
        except Exception:
            time.sleep(2)
    return None

def process_one(item, cat_dir):
    tpl_id = item.get("id")
    tpl_name = item.get("name", "template")
    safe_name = safe_filename(tpl_name)
    prefix = f"{safe_name}_{tpl_id}"

    detail_file = os.path.join(cat_dir, "json", f"{prefix}.json")
    if os.path.exists(detail_file) and os.path.getsize(detail_file) > 10:
        return tpl_id, True

    detail_url = f"{API_BASE}/app/designs/default-templates/{tpl_id}"
    detail = fetch_json_with_retry(detail_url)
    if detail:
        os.makedirs(os.path.join(cat_dir, "json"), exist_ok=True)
        with open(detail_file, "w", encoding="utf-8") as f:
            json.dump(detail, f, indent=2)

        # Download HD background if present
        if "background" in detail and isinstance(detail["background"], dict):
            bg_url_rel = detail["background"].get("url")
            if bg_url_rel:
                bg_full_url = f"{S3_CDN}/{bg_url_rel}"
                ext = os.path.splitext(bg_url_rel)[1] or ".png"
                bg_target = os.path.join(cat_dir, "backgrounds", f"{prefix}_bg{ext}")
                download_file(bg_full_url, bg_target)
        return tpl_id, True
    return tpl_id, False

def main():
    cat_dir = os.path.join(BASE_DIR, "certificates")
    json_dir = os.path.join(cat_dir, "json")
    os.makedirs(json_dir, exist_ok=True)

    with open(os.path.join(BASE_DIR, "catalogs", "certificates.json")) as f:
        items = json.load(f)

    existing_files = set(os.listdir(json_dir))
    todo = []
    for it in items:
        tid = it["id"]
        # check if tid is in any existing filename
        if not any(tid in f for f in existing_files):
            todo.append(it)

    print(f"Total certificates: {len(items)}, Already downloaded: {len(existing_files)}, Remaining to fetch: {len(todo)}")

    if not todo:
        print("All certificates are already 100% downloaded!")
        return

    # Use 6 workers with gentle spacing to avoid aggressive rate limiting
    success = 0
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(process_one, item, cat_dir): item for item in todo}
        for future in as_completed(futures):
            tpl_id, ok = future.result()
            if ok:
                success += 1
            if success % 50 == 0 or success == len(todo):
                print(f"[Certificates JSON] Downloaded {success}/{len(todo)} missing design schemas...")
            time.sleep(0.08) # gentle delay between task handoffs

    print(f"\nFinished fetching remaining certificates: {success} newly fetched.")

if __name__ == "__main__":
    main()
