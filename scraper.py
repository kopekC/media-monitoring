"""
Main scraper script for TikTok, Instagram, and Facebook using Apify
"""

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from apify_client import ApifyClient
import pandas as pd
from keywords import KEYWORDS

# Load environment variables
load_dotenv()

# Initialize Apify client
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN')
if not APIFY_TOKEN:
    raise ValueError("APIFY_API_TOKEN not found in environment variables. Please create a .env file.")

client = ApifyClient(APIFY_TOKEN)

# Configuration
MAX_RESULTS_PER_KEYWORD = int(os.getenv('MAX_RESULTS_PER_KEYWORD', 100))
RESULTS_LIMIT = int(os.getenv('RESULTS_LIMIT', 1000))

# Date filter for 2025 onwards
START_DATE = "2025-01-01"


def scrape_instagram(hashtags, output_file='instagram_data.csv'):
    """
    Scrape Instagram posts using hashtags
    Output: post_id, usuario, caption, hashtags, likes, comments, fecha, url
    """
    print(f"\n{'='*60}")
    print("Starting Instagram scraping...")
    print(f"{'='*60}\n")
    
    all_results = []
    
    for keyword, hashtag in list(hashtags.items())[:10]:  # Start with first 10 keywords
        print(f"Scraping Instagram for: {hashtag}")
        
        try:
            # Configure the Actor input
            run_input = {
                "directUrls": [f"https://www.instagram.com/explore/tags/{hashtag.replace('#', '')}/"],
                "resultsType": "posts",
                "resultsLimit": MAX_RESULTS_PER_KEYWORD,
            }
            
            # Run the Actor and wait for it to finish
            print(f"  → Running Apify actor...")
            run = client.actor("apify/instagram-scraper").call(run_input=run_input)
            
            # Fetch results from the dataset
            dataset_items = []
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                dataset_items.append(item)
            
            print(f"  → Found {len(dataset_items)} posts")
            
            # Process results
            for item in dataset_items:
                try:
                    # Parse timestamp
                    post_date = None
                    if 'timestamp' in item and item['timestamp']:
                        post_date = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
                        # Filter by date (2025 onwards)
                        if post_date.year < 2025:
                            continue
                    
                    result = {
                        'post_id': item.get('id', ''),
                        'usuario': item.get('ownerUsername', ''),
                        'caption': item.get('caption', ''),
                        'hashtags': ', '.join(item.get('hashtags', [])) if isinstance(item.get('hashtags'), list) else '',
                        'likes': item.get('likesCount', 0),
                        'comments': item.get('commentsCount', 0),
                        'fecha': post_date.strftime('%Y-%m-%d %H:%M:%S') if post_date else '',
                        'url': item.get('url', ''),
                        'keyword': keyword
                    }
                    all_results.append(result)
                except Exception as e:
                    print(f"  ⚠ Error processing item: {e}")
                    continue
            
            # Respect rate limits
            time.sleep(2)
            
        except Exception as e:
            print(f"  ✗ Error scraping {hashtag}: {e}")
            continue
    
    # Save to CSV
    if all_results:
        df = pd.DataFrame(all_results)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✓ Instagram data saved to {output_file}")
        print(f"  Total posts collected: {len(all_results)}")
    else:
        print("\n⚠ No Instagram data collected")
    
    return all_results


def scrape_tiktok(hashtags, output_file='tiktok_data.csv'):
    """
    Scrape TikTok videos using hashtags
    Output: video_id, usuario, caption, hashtags, views, likes, fecha, url
    """
    print(f"\n{'='*60}")
    print("Starting TikTok scraping...")
    print(f"{'='*60}\n")
    
    all_results = []
    
    for keyword, hashtag in list(hashtags.items())[:10]:  # Start with first 10 keywords
        print(f"Scraping TikTok for: {hashtag}")
        
        try:
            # Configure the Actor input
            run_input = {
                "hashtags": [hashtag.replace('#', '')],
                "resultsPerPage": MAX_RESULTS_PER_KEYWORD,
                "shouldDownloadVideos": False,
                "shouldDownloadCovers": False,
                "shouldDownloadSubtitles": False,
            }
            
            # Run the Actor and wait for it to finish
            print(f"  → Running Apify actor...")
            run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
            
            # Fetch results from the dataset
            dataset_items = []
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                dataset_items.append(item)
            
            print(f"  → Found {len(dataset_items)} videos")
            
            # Process results
            for item in dataset_items:
                try:
                    # Parse timestamp
                    post_date = None
                    if 'createTime' in item and item['createTime']:
                        post_date = datetime.fromtimestamp(item['createTime'])
                        # Filter by date (2025 onwards)
                        if post_date.year < 2025:
                            continue
                    elif 'createTimeISO' in item and item['createTimeISO']:
                        post_date = datetime.fromisoformat(item['createTimeISO'].replace('Z', '+00:00'))
                        if post_date.year < 2025:
                            continue
                    
                    result = {
                        'video_id': item.get('id', ''),
                        'usuario': item.get('authorMeta', {}).get('name', '') if isinstance(item.get('authorMeta'), dict) else '',
                        'caption': item.get('text', ''),
                        'hashtags': ', '.join([tag.get('name', '') for tag in item.get('hashtags', [])]) if isinstance(item.get('hashtags'), list) else '',
                        'views': item.get('playCount', 0),
                        'likes': item.get('diggCount', 0),
                        'fecha': post_date.strftime('%Y-%m-%d %H:%M:%S') if post_date else '',
                        'url': item.get('webVideoUrl', ''),
                        'keyword': keyword
                    }
                    all_results.append(result)
                except Exception as e:
                    print(f"  ⚠ Error processing item: {e}")
                    continue
            
            # Respect rate limits
            time.sleep(2)
            
        except Exception as e:
            print(f"  ✗ Error scraping {hashtag}: {e}")
            continue
    
    # Save to CSV
    if all_results:
        df = pd.DataFrame(all_results)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✓ TikTok data saved to {output_file}")
        print(f"  Total videos collected: {len(all_results)}")
    else:
        print("\n⚠ No TikTok data collected")
    
    return all_results


def scrape_twitter(keywords, output_file='twitter_data.csv'):
    """
    Scrape Twitter/X posts using keyword search
    Output: tweet_id, usuario, texto, hashtags, likes, retweets, replies, views, fecha, url, keyword
    """
    print(f"\n{'='*60}")
    print("Starting Twitter/X scraping...")
    print(f"{'='*60}\n")
    
    all_results = []
    
    for keyword, hashtag in list(keywords.items())[:10]:  # Start with first 10 keywords
        print(f"Scraping Twitter for: {hashtag}")
        
        try:
            # Configure the Actor input for Twitter scraper
            # Using correct parameters from https://apify.com/apidojo/tweet-scraper
            run_input = {
                "searchTerms": [hashtag],
                "maxItems": max(50, MAX_RESULTS_PER_KEYWORD),  # API requires minimum 50 tweets per query
                "addUserInfo": True,
                "sort": "Latest",
            }
            
            # Run the Actor and wait for it to finish
            print(f"  → Running Apify actor...")
            run = client.actor("apidojo/tweet-scraper").call(run_input=run_input)
            
            # Fetch results from the dataset
            dataset_items = []
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                dataset_items.append(item)
            
            print(f"  → Found {len(dataset_items)} tweets")
            
            # Process results
            for item in dataset_items:
                try:
                    # Parse timestamp
                    post_date = None
                    if 'created_at' in item and item['created_at']:
                        # Twitter timestamp format: "Wed Nov 18 17:00:00 +0000 2025"
                        from datetime import datetime
                        post_date = datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S %z %Y')
                        # Filter by date (2025 onwards)
                        if post_date.year < 2025:
                            continue
                    
                    # Extract hashtags
                    tweet_hashtags = []
                    if 'entities' in item and 'hashtags' in item['entities']:
                        tweet_hashtags = [tag['text'] for tag in item['entities']['hashtags']]
                    
                    result = {
                        'tweet_id': item.get('id_str', ''),
                        'usuario': item.get('user', {}).get('screen_name', '') if isinstance(item.get('user'), dict) else '',
                        'texto': item.get('full_text', '') or item.get('text', ''),
                        'hashtags': ', '.join(tweet_hashtags),
                        'likes': item.get('favorite_count', 0),
                        'retweets': item.get('retweet_count', 0),
                        'replies': item.get('reply_count', 0),
                        'views': item.get('view_count', 0),
                        'fecha': post_date.strftime('%Y-%m-%d %H:%M:%S') if post_date else '',
                        'url': f"https://twitter.com/{item.get('user', {}).get('screen_name', 'i')}/status/{item.get('id_str', '')}" if isinstance(item.get('user'), dict) else '',
                        'keyword': keyword
                    }
                    all_results.append(result)
                except Exception as e:
                    print(f"  ⚠ Error processing item: {e}")
                    continue
            
            # Respect rate limits
            time.sleep(2)
            
        except Exception as e:
            print(f"  ✗ Error scraping {hashtag}: {e}")
            continue
    
    # Save to CSV
    if all_results:
        df = pd.DataFrame(all_results)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✓ Twitter data saved to {output_file}")
        print(f"  Total tweets collected: {len(all_results)}")
    else:
        print("\n⚠ No Twitter data collected")
    
    return all_results


def main():
    """
    Main function to run all scrapers
    """
    print("\n" + "="*60)
    print("SOCIAL MEDIA SCRAPER")
    print("="*60)
    print(f"Keywords to search: {len(KEYWORDS)}")
    print(f"Max results per keyword: {MAX_RESULTS_PER_KEYWORD}")
    print(f"Date filter: {START_DATE} onwards")
    print("="*60 + "\n")
    
    # Create output directory
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Run scrapers
    start_time = time.time()
    
    # Scrape Instagram
    instagram_results = scrape_instagram(
        KEYWORDS, 
        output_file=f'{output_dir}/instagram_data.csv'
    )
    
    # Scrape TikTok
    tiktok_results = scrape_tiktok(
        KEYWORDS, 
        output_file=f'{output_dir}/tiktok_data.csv'
    )
    
    # Scrape Twitter
    twitter_results = scrape_twitter(
        KEYWORDS, 
        output_file=f'{output_dir}/twitter_data.csv'
    )
    
    # Summary
    elapsed_time = time.time() - start_time
    print(f"\n{'='*60}")
    print("SCRAPING COMPLETE")
    print(f"{'='*60}")
    print(f"Instagram posts: {len(instagram_results)}")
    print(f"TikTok videos: {len(tiktok_results)}")
    print(f"Twitter tweets: {len(twitter_results)}")
    print(f"Total items: {len(instagram_results) + len(tiktok_results) + len(twitter_results)}")
    print(f"Time elapsed: {elapsed_time/60:.2f} minutes")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

