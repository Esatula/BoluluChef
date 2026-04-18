import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from chef_logic import BoluluSefBot

def run_evaluation():
    # Test veri seti (Chatbot'un daha önce görmediği örnekler eklenebilir)
    test_data = [
        ("merhaba usta", "greeting"),
        ("nasılsın şefim", "how_are_you"),
        ("sen kimsin", "greeting"),
        ("günaydın", "greeting"),
        ("menemen yapılışı nedir", "recipe_request"),
        ("karnıyarık tarifi lazım", "recipe_request"),
        ("baklava nasıl pişirilir", "recipe_request"),
        ("sütlaç malzemeleri nedir", "recipe_request"),
        ("dolapta patlıcan ve kıyma var", "ingredient_based"),
        ("yumurta domates biberim var", "ingredient_based"),
        ("mercimeğim var ne yapsam", "ingredient_based"),
        ("evde un ve şeker var", "ingredient_based"),
        ("ne pişirebilirim", "ingredient_based"),
        ("hangi çorbalar var", "category_request"),
        ("tatlı tarifleri ver", "category_request"),
        ("et yemeği ne önerirsin", "category_request"),
        ("sebze yemekleri listesi", "category_request"),
        ("baklagil tarifleri", "category_request"),
        ("meze çeşitleri", "category_request"),
        ("hamur işleri neler", "category_request")
    ]
    
    bot = BoluluSefBot()
    
    y_true = [item[1] for item in test_data]
    y_pred = [bot.predict_intent(item[0]) for item in test_data]
    
    # 1. Accuracy
    acc = accuracy_score(y_true, y_pred)
    print(f"Intent Classification Accuracy: %{acc*100:.2f}")
    
    # 2. Classification Report
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred))
    
    # 3. Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=np.unique(y_true), yticklabels=np.unique(y_true), cmap='Blues')
    plt.xlabel('Tahmin Edilen')
    plt.ylabel('Gerçek')
    plt.title('Intent Classification Confusion Matrix')
    plt.savefig('intent_confusion_matrix.png')
    print("\nConfusion Matrix 'intent_confusion_matrix.png' olarak kaydedildi.")

if __name__ == "__main__":
    run_evaluation()
