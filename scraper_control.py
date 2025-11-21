"""
Scraper script for CONTROL GROUP keywords
"""

import os
import time
from dotenv import load_dotenv
from scraper import scrape_instagram, scrape_tiktok, scrape_twitter
from keywords import KEYWORDS_CONTROL

# Load environment variables
load_dotenv()

# Configuration
MAX_RESULTS_PER_KEYWORD = int(os.getenv('MAX_RESULTS_PER_KEYWORD', 100))

print("\n" + "="*60)
print("SOCIAL MEDIA SCRAPER - CONTROL GROUP")
print("="*60)
print(f"Keywords to search: {len(KEYWORDS_CONTROL)}")
print(f"Max results per keyword: {MAX_RESULTS_PER_KEYWORD}")
print(f"Date filter: 2025-01-01 onwards")
print("="*60 + "\n")

# Create output directory
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Run scrapers
start_time = time.time()

# Scrape Instagram
instagram_results = scrape_instagram(
    KEYWORDS_CONTROL, 
    output_file=f'{output_dir}/instagram_data_control.csv'
)

# Scrape TikTok
tiktok_results = scrape_tiktok(
    KEYWORDS_CONTROL, 
    output_file=f'{output_dir}/tiktok_data_control.csv'
)

# Scrape Twitter
twitter_results = scrape_twitter(
    KEYWORDS_CONTROL, 
    output_file=f'{output_dir}/twitter_data_control.csv'
)

# Summary
elapsed_time = time.time() - start_time
print(f"\n{'='*60}")
print("CONTROL GROUP SCRAPING COMPLETE")
print(f"{'='*60}")
print(f"Instagram posts: {len(instagram_results)}")
print(f"TikTok videos: {len(tiktok_results)}")
print(f"Twitter tweets: {len(twitter_results)}")
print(f"Total items: {len(instagram_results) + len(tiktok_results) + len(twitter_results)}")
print(f"Time elapsed: {elapsed_time/60:.2f} minutes")
print(f"{'='*60}\n")

print("📁 Output files:")
print(f"  - {output_dir}/instagram_data_control.csv")
print(f"  - {output_dir}/tiktok_data_control.csv")
print(f"  - {output_dir}/twitter_data_control.csv")

