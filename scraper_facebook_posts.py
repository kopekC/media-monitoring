"""
Facebook Posts Scraper - Extract posts from feminist organizations that match keywords
Extracts: post_id, page_name, texto, likes, comments, shares, fecha, url, keyword_matched
"""

import os
import time
from datetime import datetime
from dotenv import load_dotenv
from apify_client import ApifyClient
import pandas as pd
from facebook_pages import FACEBOOK_PAGES
from keywords import KEYWORDS

# Load environment variables
load_dotenv()

# Initialize Apify client
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN')
if not APIFY_TOKEN:
    raise ValueError("APIFY_API_TOKEN not found in environment variables. Please create a .env file.")

client = ApifyClient(APIFY_TOKEN)

# Configuration
MAX_POSTS_PER_PAGE = int(os.getenv('MAX_POSTS_PER_PAGE', 100))
START_DATE = "2025-01-01"

def scrape_facebook_posts(pages_dict, keywords_dict, output_file='facebook_posts_data.csv'):
    """
    Scrape Facebook Posts from specific pages and filter by keywords
    Output: post_id, page_name, organization_name, texto, likes, comments, shares, 
            fecha, url, keywords_matched
    """
    print(f"\n{'='*60}")
    print("Iniciando scraping de Posts de Facebook...")
    print(f"{'='*60}\n")
    
    all_results = []
    
    # Convert dict to list of URLs for processing
    page_urls = list(pages_dict.values())
    page_names = list(pages_dict.keys())
    
    # Prepare keywords for matching (remove # and lowercase)
    keywords_clean = {k: v.replace('#', '').lower() for k, v in keywords_dict.items()}
    
    print(f"Total de páginas a procesar: {len(page_urls)}")
    print(f"Keywords a buscar: {len(keywords_clean)}")
    print(f"Posts máximos por página: {MAX_POSTS_PER_PAGE}")
    print(f"Filtro de fecha: {START_DATE} en adelante\n")
    
    # Process pages in smaller batches to avoid timeouts
    batch_size = 5
    
    for i in range(0, len(page_urls), batch_size):
        batch_urls = page_urls[i:i+batch_size]
        batch_names = page_names[i:i+batch_size]
        
        print(f"{'='*60}")
        print(f"Procesando lote {i//batch_size + 1} ({len(batch_urls)} páginas)...")
        print(f"{'='*60}")
        
        for idx, (url, org_name) in enumerate(zip(batch_urls, batch_names)):
            print(f"\n[{idx+1}/{len(batch_urls)}] Procesando: {org_name}")
            print(f"  URL: {url}")
            
            try:
                # Configure the Actor input for Facebook Posts scraper
                # Using https://apify.com/apify/facebook-posts-scraper
                run_input = {
                    "startUrls": [{"url": url}],
                    "maxPosts": MAX_POSTS_PER_PAGE,
                    "resultsLimit": MAX_POSTS_PER_PAGE,
                }
                
                # Run the Actor and wait for it to finish
                print(f"  → Ejecutando Apify actor...")
                run = client.actor("apify/facebook-posts-scraper").call(run_input=run_input)
                
                # Fetch results from the dataset
                dataset_items = []
                for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                    dataset_items.append(item)
                
                print(f"  → {len(dataset_items)} posts extraídos")
                
                # Process and filter results by keywords
                posts_matched = 0
                
                for item in dataset_items:
                    try:
                        # Get post text
                        post_text = item.get('text', '') or item.get('postText', '') or ''
                        
                        if not post_text:
                            continue
                        
                        # Parse date
                        post_date = None
                        date_str = item.get('time', '') or item.get('date', '')
                        
                        if date_str:
                            try:
                                # Try different date formats
                                for fmt in ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                                    try:
                                        post_date = datetime.strptime(date_str.split('.')[0].replace('T', ' ').replace('Z', '').strip(), fmt.replace('.%f', ''))
                                        break
                                    except:
                                        continue
                                
                                # Filter by date (2025 onwards)
                                if post_date and post_date.year < 2025:
                                    continue
                                    
                            except Exception as e:
                                pass
                        
                        # Check if post contains any keywords
                        post_text_lower = post_text.lower()
                        matched_keywords = []
                        
                        for keyword_key, keyword_clean in keywords_clean.items():
                            if keyword_clean in post_text_lower:
                                matched_keywords.append(keyword_key)
                        
                        # Only save if at least one keyword matched
                        if matched_keywords:
                            result = {
                                'post_id': item.get('postId', '') or item.get('id', ''),
                                'organization_name': org_name,
                                'page_name': item.get('pageName', '') or org_name,
                                'texto': post_text,
                                'likes': item.get('likes', 0) or item.get('likeCount', 0),
                                'comments': item.get('comments', 0) or item.get('commentCount', 0),
                                'shares': item.get('shares', 0) or item.get('shareCount', 0),
                                'fecha': post_date.strftime('%Y-%m-%d %H:%M:%S') if post_date else date_str,
                                'url': item.get('url', '') or item.get('postUrl', ''),
                                'keywords_matched': ', '.join(matched_keywords),
                                'num_keywords': len(matched_keywords),
                            }
                            all_results.append(result)
                            posts_matched += 1
                        
                    except Exception as e:
                        print(f"  ⚠ Error procesando post: {e}")
                        continue
                
                print(f"  ✓ Posts que coinciden con keywords: {posts_matched}")
                
                # Small delay between pages
                time.sleep(2)
            
            except Exception as e:
                print(f"  ✗ Error procesando página: {e}")
                continue
        
        # Longer delay between batches
        if i + batch_size < len(page_urls):
            print(f"\n{'='*60}")
            print(f"Esperando antes del siguiente lote...")
            print(f"{'='*60}\n")
            time.sleep(5)
    
    # Save to CSV
    if all_results:
        df = pd.DataFrame(all_results)
        # Sort by number of keywords matched (descending) and date
        df = df.sort_values(['num_keywords', 'fecha'], ascending=[False, False])
        df = df.drop('num_keywords', axis=1)  # Remove helper column
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\n{'='*60}")
        print("RESUMEN DE DATOS EXTRAÍDOS")
        print(f"{'='*60}")
        print(f"✓ Datos guardados en: {output_file}")
        print(f"Total de posts con keywords: {len(all_results)}")
        print(f"\nTop 5 organizaciones con más posts:")
        top_orgs = df['organization_name'].value_counts().head()
        for org, count in top_orgs.items():
            print(f"  - {org}: {count} posts")
        
        print(f"\nTop 10 keywords más mencionados:")
        # Count keyword occurrences
        keyword_counts = {}
        for keywords_str in df['keywords_matched']:
            for kw in keywords_str.split(', '):
                keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        
        for kw, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  - #{kw}: {count} menciones")
        
        print(f"\nEstadísticas de engagement:")
        print(f"  Total de likes: {df['likes'].sum():,}")
        print(f"  Total de comentarios: {df['comments'].sum():,}")
        print(f"  Total de shares: {df['shares'].sum():,}")
        print(f"  Promedio de likes por post: {df['likes'].mean():.1f}")
        print(f"{'='*60}\n")
    else:
        print("\n⚠ No se encontraron posts que coincidan con los keywords")
    
    return all_results


def main():
    """
    Main function to run Facebook Posts scraper
    """
    print("\n" + "="*60)
    print("FACEBOOK POSTS SCRAPER CON FILTRO DE KEYWORDS")
    print("="*60)
    print(f"Páginas de Facebook: {len(FACEBOOK_PAGES)}")
    print(f"Keywords a buscar: {len(KEYWORDS)}")
    print(f"Posts máximos por página: {MAX_POSTS_PER_PAGE}")
    print("="*60 + "\n")
    
    # Create output directory
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    start_time = time.time()
    
    # Scrape Facebook Posts
    facebook_posts_results = scrape_facebook_posts(
        FACEBOOK_PAGES,
        KEYWORDS,
        output_file=f'{output_dir}/facebook_posts_data.csv'
    )
    
    # Summary
    elapsed_time = time.time() - start_time
    print(f"\n{'='*60}")
    print("SCRAPING DE POSTS DE FACEBOOK COMPLETO")
    print(f"{'='*60}")
    print(f"Posts con keywords encontrados: {len(facebook_posts_results)}")
    print(f"Tiempo transcurrido: {elapsed_time/60:.2f} minutos")
    print(f"{'='*60}\n")
    print(f"📁 Archivo de salida:\n  - {output_dir}/facebook_posts_data.csv\n")


if __name__ == "__main__":
    main()

