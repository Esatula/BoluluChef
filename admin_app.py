import streamlit as st
import json
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Bolulu Şef - Yönetim Paneli", page_icon="📝")

# Veri Yükleme Fonksiyonu
def load_recipes():
    with open('data/recipes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Veri Kaydetme Fonksiyonu
def save_recipes(recipes):
    with open('data/recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)

st.title("👨‍🍳 Tarif Yönetim Paneli")
st.markdown("Bu panelden mevcut tariflerin kategorilerini ve malzemelerini güncelleyebilirsiniz.")

# Tarifler Yükle
if os.path.exists('data/recipes.json'):
    recipes = load_recipes()
    recipe_names = [r['name'] for r in recipes]
    
    # Tarif Seçimi
    selected_name = st.selectbox("Düzenlemek istediğiniz tarifi seçin:", recipe_names)
    
    # Seçili Tarifi Bul
    recipe_idx = next(i for i, r in enumerate(recipes) if r['name'] == selected_name)
    recipe = recipes[recipe_idx]
    
    st.divider()
    
    # Düzenleme Formu
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Temel Bilgiler")
        new_name = st.text_input("Yemek Adı", recipe['name'])
        
        categories = ["Ana Yemekler", "Çorbalar", "Tatlılar", "Salatalar & Mezeler", "Hamur İşleri", "Genel"]
        
        # Eğer mevcut kategori listede yoksa ekle
        current_cat = recipe.get('category', 'Genel')
        if current_cat not in categories:
            categories.append(current_cat)
            
        new_category = st.selectbox("Kategori", categories, index=categories.index(current_cat))
        
        new_origin = st.radio("Köken", ["Turkish", "Global"], 
                              index=0 if recipe.get('origin') == 'Turkish' else 1)

    with col2:
        st.subheader("Malzemeler")
        # Malzemeleri alt alta string yap
        current_ingredients = "\n".join(recipe['ingredients'])
        new_ingredients_raw = st.text_area("Malzemeler (Her satıra bir malzeme)", current_ingredients, height=200)
        new_ingredients = [line.strip() for line in new_ingredients_raw.split("\n") if line.strip()]

    st.subheader("Hazırlanış Adımları")
    current_steps = "\n".join(recipe['steps'])
    new_steps_raw = st.text_area("Adımlar (Her satıra bir adım)", current_steps, height=150)
    new_steps = [line.strip() for line in new_steps_raw.split("\n") if line.strip()]

    st.divider()
    
    if st.button("✅ Değişiklikleri Kaydet", use_container_state=True):
        # Güncelleme
        recipes[recipe_idx]['name'] = new_name
        recipes[recipe_idx]['category'] = new_category
        recipes[recipe_idx]['ingredients'] = new_ingredients
        recipes[recipe_idx]['steps'] = new_steps
        recipes[recipe_idx]['origin'] = new_origin
        
        save_recipes(recipes)
        st.success(f"'{new_name}' başarıyla güncellendi!")
        st.balloons()

else:
    st.error("Veri dosyası (recipes.json) bulunamadı!")

# Sidebar Bilgi
with st.sidebar:
    st.info(f"Sistemde toplam **{len(recipes) if 'recipes' in locals() else 0}** tarif kayıtlı.")
    st.warning("Dikkat: Kaydedilen değişiklikler Chatbot'un cevaplarını doğrudan etkileyecektir.")
