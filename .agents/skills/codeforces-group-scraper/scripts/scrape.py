#!/usr/bin/env python3
import sys
import time
import json
import argparse
import urllib.request
import urllib.error
from html.parser import HTMLParser

# Base URL for Codeforces
BASE_URL = "https://codeforces.com"

class ContestsParser(HTMLParser):
    def __init__(self, group_id):
        super().__init__()
        self.group_id = group_id
        self.contests = []
        self.in_table = False
        self.in_row = False
        self.cell_index = -1
        self.in_cell = False
        self.current_cell_text = ""
        self.current_href = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "table":
            self.in_table = True
        elif self.in_table:
            if tag == "tr":
                self.in_row = True
                self.cell_index = -1
            elif self.in_row:
                if tag in ["td", "th"]:
                    self.in_cell = True
                    self.cell_index += 1
                    if self.cell_index == 0:
                        self.current_cell_text = ""
                        self.current_href = None
                elif self.in_cell and self.cell_index == 0:
                    if tag == "a":
                        href = attrs_dict.get("href", "")
                        if f"/group/{self.group_id}/contest/" in href:
                            parts = href.split("/")
                            if parts[-1].isdigit():
                                self.current_href = parts[-1]

    def handle_data(self, data):
        if self.in_cell and self.cell_index == 0:
            self.current_cell_text += data

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        elif self.in_table:
            if tag == "tr":
                self.in_row = False
                if self.current_href and self.current_cell_text:
                    raw_text = self.current_cell_text.strip()
                    raw_text = " ".join(raw_text.split())
                    name = raw_text
                    for marker in ["Enter »", "Enter", "Virtual", "virtual participation"]:
                        if marker in name:
                            name = name.split(marker)[0].strip()
                            
                    if name and not any(c["id"] == self.current_href for c in self.contests):
                        self.contests.append({"id": self.current_href, "name": name})
            elif self.in_row:
                if tag in ["td", "th"]:
                    self.in_cell = False

class SubmissionsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_cell_text = ""
        self.current_row = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "table":
            # Codeforces status table
            cls = attrs_dict.get("class", "")
            if "status-frame-datatable" in cls:
                self.in_table = True
        elif self.in_table:
            if tag == "tr":
                self.in_row = True
                self.current_row = []
            elif self.in_row:
                if tag in ["td", "th"]:
                    self.in_cell = True
                    self.current_cell_text = ""

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell_text += data

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        elif self.in_table:
            if tag == "tr":
                self.in_row = False
                if self.current_row:
                    self.rows.append(self.current_row)
            elif self.in_row:
                if tag in ["td", "th"]:
                    self.in_cell = False
                    text = " ".join(self.current_cell_text.split())
                    self.current_row.append(text)

def make_request(url, cookies_str):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    req.add_header("Accept-Language", "es-ES,es;q=0.9,en;q=0.8")
    req.add_header("Cookie", cookies_str)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode("utf-8"), response.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception as e:
        print(f"Error connecting: {e}", file=sys.stderr)
        return "", 0

def get_group_contests(group_id, cookies_str):
    url = f"{BASE_URL}/group/{group_id}/contests"
    print(f"Fetching contests from: {url}")
    html_content, status = make_request(url, cookies_str)
    
    if status != 200:
        print(f"Error fetching contests page: HTTP {status}", file=sys.stderr)
        if status == 403:
            print("Hint: Make sure your JSESSIONID and 39ceb cookies are correct.", file=sys.stderr)
        return []
        
    parser = ContestsParser(group_id)
    parser.feed(html_content)
    print(f"Found {len(parser.contests)} contests.")
    return parser.contests

def scrape_submissions(group_id, contest_id, cookies_str):
    submissions = []
    page = 1
    seen_ids = set()
    
    while True:
        url = f"{BASE_URL}/group/{group_id}/contest/{contest_id}/status?pageIndex={page}"
        print(f"  Fetching submissions for page {page} for contest {contest_id}...")
        html_content, status = make_request(url, cookies_str)
        
        if status != 200:
            print(f"  Error fetching page {page}: HTTP {status}", file=sys.stderr)
            break
            
        parser = SubmissionsParser()
        parser.feed(html_content)
        
        rows = parser.rows
        if len(rows) <= 1:
            print("  No submissions table found or table is empty. Stopping.")
            break
            
        # Parse headers to identify columns
        headers = [h.lower() for h in rows[0]]
        
        col_indices = {
            "id": -1,
            "who": -1,
            "problem": -1,
            "lang": -1,
            "verdict": -1,
            "when": -1
        }
        
        for idx, h in enumerate(headers):
            if "#" in h or "id" in h:
                col_indices["id"] = idx
            elif "who" in h or "author" in h or "usuario" in h:
                col_indices["who"] = idx
            elif "problem" in h or "problema" in h:
                col_indices["problem"] = idx
            elif "lang" in h or "lenguaje" in h:
                col_indices["lang"] = idx
            elif "verdict" in h or "resultado" in h or "sentencia" in h:
                col_indices["verdict"] = idx
            elif "when" in h or "cuando" in h or "fecha" in h:
                col_indices["when"] = idx
                
        # Parse rows
        page_subs = 0
        new_subs = 0
        for row in rows[1:]:
            if not row or len(row) < max(col_indices.values()) + 1:
                continue
                
            sub_id = row[col_indices["id"]] if col_indices["id"] != -1 else ""
            who = row[col_indices["who"]] if col_indices["who"] != -1 else ""
            problem = row[col_indices["problem"]] if col_indices["problem"] != -1 else ""
            lang = row[col_indices["lang"]] if col_indices["lang"] != -1 else ""
            verdict = row[col_indices["verdict"]] if col_indices["verdict"] != -1 else ""
            when = row[col_indices["when"]] if col_indices["when"] != -1 else ""
            
            # Skip if we didn't get any sub ID
            if not sub_id:
                continue
                
            if sub_id in seen_ids:
                continue
                
            seen_ids.add(sub_id)
            submissions.append({
                "submission_id": sub_id,
                "contest_id": contest_id,
                "user": who,
                "problem": problem,
                "language": lang,
                "verdict": verdict,
                "when": when
            })
            page_subs += 1
            new_subs += 1
            
        print(f"  Parsed {page_subs} submissions ({new_subs} new).")
        if new_subs == 0:
            break
            
        page += 1
        time.sleep(1.2) # Polite scraping delay
        
    return submissions

def main():
    parser = argparse.ArgumentParser(description="Scrape submissions from a Codeforces Group (Standard Library Only)")
    parser.add_argument("--group", default="GHvtTrfZFd", help="Group ID (from URL, e.g., GHvtTrfZFd)")
    parser.add_argument("--cookies", help="Full cookie string (e.g. from document.cookie in browser console)")
    parser.add_argument("--jsessionid", help="JSESSIONID cookie value (alternative)")
    parser.add_argument("--secret-cookie-name", default="39ceb", help="Name of the session tracking cookie (e.g. 39ceb, 39ce7)")
    parser.add_argument("--secret-cookie-value", help="Value of the session tracking cookie")
    parser.add_argument("--output", default="submissions.json", help="Path to output JSON file")
    args = parser.parse_args()
    
    if args.cookies:
        cookies_str = args.cookies
    elif args.jsessionid and args.secret_cookie_value:
        cookies_str = f"JSESSIONID={args.jsessionid}; {args.secret_cookie_name}={args.secret_cookie_value}"
    else:
        parser.error("Either --cookies or both --jsessionid and --secret-cookie-value must be provided.")
    
    # 1. Fetch group contests
    contests = get_group_contests(args.group, cookies_str)
    if not contests:
        print("No contests found. Exiting.")
        return
        
    # 2. Iterate through each contest and scrape submissions
    all_submissions = []
    
    for c in contests:
        c_id = c["id"]
        c_name = c["name"]
        print(f"Scraping contest {c_id}: {c_name}...")
        subs = scrape_submissions(args.group, c_id, cookies_str)
        print(f"Found {len(subs)} submissions for contest {c_id}.\n")
        all_submissions.extend(subs)
        time.sleep(2) # Delay between contests
        
    # 3. Save to JSON
    output_data = {
        "group_id": args.group,
        "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "contests": contests,
        "total_submissions": len(all_submissions),
        "submissions": all_submissions
    }
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
        
    print(f"Saved {len(all_submissions)} submissions to {args.output}")

if __name__ == "__main__":
    main()
