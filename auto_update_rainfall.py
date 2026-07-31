import os
import sys
import glob
import json
import datetime
import webbrowser
import subprocess
import pandas as pd
import re
import ssl
import urllib.request
import urllib.parse
import shutil

PERIOD_KEYS = [
    'jan', 'feb', 'jan_feb', 'mar', 'apr', 'may', 'pre_monsoon',
    'june', 'last_24h', 'last_7d', 'july_mtd', 'sw_monsoon', 'oct', 'nov', 'dec', 'ne_monsoon', 'ytd'
]

def safe_float(v):
    try:
        if pd.isna(v): return 0.0
        return round(float(v), 1)
    except:
        return 0.0

def safe_str(v):
    if pd.isna(v): return ""
    return str(v).strip()

def extract_data_date(excel_path):
    try:
        df_top = pd.read_excel(excel_path, sheet_name='District', header=None, nrows=6)
        text = ' '.join([str(x) for x in df_top.fillna('').values.flatten()])
        match = re.search(r'As on\s+([0-9]{1,2}[\-/.\s]+[0-9]{1,2}[\-/.\s]+[0-9]{2,4}|\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s*[\-–]?\s*\d{4})', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    except Exception as e:
        print(f"[WARN] Failed to extract date from Excel header: {e}")
    
    try:
        mtime = os.path.getmtime(excel_path)
        return datetime.datetime.fromtimestamp(mtime).strftime("%d-%b-%Y")
    except:
        return datetime.datetime.now().strftime("%d-%b-%Y")

def extract_period_dates(excel_path):
    try:
        df = pd.read_excel(excel_path, sheet_name='District', header=None, nrows=4)
        row2 = df.iloc[2].fillna('').to_dict()
        keys = ['jan', 'feb', 'jan_feb', 'mar', 'apr', 'may', 'pre_monsoon', 'june', 'last_24h', 'last_7d', 'july_mtd', 'sw_monsoon', 'ytd']
        col_indices = [7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43]
        raw = {}
        for k, c in zip(keys, col_indices):
            raw[k] = str(row2.get(c, '')).replace('\n', ' ').strip()
            
        m_sw = re.search(r'to\s+(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+)', raw.get('sw_monsoon', ''), re.I)
        end_date = m_sw.group(1).strip() if m_sw else '23rd July'
        
        m_7d = re.search(r'(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s*to\s*\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+(?:\s*\d{4})?)', raw.get('last_7d', ''), re.I)
        l7d_str = m_7d.group(1).strip() if m_7d else f'17th July to {end_date}'
        
        m_24h = re.search(r'of\s+(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+(?:\s*[\-–]?\s*\d{4})?)', raw.get('last_24h', ''), re.I)
        l24h_str = m_24h.group(1).strip() if m_24h else end_date
        
        return {
            'sw_monsoon': f'June 1 – {end_date}',
            'ne_monsoon': 'Oct 1 – Dec 31',
            'july_mtd': f'July 1 – {end_date}',
            'last_7d': l7d_str,
            'last_24h': f'Ending 8:30 AM of {l24h_str}',
            'pre_monsoon': 'March 1 – May 31',
            'ytd': f'Jan 1 – {end_date}',
            'end_date': end_date
        }
    except Exception as e:
        print(f"[WARN] Failed to extract period dates: {e}")
        return {
            'sw_monsoon': 'June 1 – July 23',
            'ne_monsoon': 'Oct 1 – Dec 31',
            'july_mtd': 'July 1 – July 23',
            'last_7d': '17th July to 23rd July 2026',
            'last_24h': 'Ending 8:30 AM of 23rd July -2026',
            'pre_monsoon': 'March 1 – May 31',
            'ytd': 'Jan 1 – July 23',
            'end_date': '23rd July'
        }

def parse_ksndmc_excel(excel_path):
    print(f"[INFO] Reading KSNDMC Excel: {excel_path}")
    updated_date = extract_data_date(excel_path)
    period_dates = extract_period_dates(excel_path)
    print(f"[INFO] Extracted Data Updated Date: {updated_date}")
    print(f"[INFO] Extracted Period End Date: {period_dates.get('end_date')}")
    
    # 1. Parse District Sheet
    df_dist = pd.read_excel(excel_path, sheet_name='District')
    districts_data = {}
    
    # District data rows start at row index 5
    for idx in range(5, len(df_dist)):
        row = df_dist.iloc[idx]
        dist_name = safe_str(row.iloc[6])
        if not dist_name or dist_name.lower().startswith('total') or dist_name.lower().startswith('sl.'):
            continue
        
        sl_no = safe_str(row.iloc[0])
        code = safe_str(row.iloc[1])
        region = safe_str(row.iloc[2])
        division = safe_str(row.iloc[5])
        
        # Only parse actual district rows with numeric sl_no (1-31)
        if not sl_no.isdigit():
            continue
        
        dist_entry = {
            "slNo": int(sl_no),
            "code": code,
            "region": region,
            "division": division
        }
        
        col_offset = 7
        for pkey in PERIOD_KEYS:
            if col_offset + 2 < len(row):
                norm = safe_float(row.iloc[col_offset])
                act = safe_float(row.iloc[col_offset + 1])
                dep = safe_float(row.iloc[col_offset + 2])
            else:
                norm, act, dep = 0.0, 0.0, 0.0
            dist_entry[pkey] = {"normal": norm, "actual": act, "dep": dep}
            col_offset += 3
            
        districts_data[dist_name] = dist_entry

    # 2. Parse Taluk Sheet
    df_taluk = pd.read_excel(excel_path, sheet_name='Taluk')
    taluks_data = []
    
    # Taluk data rows start at row index 4
    for idx in range(4, len(df_taluk)):
        row = df_taluk.iloc[idx]
        dist_name = safe_str(row.iloc[8])
        taluk_name = safe_str(row.iloc[9])
        if not dist_name or not taluk_name or taluk_name.lower().startswith('total'):
            continue
        
        region = safe_str(row.iloc[4])
        division = safe_str(row.iloc[7])
        
        taluk_entry = {
            "dist": dist_name,
            "taluk": taluk_name,
            "region": region,
            "division": division
        }
        
        col_offset = 11
        for pkey in PERIOD_KEYS:
            if col_offset + 2 < len(row):
                norm = safe_float(row.iloc[col_offset])
                act = safe_float(row.iloc[col_offset + 1])
                dep = safe_float(row.iloc[col_offset + 2])
            else:
                norm, act, dep = 0.0, 0.0, 0.0
            taluk_entry[pkey] = {"normal": norm, "actual": act, "dep": dep}
            col_offset += 3
            
        taluks_data.append(taluk_entry)
        
    return {"districts": districts_data, "taluks": taluks_data, "updated_date": updated_date, "period_dates": period_dates}

def update_html_from_json(json_data, base_dir):
    json_path = os.path.join(base_dir, 'data_embedded.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    print(f"[SUCCESS] Updated {json_path}")
    
    json_districts = json.dumps(json_data['districts'])
    json_taluks = json.dumps(json_data['taluks'])
    updated_date = json_data.get('updated_date', '')
    json_period_dates = json.dumps(json_data.get('period_dates', {}))
    
    template_path = os.path.join(base_dir, 'template_rainfall_status.html')
    if not os.path.exists(template_path):
        template_path = os.path.join(os.path.dirname(base_dir), 'template_rainfall_status.html')
        
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    html = html.replace('__JSON_DISTRICTS__', json_districts)
    html = html.replace('__JSON_TALUKS__', json_taluks)
    html = html.replace('__JSON_UPDATED_DATE__', updated_date)
    html = html.replace('__JSON_PERIOD_DATES__', json_period_dates)
    
    for fname in ['index.html', 'rainfall status.html', 'rainfall_status.html']:
        out_path = os.path.join(base_dir, fname)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"[SUCCESS] Updated {fname}")

def check_and_download_ksndmc_report(target_dir):
    print("[INFO] Checking KSNDMC website (https://www.ksndmc.org/ReportHomePage.aspx/Reports/Daily)...")
    urls_to_check = [
        "https://www.ksndmc.org/ReportHomePage.aspx/Reports/Daily",
        "https://www.ksndmc.org/ReportHomePage.aspx/DailyReport/getDailyReport",
        "https://www.ksndmc.org/ReportHomePage.aspx",
        "https://www.ksndmc.org/",
        "https://ksndmc.karnataka.gov.in"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for page_url in urls_to_check:
        try:
            req = urllib.request.Request(page_url, headers=headers)
            html = urllib.request.urlopen(req, context=ctx, timeout=8).read().decode('utf-8', errors='ignore')
            xls_links = re.findall(r'href=["\']([^"\']+\.xls[x]?)["\']', html, re.I)
            if xls_links:
                for link in xls_links:
                    if not link.startswith('http'):
                        link = urllib.parse.urljoin(page_url, link)
                    print(f"[INFO] Found online report link: {link}")
                    out_file = os.path.join(target_dir, f"KSNDMC_AutoDownload_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
                    print(f"[INFO] Downloading latest report to {out_file}...")
                    urllib.request.urlretrieve(link, out_file)
                    print(f"[SUCCESS] Downloaded updated report from KSNDMC website!")
                    return out_file
        except Exception as e:
            continue

    print("[INFO] KSNDMC online check complete. (Proceeding with latest report in Downloads / workspace)")
    return None

def sync_to_github(base_dir, updated_date):
    print("\n[INFO] Syncing updated dashboard to GitHub repository...")
    try:
        subprocess.run(["git", "add", "."], cwd=base_dir, check=True)
        status = subprocess.run(["git", "status", "--porcelain"], cwd=base_dir, capture_output=True, text=True)
        has_changes = bool(status.stdout.strip())
        
        if not has_changes:
            print("[INFO] GitHub repository is already up-to-date! No local changes to commit.")
        else:
            commit_msg = f"Auto-update rainfall status data - {updated_date} ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=base_dir, check=True)
            print(f"[SUCCESS] Committed changes: '{commit_msg}'")
        
        choice = input("\nDo you want to push these updates to GitHub now? (Y/N): ").strip().upper()
        if choice == 'Y':
            print("[INFO] Pushing changes to GitHub (origin/main)...")
            push_res = subprocess.run(["git", "push", "origin", "main"], cwd=base_dir, capture_output=True, text=True)
            if push_res.returncode == 0:
                print("[SUCCESS] Successfully updated GitHub repository!")
                print("[LIVE DASHBOARD URL] https://amith1994.github.io/Rainfall_status_of_Karnataka/")
                return True
            else:
                print(f"[WARN] Git push output: {push_res.stderr or push_res.stdout}")
        else:
            print("[INFO] Git push skipped. Local files are updated.")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to push to GitHub: {e}")
    return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    user_home = os.path.expanduser("~")
    downloads_dir = os.path.join(user_home, "Downloads")
    desktop_dir = os.path.join(user_home, "Desktop")
    onedrive_desktop = os.path.join(user_home, "OneDrive", "Desktop")
    
    print("=" * 60)
    print("  KSNDMC DAILY RAINFALL STATUS AUTOMATED UPDATER")
    print("=" * 60)
    
    # Check online website for updated reports
    check_and_download_ksndmc_report(downloads_dir)
    
    # Find candidate excel files across Downloads, Desktop, and Workspace
    search_dirs = [script_dir, parent_dir, downloads_dir, desktop_dir, onedrive_desktop]
    search_patterns = [
        "*.xlsx", "*.xls",
        "*Rainfall*.xlsx", "*Rainfall*.xls",
        "*KSNDMC*.xlsx", "*KSNDMC*.xls",
        "*Karnataka*.xlsx", "*Karnataka*.xls"
    ]
    
    candidate_files = []
    for sdir in search_dirs:
        if not os.path.exists(sdir):
            continue
        for pat in search_patterns:
            candidate_files.extend(glob.glob(os.path.join(sdir, pat)))
        
    # Remove duplicates & exclude temporary Excel files (~$)
    candidate_files = list(set(candidate_files))
    candidate_files = [f for f in candidate_files if not os.path.basename(f).startswith("~$")]
    
    if not candidate_files:
        print("[ERROR] No Rainfall Excel file found!")
        print("Please place your Excel file in Downloads, Desktop, or the Rainfall_Status_App folder.")
        input("Press Enter to exit...")
        return
        
    latest_excel = max(candidate_files, key=os.path.getmtime)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(latest_excel)).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[INFO] Detected Latest Excel File: {latest_excel}")
    print(f"[INFO] File Modified Time: {mtime}")
    
    target_excel = os.path.join(script_dir, "Rainfall status.xlsx")
    if os.path.abspath(latest_excel).lower() != os.path.abspath(target_excel).lower():
        try:
            print(f"[INFO] Synchronizing '{os.path.basename(latest_excel)}' -> '{target_excel}'...")
            shutil.copy2(latest_excel, target_excel)
            latest_excel = target_excel
            print(f"[SUCCESS] Updated local Excel file repository!")
        except Exception as e:
            print(f"[WARN] Could not copy Excel file: {e}")

    json_data = parse_ksndmc_excel(latest_excel)
    print(f"[INFO] Parsed {len(json_data['districts'])} Districts & {len(json_data['taluks'])} Taluks.")
    
    update_html_from_json(json_data, script_dir)
    
    # Sync updated files to GitHub repository
    sync_to_github(script_dir, json_data.get('updated_date', ''))
    
    target_html = os.path.join(script_dir, 'rainfall_status.html')
    print(f"\n[INFO] Launching Karnataka Current Status of Rainfall App in browser...")
    webbrowser.open(f"file:///{target_html}")
    print("[DONE] Update process completed successfully!\n")

if __name__ == '__main__':
    main()
