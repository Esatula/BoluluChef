import requests
from bs4 import BeautifulSoup
import json
import time
import os

def scrape_recipe(url):
    print(f"Scraping: {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: Status {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # JSON-LD verisini bul (En güvenli yöntem)
        json_ld_tags = soup.find_all('script', type='application/ld+json')
        recipe_data = None
        
        for tag in json_ld_tags:
            try:
                data = json.loads(tag.string)
                # Bazı sitelerde liste içinde geliyor, bazıları direkt dict
                if isinstance(data, list):
                    for item in data:
                        if item.get('@type') == 'Recipe':
                            recipe_data = item
                            break
                elif data.get('@type') == 'Recipe':
                    recipe_data = data
                
                if recipe_data: break
            except:
                continue

        if not recipe_data:
            print(f"Recipe data not found in JSON-LD for {url}")
            return None

        # Başlık
        title = recipe_data.get('name', 'Adsız Tarif')
        
        # Malzemeler (Nested list olabiliyor, düzleştiriyoruz)
        ingredients = []
        raw_ingredients = recipe_data.get('recipeIngredient', [])
        for item in raw_ingredients:
            if isinstance(item, list):
                ingredients.extend(item)
            else:
                ingredients.append(item)
            
        # Hazırlanış (Nested list olabiliyor, düzleştiriyoruz)
        steps = []
        raw_instructions = recipe_data.get('recipeInstructions', [])
        for item in raw_instructions:
            if isinstance(item, list):
                steps.extend(item)
            elif isinstance(item, dict):
                steps.append(item.get('text', ''))
            else:
                steps.append(str(item))
            
        # Kategori
        category = recipe_data.get('recipeCategory', 'Genel')
        if isinstance(category, list): category = category[0]
        
        # Origin Tespiti
        global_keywords = ["pizza", "lasagna", "pasta", "hamburger", "sushi", "taco", "risotto", "tiramisu", "ratatouille", "panna cotta", "spagetti"]
        is_global = any(kw in url.lower() or kw in title.lower() for kw in global_keywords)
        
        return {
            "name": title,
            "ingredients": ingredients,
            "steps": steps,
            "category": category,
            "origin": "Global" if is_global else "Turkish"
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    source_file = 'sources.txt'
    if not os.path.exists(source_file):
        print(f"Hata: {source_file} bulunamadı.")
        return
        
    with open(source_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"{len(urls)} adet link işleniyor...")
    new_recipes = []
    for url in urls:
        recipe = scrape_recipe(url)
        if recipe:
            new_recipes.append(recipe)
        time.sleep(1)
    
    # Mevcut verileri yükle
    data_path = 'data/recipes.json'
    existing_recipes = []
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            existing_recipes = json.load(f)
            
    # Mevcut isimleri kontrol et
    # Yeni eşleşenleri güncelle, olmayanları ekle
    for nr in new_recipes:
        found = False
        for er in existing_recipes:
            if er['name'] == nr['name']:
                er['ingredients'] = nr['ingredients']
                er['steps'] = nr['steps']
                er['category'] = nr['category']
                er['origin'] = nr['origin']
                found = True
                break
        if not found:
            max_id = max([r.get('id', 0) for r in existing_recipes]) if existing_recipes else 0
            nr['id'] = max_id + 1
            existing_recipes.append(nr)
            
    # Sırala: Turkish önce
    sorted_recipes = sorted(existing_recipes, key=lambda x: 0 if x.get('origin') == 'Turkish' else 1)
    
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_recipes, f, ensure_ascii=False, indent=2)
        
    print(f"İşlem tamam. Toplam {len(existing_recipes)} tarif güncellendi/eklendi.")

if __name__ == "__main__":
    main()
