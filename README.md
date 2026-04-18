# Bolulu Şef Chatbot - NLP Projesi

Bu proje, geleneksel Türk mutfağını esprili bir "Bolulu Şef" kişiliği üzerinden tanıtan ve tarif önerileri veren bir Doğal Dil İşleme (NLP) uygulamasıdır.

## Özellikler
1. **Niyet Sınıflandırma (Intent Classification):** Kullanıcının tarif mi aradığı, malzeme mi belirttiği yoksa sohbet mi etmek istediği TF-IDF ve Lojistik Regresyon kullanılarak belirlenir.
2. **Varlık Çıkarımı (Entity Extraction):** Kullanıcı mesajındaki malzemeler anahtar kelime eşleştirme (keyword matching) yöntemiyle çekilir.
3. **Tarif Öneri Sistemi:** Kullanıcı isteğine en uygun tarif TF-IDF ve Cosine Similarity ile bulunur.
4. **Bolulu Şef Kişiliği:** Bot, Bolulu bir ustaya özgü esprili ve karakterli cevaplar verir.
5. **Arayüz:** Streamlit kullanılarak modern ve karanlık mod temalı bir sohbet arayüzü sunulmuştur.

## Kurulum ve Çalıştırma

### 1. Kütüphanelerin Yüklenmesi
```bash
pip install -r requirements.txt
```

### 2. Uygulamanın Başlatılması
```bash
streamlit run app.py
```

### 3. Model Değerlendirme
Modelin başarısını ölçmek ve Confusion Matrix oluşturmak için:
```bash
python evaluate_model.py
```

## Proje Yapısı
- `app.py`: Streamlit arayüzü ve ana uygulama akışı.
- `chef_logic.py`: NLP pipeline'ı ve chatbot mantığı.
- `data/recipes.json`: 30+ geleneksel Türk yemeği tarifi.
- `evaluate_model.py`: Model başarı metriklerini hesaplayan script.
- `populate_data.py`: Veri setini genişletmek için kullanılan araç.

## Değerlendirme Sonuçları
Değerlendirme sonucunda oluşan hata matrisine `intent_confusion_matrix.png` dosyasından ulaşabilirsiniz.
