import json
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

class BoluluSefBot:
    def __init__(self, recipes_path='data/recipes.json'):
        self.load_recipes(recipes_path)
        self.train_intent_model()
        self.vectorizer = TfidfVectorizer()
        self.recipe_names = [r['name'] for r in self.recipes]
        self.recipe_vectors = self.vectorizer.fit_transform(self.recipe_names)

    def load_recipes(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            self.recipes = json.load(f)

    def train_intent_model(self):
        # Örnek eğitim verileri
        data = [
            ("merhaba", "smalltalk"),
            ("selam", "smalltalk"),
            ("nasılsın", "smalltalk"),
            ("kimsin sen", "smalltalk"),
            ("hoşçakal", "smalltalk"),
            ("menemen nasıl yapılır", "recipe_request"),
            ("mantı tarifi ver", "recipe_request"),
            ("sütlaç yapar mısın", "recipe_request"),
            ("baklava tarifini istiyorum", "recipe_request"),
            ("yemek tarifi", "recipe_request"),
            ("elimde yumurta ve domates var", "ingredient_based"),
            ("kıyma ve patlıcanla ne yapabilirim", "ingredient_based"),
            ("dolapta süt ve pirinç var", "ingredient_based"),
            ("malzemelerim mercimek ve soğan", "ingredient_based"),
            ("ne pişirebilirim", "ingredient_based")
        ]
        
        df = pd.DataFrame(data, columns=['text', 'intent'])
        self.intent_vectorizer = TfidfVectorizer()
        X = self.intent_vectorizer.fit_transform(df['text'])
        self.intent_model = LogisticRegression()
        self.intent_model.fit(X, df['intent'])

    def predict_intent(self, text):
        X = self.intent_vectorizer.transform([text])
        return self.intent_model.predict(X)[0]

    def extract_ingredients(self, text):
        # Basit keyword matching - Proje planında 4. adımda bahsedilen başlangıç yöntemi
        all_ingredients = set()
        for r in self.recipes:
            for ing in r['ingredients']:
                all_ingredients.add(ing.lower())
        
        found = []
        words = text.lower().split()
        for ing in all_ingredients:
            if ing in text.lower():
                found.append(ing)
        return list(set(found))

    def find_recipe_by_name(self, text):
        query_vec = self.vectorizer.transform([text])
        from sklearn.metrics.pairwise import cosine_similarity
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
            match_count = len(set(user_ingredients) & set(recipe['ingredients']))
            scores.append(match_count / len(recipe['ingredients']))
            
        best_idx = np.argmax(scores)
        if scores[best_idx] > 0:
            return self.recipes[best_idx]
        return None

    def get_chef_response(self, text):
        intent = self.predict_intent(text)
        
        if intent == "smalltalk":
            responses = [
                "Selam evlat! Bolu'nun ocağından geldim, mutfağın sırları bendedir. Ne pişireceğiz bugün?",
                "Ooo hoş geldin! Elinin lezzeti Bolu'nun havası suyu gibiyse harikalar yaratırız.",
                "Şeflerin şahı Bolulu burada! Mutfakta işler nasıl gidiyor bakalım?"
            ]
            return random.choice(responses)
        
        elif intent == "recipe_request":
            recipe = self.find_recipe_by_name(text)
            if recipe:
                steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(recipe['steps'])])
                return f"Bak hele! **{recipe['name']}** dediğin öyle her yiğidin harcı değildir. Bolu usulü şöyle yapılır:\n\n{steps}\n\nAfiyet olsun, parmaklarını yemeyesin ha! 😄"
            else:
                return "Vallahi o tarifi henüz bizim Bolulu ustalardan duymadım, ama menemen falan sorsan hemen döktürürdüm."
                
        elif intent == "ingredient_based":
            extracted = self.extract_ingredients(text)
            recipe = self.recommend_by_ingredients(extracted)
            if recipe:
                return f"Hımm, bakıyorum mutfakta **{', '.join(extracted)}** varmış. Evlat, bunlarla sana mis gibi bir **{recipe['name']}** patlatalım mı? Şeflik belgesi ister bu iş ama sana güveniyorum! 😉"
            else:
                return "Mutfaktaki o malzemelerle ancak çay demlenir gibi duruyor evlat. Biraz daha malzeme getir de şenlenelim!"

        return "Anlamadım ne dediğini, mutfakta gürültü mü var?"

if __name__ == "__main__":
    bot = BoluluSefBot()
    print(bot.get_chef_response("Menemen nasıl yapılır?"))
