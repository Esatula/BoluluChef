import json
import random
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def load_intents(file_path):
    intents = {}
    current_intent = None

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("[INTENT:"):
                current_intent = line.replace("[INTENT:", "").replace("]", "")
                intents[current_intent] = []
            else:
                intents[current_intent].append(line)

    return intents

class BoluluSefBot:
    def __init__(self, recipes_path='data/recipes.json', intents_path='data/intents.txt'):
        self.load_recipes(recipes_path)
        self.intents = load_intents(intents_path)
        
        # SBERT Model loading
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.prepare_embeddings()
        
        # Recipe search (using simple keyword match or vector search)
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vectorizer = TfidfVectorizer()
        self.recipe_names = [r['name'] for r in self.recipes]
        self.recipe_vectors = self.vectorizer.fit_transform(self.recipe_names)

        # Responses for smalltalk
        self.smalltalk_responses = {
            "greeting": [
                "Hoş geldin evlat! Ne pişiriyoruz bugün?",
                "Selam! Aç mısın yoksa muhabbet mi edelim 😄",
                "Selamlar! Bolu'nun ocağından taze geldim, buyur ne istersin?"
            ],
            "how_are_you": [
                "Ben iyiyim, tencereler kaynıyor 😎",
                "Şef her zaman formda 💪 sen nasılsın?",
                "Mutfak sıcak, keyifler gıcır! Sen nasılsın bakalım?"
            ],
            "thanks": [
                "Afiyet bal şeker olsun!",
                "Rica ederim evlat, elinin lezzeti bol olsun.",
                "Eyvallah, her zaman beklerim mutfağa!"
            ],
            "goodbye": [
                "Görüşürüz evlat, ocağı açık unutma!",
                "Bye bye! Bir dahaki sefere daha aç gel.",
                "Kendine iyi bak, mutfağı özletme!"
            ],
            "addressing": [
                "Buyur evlat, şefin burada!",
                "Efendim canım, ne lazım mutfaktan?",
                "Söyle bakalım şefine, neyimiz eksik?"
            ]
        }

    def load_recipes(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            self.recipes = json.load(f)

    def prepare_embeddings(self):
        self.intent_embeddings = {}
        for intent, examples in self.intents.items():
            self.intent_embeddings[intent] = self.model.encode(examples)

    def predict_intents(self, text, threshold=0.5):
        text_emb = self.model.encode([text])
        detected_intents = []

        for intent, emb in self.intent_embeddings.items():
            # Get the max similarity between user text and all examples for this intent
            sims = cosine_similarity(text_emb, emb).flatten()
            max_sim = sims.max()
            if max_sim > threshold:
                detected_intents.append((intent, max_sim))
        
        # Sort by similarity
        detected_intents.sort(key=lambda x: x[1], reverse=True)
        return detected_intents

    def predict_intent(self, text):
        intents = self.predict_intents(text)
        if intents:
            return intents[0][0]
        return "unknown"

    def extract_ingredients(self, text):
        all_ingredients = set()
        for r in self.recipes:
            for ing in r['ingredients']:
                all_ingredients.add(ing.lower())
        
        found = []
        for ing in all_ingredients:
            if ing in text.lower():
                found.append(ing)
        return list(set(found))

    def find_recipe_by_name(self, text):
        query_vec = self.vectorizer.transform([text])
        similarities = cosine_similarity(query_vec, self.recipe_vectors).flatten()
        best_match_idx = np.argmax(similarities)
        if similarities[best_match_idx] > 0.3:
            return self.recipes[best_match_idx]
        return None

    def recommend_by_ingredients(self, user_ingredients):
        if not user_ingredients:
            return None
        
        scores = []
        for recipe in self.recipes:
            # Simple intersection over total ingredients
            match_count = len(set(user_ingredients) & set(recipe['ingredients']))
            scores.append(match_count / len(recipe['ingredients']))
            
        best_idx = np.argmax(scores)
        if scores[best_idx] > 0:
            return self.recipes[best_idx]
        return None

    def get_chef_response(self, text):
        detected = self.predict_intents(text)
        
        if not detected:
            return "Anlayamadım evlat, mutfakta gürültü mü var? Daha açık söyle ne istediğini."

        intents = [d[0] for d in detected]
        
        # Multi-intent logic: If there's greeting/thanks etc, combine them.
        # But if it's a recipe request or similar, prioritize that.
        
        response_parts = []
        
        # Handle smalltalk first
        handled_smalltalk = False
        for intent in ["greeting", "how_are_you", "addressing", "thanks", "goodbye"]:
            if intent in intents:
                response_parts.append(random.choice(self.smalltalk_responses[intent]))
                handled_smalltalk = True
                # If we have greeting, we don't necessarily want to dump ALL smalltalk responses
                # but "selam nasılsın" should get both.
                # However, addressing "şef" shouldn't always trigger if there's other stuff.
                if intent == "addressing" and len(intents) > 1:
                    response_parts.pop() # Remove "Buyur evlat" if we have more specific stuff
        
        # Handle primary actions
        if "recipe_request" in intents:
            recipe = self.find_recipe_by_name(text)
            if recipe:
                steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(recipe['steps'])])
                response_parts.append(f"Bak hele! **{recipe['name']}** dediğin öyle her yiğidin harcı değildir. Bolu usulü şöyle yapılır:\n\n{steps}\n\nAfiyet olsun!")
            else:
                response_parts.append("Vallahi o tarifi henüz bizim Bolulu ustalardan duymadım, ama menemen falan sorsan hemen döktürürdüm.")
        
        elif "ingredient_based" in intents:
            extracted = self.extract_ingredients(text)
            recipe = self.recommend_by_ingredients(extracted)
            if recipe:
                response_parts.append(f"Hımm, bakıyorum elinde **{', '.join(extracted)}** varmış. Bunlarla sana mis gibi bir **{recipe['name']}** patlatalım mı? Şeflik belgesi ister bu iş ama sana güveniyorum! 😉")
            else:
                response_parts.append("Mutfaktaki o malzemelerle ancak çay demlenir gibi duruyor evlat. Biraz daha malzeme getir de şenlenelim!")

        elif "category_request" in intents:
            cat_keywords = {
                "çorba": "Çorbalar", "tatlı": "Tatlılar", "meze": "Salatalar & Mezeler",
                "salata": "Salatalar & Mezeler", "hamur": "Hamur İşleri", "ana yemek": "Ana Yemekler",
                "et": "Ana Yemekler", "sebze": "Ana Yemekler", "baklagil": "Ana Yemekler"
            }
            target_cat = None
            for kw, cat in cat_keywords.items():
                if kw in text.lower():
                    target_cat = cat
                    break
            
            if target_cat:
                filtered = [r['name'] for r in self.recipes if target_cat in r.get('category', '')]
                if filtered:
                    response_parts.append(f"Ooo, **{target_cat}** mı istiyorsun? Şefin tavsiyeleri:\n\n* " + "\n* ".join(filtered[:8]) + "\n\nHangisini istersin?")
                else:
                    response_parts.append(f"Vallahi o kategoride henüz bir numaram yok ama yakında yeni tarifler gelecek!")
            else:
                response_parts.append("Hangi kategoriyi sordun anlayamadım ama her çeşit lezzetimiz mevcuttur evlat!")

        if not response_parts:
            return "Anlamadım ne dediğini, mutfakta gürültü mü var?"

        return " ".join(response_parts)

if __name__ == "__main__":
    bot = BoluluSefBot()
    print(bot.get_chef_response("Menemen nasıl yapılır?"))
