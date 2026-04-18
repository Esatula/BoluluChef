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
        
        # Recipe search
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vectorizer = TfidfVectorizer()
        self.recipe_names = [r['name'] for r in self.recipes]
        self.recipe_vectors = self.vectorizer.fit_transform(self.recipe_names)

        # State tracking
        self.state = {"last_intent": None}

        # Intent Priority
        self.INTENT_PRIORITY = [
            "recipe_request",
            "ingredient_input",
            "category_request",
            "how_are_you",
            "greeting",
            "thanks",
            "goodbye",
            "addressing"
        ]

        # Incompatible Filter (User's list)
        self.INCOMPATIBLE = {
            "goodbye": ["greeting", "how_are_you", "recipe_request"],
            "thanks": ["greeting"],
        }

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

    def predict_intents(self, text, threshold=0.7):
        text_emb = self.model.encode([text])
        detected_intents = []

        for intent, emb in self.intent_embeddings.items():
            sims = cosine_similarity(text_emb, emb).flatten()
            max_sim = sims.max()
            if max_sim > threshold:
                detected_intents.append((intent, float(max_sim)))
        
        detected_intents.sort(key=lambda x: x[1], reverse=True)
        return detected_intents

    def filter_intents(self, detected_intents):
        # detected_intents is a list of (name, score)
        intent_names = [d[0] for d in detected_intents]
        intent_scores = {d[0]: d[1] for d in detected_intents}
        
        filtered = list(intent_names)
        for intent in intent_names:
            if intent in self.INCOMPATIBLE:
                for bad in self.INCOMPATIBLE[intent]:
                    if bad in filtered:
                        # Only remove if the current intent has a HIGHER score than the bad one
                        if intent_scores[intent] > intent_scores[bad]:
                            filtered.remove(bad)
        return filtered

    def select_main_intent(self, filtered_names):
        for priority_intent in self.INTENT_PRIORITY:
            if priority_intent in filtered_names:
                return priority_intent
        return None

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
        valid_recipes = []
        for recipe in self.recipes:
            ingredients = recipe.get('ingredients', [])
            if not ingredients:
                continue
            
            match_count = len(set(user_ingredients) & set(ingredients))
            scores.append(match_count / len(ingredients))
            valid_recipes.append(recipe)
            
        if not scores:
            return None
            
        best_idx = np.argmax(scores)
        if scores[best_idx] > 0:
            return valid_recipes[best_idx]
        return None

    def handle_main_intent(self, intent, text):
        if not intent:
            return "Ne demek istediğini tam çıkaramadım ama mutfakta çözülmeyecek şey yok 😄"

        if intent in self.smalltalk_responses:
            return random.choice(self.smalltalk_responses[intent])

        if intent == "recipe_request":
            recipe = self.find_recipe_by_name(text)
            if recipe:
                steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(recipe['steps'])])
                return f"Bak hele! **{recipe['name']}** dediğin öyle her yiğidin harcı değildir. Bolu usulü şöyle yapılır:\n\n{steps}\n\nAfiyet olsun!"
            else:
                return "Vallahi o tarifi henüz bizim Bolulu ustalardan duymadım, ama menemen falan sorsan hemen döktürürdüm."
        
        elif intent == "ingredient_input":
            extracted = self.extract_ingredients(text)
            if not extracted:
                 return "Bak hele! Malzeme var diyorsun ama ne olduğunu çıkaramadım. Biraz daha açık söyle de tencereyi kaynatalım!"
            
            recipe = self.recommend_by_ingredients(extracted)
            if recipe:
                # Custom flair as requested by user
                return f"Bak hele! **{', '.join(extracted)}** varsa sana güzel bir şey çıkar 😄\n\n**{recipe['name']}** yapabilirsin. Bolu usulü mis gibi olur. Tarifini istersen söylemen yeterli!"
            else:
                return "Mutfaktaki o malzemelerle ancak çay demlenir gibi duruyor evlat. Biraz daha malzeme getir de şenlenelim!"

        elif intent == "category_request":
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
                    return f"Ooo, **{target_cat}** mı istiyorsun? Şefin tavsiyeleri:\n\n* " + "\n* ".join(filtered[:8]) + "\n\nHangisinin tarifini istersin?"
                else:
                    return f"Vallahi o kategoride henüz bir numaram yok ama yakında yeni tarifler gelecek!"
            return "Hangi kategoriyi sordun anlayamadım ama her çeşit lezzetimiz mevcuttur evlat!"

        return "Anlayamadım ne dediğini, mutfakta gürültü mü var?"

    def get_chef_response(self, text):
        detected = self.predict_intents(text)
        
        # DEBUG
        # print(f"DEBUG detected: {detected}")

        # 1. Fallback for very low confidence
        if not detected:
            return "Ne demek istediğini tam çıkaramadım ama mutfakta çözülmeyecek şey yok 😄"
        
        if detected[0][1] < 0.5:
             return "Biraz daha açık söyler misin evlat, mutfakta kepçe sesinden tam duyulmuyor 😄"

        # 2. Filter Incompatible
        filtered_names = self.filter_intents(detected)
        print(f"DEBUG filtered_names: {filtered_names}")
        
        # 3. Select Main Intent
        main_intent = self.select_main_intent(filtered_names)
        print(f"DEBUG main_intent: {main_intent}")
        
        # 4. Handle Cooldown
        skip_smalltalk = False
        if self.state["last_intent"] == main_intent and main_intent in ["greeting", "how_are_you", "addressing"]:
            skip_smalltalk = True
        
        self.state["last_intent"] = main_intent
        
        # 5. Generate Response
        response = self.handle_main_intent(main_intent, text)
        
        # 6. Add Support (Controlled greeting)
        if "greeting" in filtered_names and main_intent != "greeting" and not skip_smalltalk:
            greet = random.choice(self.smalltalk_responses["greeting"])
            response = f"{greet} {response}"

        return response

if __name__ == "__main__":
    bot = BoluluSefBot()
    print(bot.get_chef_response("Menemen nasıl yapılır?"))
