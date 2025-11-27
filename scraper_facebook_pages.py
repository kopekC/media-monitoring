"""
Facebook Pages Scraper - Independent scraper for Facebook page information
Extracts: page info, likes, followers, contact details, and more
"""

import os
import time
from dotenv import load_dotenv
from apify_client import ApifyClient
import pandas as pd
from facebook_pages import FACEBOOK_PAGES

# Load environment variables
load_dotenv()

# Initialize Apify client
APIFY_TOKEN = os.getenv('APIFY_API_TOKEN')
if not APIFY_TOKEN:
    raise ValueError("APIFY_API_TOKEN not found in environment variables. Please create a .env file.")

client = ApifyClient(APIFY_TOKEN)

def scrape_facebook_pages(pages_dict, output_file='facebook_pages_data.csv'):
    """
    Scrape Facebook Pages information
    Output: page_name, page_url, categoria, likes, followers, intro, website, email, 
            telefono, direccion, rating, rating_count, messenger, page_creation_date, 
            ad_status, ad_library_id, profile_picture_url, cover_photo_url
    """
    print(f"\n{'='*60}")
    print("Iniciando scraping de Páginas de Facebook...")
    print(f"{'='*60}\n")
    
    all_results = []
    
    # Convert dict to list of URLs for processing
    page_urls = list(pages_dict.values())
    page_names = list(pages_dict.keys())
    
    print(f"Total de páginas a procesar: {len(page_urls)}\n")
    
    # Process pages in batches to avoid API limits
    batch_size = 10
    
    for i in range(0, len(page_urls), batch_size):
        batch_urls = page_urls[i:i+batch_size]
        batch_names = page_names[i:i+batch_size]
        
        print(f"Procesando lote {i//batch_size + 1} ({len(batch_urls)} páginas)...")
        
        try:
            # Configure the Actor input for Facebook Pages scraper
            # Using correct parameters from https://apify.com/apify/facebook-pages-scraper
            run_input = {
                "startUrls": [{"url": url} for url in batch_urls],
                "maxPagesPerQuery": len(batch_urls),
            }
            
            # Run the Actor and wait for it to finish
            print(f"  → Ejecutando Apify actor...")
            run = client.actor("apify/facebook-pages-scraper").call(run_input=run_input)
            
            # Fetch results from the dataset
            dataset_items = []
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                dataset_items.append(item)
            
            print(f"  → Datos de {len(dataset_items)} páginas extraídos")
            
            # Process results
            for idx, item in enumerate(dataset_items):
                try:
                    # Extract page name from our original list
                    original_name = ""
                    for name, url in pages_dict.items():
                        if url in item.get('pageUrl', '') or url in item.get('facebookUrl', ''):
                            original_name = name
                            break
                    
                    # Extract websites (can be multiple)
                    websites = item.get('websites', [])
                    website = websites[0] if websites else item.get('website', '')
                    
                    # Extract categories
                    categories = item.get('categories', [])
                    categoria = ', '.join(categories) if categories else ''
                    
                    result = {
                        'nombre_organizacion': original_name,
                        'page_name': item.get('title', '') or item.get('pageName', ''),
                        'page_url': item.get('pageUrl', '') or item.get('facebookUrl', ''),
                        'page_id': item.get('pageId', ''),
                        'categoria': categoria,
                        'likes': item.get('likes', 0),
                        'followers': item.get('followers', 0),
                        'intro': item.get('intro', ''),
                        'website': website,
                        'email': item.get('email', ''),
                        'telefono': item.get('phone', '') or item.get('phoneNumber', ''),
                        'direccion': item.get('address', ''),
                        'rating': item.get('rating', ''),
                        'rating_count': item.get('ratingCount', 0),
                        'messenger': item.get('messenger', ''),
                        'checkins': item.get('checkins', 0),
                        'ad_library_id': item.get('adLibraryPageId', ''),
                        'ad_status': 'Sí' if item.get('adsAreRunning') else 'No',
                        'profile_picture_url': item.get('profilePictureUrl', ''),
                        'cover_photo_url': item.get('coverPhotoUrl', ''),
                    }
                    all_results.append(result)
                    
                except Exception as e:
                    print(f"  ⚠ Error procesando página: {e}")
                    continue
            
            # Respect rate limits between batches
            if i + batch_size < len(page_urls):
                print(f"  → Esperando antes del siguiente lote...")
                time.sleep(5)
        
        except Exception as e:
            print(f"  ✗ Error procesando lote: {e}")
            continue
    
    # Save to CSV
    if all_results:
        df = pd.DataFrame(all_results)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✓ Datos de páginas de Facebook guardados en {output_file}")
        print(f"  Total de páginas procesadas: {len(all_results)}")
        
        # Print summary statistics
        print(f"\n{'='*60}")
        print("RESUMEN DE DATOS EXTRAÍDOS")
        print(f"{'='*60}")
        print(f"Total de páginas: {len(all_results)}")
        print(f"Páginas con email: {df['email'].notna().sum()}")
        print(f"Páginas con teléfono: {df['telefono'].notna().sum()}")
        print(f"Páginas con website: {df['website'].notna().sum()}")
        print(f"Páginas corriendo anuncios: {df[df['ad_status'] == 'Sí'].shape[0]}")
        print(f"Total de likes: {df['likes'].sum():,}")
        print(f"Total de followers: {df['followers'].sum():,}")
        print(f"{'='*60}\n")
    else:
        print("\n⚠ No se recolectaron datos de páginas de Facebook")
    
    return all_results


def main():
    """
    Main function to run Facebook Pages scraper
    """
    print("\n" + "="*60)
    print("FACEBOOK PAGES SCRAPER")
    print("="*60)
    print(f"Páginas de Facebook a extraer: {len(FACEBOOK_PAGES)}")
    print("="*60 + "\n")
    
    # Create output directory
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    start_time = time.time()
    
    # Scrape Facebook Pages
    facebook_pages_results = scrape_facebook_pages(
        FACEBOOK_PAGES,
        output_file=f'{output_dir}/facebook_pages_data.csv'
    )
    
    # Summary
    elapsed_time = time.time() - start_time
    print(f"\n{'='*60}")
    print("SCRAPING DE PÁGINAS DE FACEBOOK COMPLETO")
    print(f"{'='*60}")
    print(f"Páginas procesadas: {len(facebook_pages_results)}")
    print(f"Tiempo transcurrido: {elapsed_time/60:.2f} minutos")
    print(f"{'='*60}\n")
    print(f"📁 Archivo de salida:\n  - {output_dir}/facebook_pages_data.csv\n")


if __name__ == "__main__":
    main()

