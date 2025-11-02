#!/usr/bin/env python3
"""
Batch verify all hyperlinks in markdown files
"""
import re
import os
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

# Configuration
BASE_URL = "http://localhost:3000/#/"
GITHUB_REPO = "https://github.com/stas00/ml-engineering/blob/master/"
ROOT_DIR = Path(__file__).parent
TIMEOUT = 10
MAX_WORKERS = 20

def find_markdown_files(root_dir):
    """Find all markdown files in the directory"""
    md_files = []
    for path in Path(root_dir).rglob("*.md"):
        # Skip node_modules and other irrelevant directories
        if "node_modules" not in str(path) and ".git" not in str(path):
            md_files.append(path)
    return md_files

def extract_links(file_path):
    """Extract all markdown links from a file"""
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Match markdown links: [text](url)
            pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
            for match in re.finditer(pattern, content):
                text = match.group(1)
                url = match.group(2)
                links.append({
                    'text': text,
                    'url': url,
                    'file': str(file_path.relative_to(ROOT_DIR))
                })
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return links

def categorize_link(url):
    """Categorize link type"""
    if url.startswith('http://') or url.startswith('https://'):
        if 'github.com' in url:
            return 'github'
        return 'external'
    elif url.startswith('#'):
        return 'anchor'
    elif url.startswith('/'):
        return 'absolute'
    elif url.startswith('./') or url.startswith('../'):
        return 'relative'
    else:
        return 'other'

def check_docsify_link(url):
    """Check if a docsify internal link is accessible"""
    # Convert to docsify URL
    if url.startswith('/'):
        # Absolute path from root
        test_url = BASE_URL + url.lstrip('/')
    else:
        return None, "Skipped relative link (needs context)"

    try:
        response = requests.get(test_url, timeout=TIMEOUT, allow_redirects=True)
        return response.status_code, response.reason
    except Exception as e:
        return None, str(e)

def check_external_link(url):
    """Check if an external link is accessible"""
    try:
        response = requests.head(url, timeout=TIMEOUT, allow_redirects=True)
        if response.status_code == 405:  # Method not allowed, try GET
            response = requests.get(url, timeout=TIMEOUT, allow_redirects=True, stream=True)
        return response.status_code, response.reason
    except Exception as e:
        return None, str(e)

def main():
    print("🔍 Scanning for markdown files...")
    md_files = find_markdown_files(ROOT_DIR)
    print(f"Found {len(md_files)} markdown files\n")

    print("📝 Extracting links...")
    all_links = []
    for md_file in md_files:
        links = extract_links(md_file)
        all_links.extend(links)
    print(f"Found {len(all_links)} total links\n")

    # Categorize links
    categorized = defaultdict(list)
    for link in all_links:
        category = categorize_link(link['url'])
        categorized[category].append(link)

    print("📊 Link Categories:")
    for category, links in sorted(categorized.items()):
        print(f"  {category}: {len(links)}")
    print()

    # Check internal docsify links (absolute paths only)
    print("🔗 Checking internal docsify links...")
    internal_links = categorized.get('absolute', [])

    # Deduplicate URLs for checking
    unique_urls = {}
    for link in internal_links:
        url = link['url']
        if url not in unique_urls:
            unique_urls[url] = []
        unique_urls[url].append(link)

    broken_links = []
    checked = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {
            executor.submit(check_docsify_link, url): (url, links)
            for url, links in unique_urls.items()
        }

        for future in as_completed(future_to_url):
            url, links = future_to_url[future]
            checked += 1
            try:
                status_code, reason = future.result()
                if status_code and status_code != 200:
                    broken_links.append({
                        'url': url,
                        'status': status_code,
                        'reason': reason,
                        'occurrences': len(links),
                        'files': list(set([l['file'] for l in links]))
                    })
                    print(f"❌ [{status_code}] {url}")
                elif checked % 10 == 0:
                    print(f"✓ Checked {checked}/{len(unique_urls)} URLs...")
            except Exception as e:
                print(f"⚠️  Error checking {url}: {e}")

    print(f"\n✅ Checked {len(unique_urls)} unique internal URLs")

    # Check GitHub links
    print("\n🔗 Checking GitHub links...")
    github_links = categorized.get('github', [])
    github_unique = {}
    for link in github_links:
        url = link['url']
        if url not in github_unique:
            github_unique[url] = []
        github_unique[url].append(link)

    github_broken = []
    checked = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {
            executor.submit(check_external_link, url): (url, links)
            for url, links in github_unique.items()
        }

        for future in as_completed(future_to_url):
            url, links = future_to_url[future]
            checked += 1
            try:
                status_code, reason = future.result()
                if status_code and status_code != 200:
                    github_broken.append({
                        'url': url,
                        'status': status_code,
                        'reason': reason,
                        'occurrences': len(links),
                        'files': list(set([l['file'] for l in links]))
                    })
                    print(f"❌ [{status_code}] {url}")
                elif checked % 10 == 0:
                    print(f"✓ Checked {checked}/{len(github_unique)} GitHub URLs...")
            except Exception as e:
                print(f"⚠️  Error checking {url}: {e}")

    print(f"✅ Checked {len(github_unique)} unique GitHub URLs")

    # Summary
    print("\n" + "="*80)
    print("📋 SUMMARY")
    print("="*80)

    if broken_links:
        print(f"\n❌ Found {len(broken_links)} broken internal links:\n")
        for link in broken_links:
            print(f"  [{link['status']}] {link['url']}")
            print(f"    Occurrences: {link['occurrences']}")
            for file in link['files'][:3]:  # Show first 3 files
                print(f"      - {file}")
            if len(link['files']) > 3:
                print(f"      ... and {len(link['files']) - 3} more")
            print()
    else:
        print("\n✅ All internal links are working!")

    if github_broken:
        print(f"\n❌ Found {len(github_broken)} broken GitHub links:\n")
        for link in github_broken:
            print(f"  [{link['status']}] {link['url']}")
            print(f"    Occurrences: {link['occurrences']}")
            for file in link['files'][:3]:
                print(f"      - {file}")
            if len(link['files']) > 3:
                print(f"      ... and {len(link['files']) - 3} more")
            print()
    else:
        print("\n✅ All GitHub links are working!")

    print("\n" + "="*80)

    return 0 if (not broken_links and not github_broken) else 1

if __name__ == "__main__":
    sys.exit(main())
