import json

def categorize_recipes():
    # Mevcut tarifler
    recipes = [
        {
            "id": 1,
            "name": "Menemen",
            "ingredients": ["yumurta", "domates", "biber"],
            "steps": ["Biberleri kavurun, domatesi ekleyin, yumurtayı kırın."],
            "category": "Ana Yemekler (Sebzeliler)"
        },
        {
            "id": 2,
            "name": "Mercimek Çorbası",
            "ingredients": ["kırmızı mercimek", "soğan", "havuç", "patates", "salça", "yağ"],
            "steps": ["Sebzeleri doğrayıp yağda kavurun.", "Yıkanmış mercimeği ve suyu ekleyin.", "Mercimekler yumuşayana kadar pişirin.", "Blenderdan geçirip sosuyla servis edin."],
            "category": "Çorbalar"
        },
        {
            "id": 3,
            "name": "Karnıyarık",
            "ingredients": ["patlıcan", "kıyma", "soğan"],
            "steps": ["Patlıcanları kızartın, kıymalı harcı doldurup pişirin."],
            "category": "Ana Yemekler (Etliler)"
        },
        {
            "id": 4,
            "name": "Mantı",
            "ingredients": ["un", "yumurta", "su", "kıyma", "soğan", "yoğurt", "sarımsak"],
            "steps": ["Hamuru yoğurup ince açın.", "Minik kareler kesip kıymalı harç ile kapatın.", "Haşlayıp üzerine sarımsaklı yoğurt ve yağ dökün."],
            "category": "Hamur İşleri"
        },
        {
            "id": 5,
            "name": "Sütlaç",
            "ingredients": ["süt", "pirinç", "şeker", "nişasta", "vanilya"],
            "steps": ["Pirinci haşlayın.", "Sütü ve şekeri ekleyip kaynatın.", "Nişasta ile kıvam aldırıp fırınlayın."],
            "category": "Tatlılar"
        },
        {
            "id": 6,
            "name": "İskender Kebap",
            "ingredients": ["döner eti", "pide", "tereyağı", "domates sosu", "yoğurt"],
            "steps": ["Pideleri küp doğrayıp ısıtın.", "Üzerine döner etlerini dizin.", "Sıcak domates sosu ve kızgın tereyağı gezdirin."],
            "category": "Ana Yemekler (Etliler)"
        },
        {
            "id": 7,
            "name": "Yaprak Sarma",
            "ingredients": ["asma yaprağı", "pirinç", "soğan", "zeytinyağı", "nane"],
            "steps": ["İç harcı hazırlayıp soğutun.", "Yaprakları tek tek sarın.", "Tencereye dizip pişirin."],
            "category": "Salatalar & Mezeler"
        },
        {
            "id": 8,
            "name": "Hünkar Beğendi",
            "ingredients": ["kuzu eti", "patlıcan", "süt", "un", "tereyağı", "kaşar peyniri"],
            "steps": ["Etleri soteleyip pişirin.", "Patlıcanları közleyip ezin.", "Beşamel sos hazırlayıp patlıcanla karıştırın."],
            "category": "Ana Yemekler (Etliler)"
        },
        {
            "id": 9,
            "name": "Baklava",
            "ingredients": ["yufka", "ceviz", "tereyağı", "şerbet"],
            "steps": ["Yufkaları kat kat yağlayıp tepsiye dizin.", "Araya ceviz serpin.", "Dilimleyip pişirin ve şerbetleyin."],
            "category": "Tatlılar"
        },
        {
            "id": 10,
            "name": "Lahmacun",
            "ingredients": ["un", "kıyma", "soğan", "sarımsak", "maydanoz", "biber", "domates", "isot"],
            "steps": ["Hamuru inceceik açın.", "İç harcı hazırlayıp üzerine yayın.", "Taş fırında veya tavada pişirin."],
            "category": "Hamur İşleri"
        },
        {
            "id": 11,
            "name": "Kısır",
            "ingredients": ["ince bulgur", "sıcak su", "salça", "zeytinyağı", "nar ekşisi", "taze soğan", "maydanoz"],
            "steps": ["Bulguru sıcak suyla ıslatın.", "Kalan malzemeleri ekleyip karıştırın."],
            "category": "Salatalar & Mezeler"
        },
        {
            "id": 12,
            "name": "İçli Köfte",
            "ingredients": ["bulgur", "irmik", "kıyma", "ceviz", "soğan", "baharat"],
            "steps": ["Dış hamuru hazırlayın.", "İç harcı kavurup soğutun.", "İçini doldurup kapatın ve kızartın."],
            "category": "Hamur İşleri"
        },
        {
            "id": 13,
            "name": "Ezogelin Çorbası",
            "ingredients": ["mercimek", "bulgur", "pirinç", "soğan", "nane", "salça"],
            "steps": ["Bakliyatları pişirin.", "Sosunu hazırlayıp karıştırın."],
            "category": "Çorbalar"
        },
        {
            "id": 14,
            "name": "Künefe",
            "ingredients": ["kadayıf", "peynir", "tereyağı", "şerbet", "antep fıstığı"],
            "steps": ["Kadayıfları yağlayıp tepsiye dizin.", "Araya peyniri koyun.", "Kızartıp şerbetini verin."],
            "category": "Tatlılar"
        },
        {
            "id": 15,
            "name": "Pilav",
            "ingredients": ["pirinç", "tereyağı", "şehriye", "su"],
            "steps": ["Şehriyeleri kavurun.", "Yıkanmış pirinci ekleyip kavurun.", "Suyunu ekleyip demlenmeye bırakın."],
            "category": "Ana Yemekler (Sebzeliler)"
        },
        {
            "id": 16,
            "name": "İmam Bayıldı",
            "ingredients": ["patlıcan", "soğan", "sarımsak", "domates", "zeytinyağı"],
            "steps": ["Patlıcanları kızartın.", "Soğanlı harcı hazırlayıp doldurun.", "Zeytinyağı ile pişirin."],
            "category": "Ana Yemekler (Sebzeliler)"
        },
        {
            "id": 17,
            "name": "Ayran Aşı Çorbası",
            "ingredients": ["yoğurt", "buğday", "nohut", "nane"],
            "steps": ["Buğday ve nohudu haşlayın.", "Soğuk yoğurtla karıştırın."],
            "category": "Çorbalar"
        },
        {
            "id": 18,
            "name": "Kadınbudu Köfte",
            "ingredients": ["kıyma", "pirinç", "yumurta", "un", "soğan"],
            "steps": ["Pirinci haşlayın.", "Kıyma ile yoğurun.", "Yumurta ve una bulayıp kızartın."],
            "category": "Ana Yemekler (Etliler)"
        },
        {
            "id": 19,
            "name": "Su Böreği",
            "ingredients": ["un", "yumurta", "peynir", "tereyağı"],
            "steps": ["Hamurları haşlayın.", "Yağlanmış tepsiye dizin.", "Araya peynir koyup pişirin."],
            "category": "Hamur İşleri"
        },
        {
            "id": 20,
            "name": "Piyaz",
            "ingredients": ["fasulye", "soğan", "maydanoz", "tahin", "sirke"],
            "steps": ["Fasulyeleri haşlayın.", "Tahinli sos hazırlayıp üzerine dökün."],
            "category": "Salatalar & Mezeler"
        },
        {
            "id": 21,
            "name": "Ali Nazik",
            "ingredients": ["patlıcan", "yoğurt", "kuzu eti", "tereyağı"],
            "steps": ["Patlıcanı közleyip yoğurtla karıştırın.", "Kavrulmuş etleri üzerine ekleyin."],
            "category": "Ana Yemekler (Etliler)"
        },
        {
            "id": 22,
            "name": "Şekerpare",
            "ingredients": ["un", "irmik", "yumurta", "şerbet"],
            "steps": ["Hamuru şekillendirin.", "Fırınlayıp sıcakken şerbetini dökün."],
            "category": "Tatlılar"
        },
        {
            "id": 23,
            "name": "Tas Kebabı",
            "ingredients": ["dana eti", "soğan", "domates", "salça"],
            "steps": ["Eti sebzelerle beraber ağır ateşte pişirin."],
            "category": "Ana Yemekler (Etliler)"
        },
        {
            "id": 24,
            "name": "Kabak Tatlısı",
            "ingredients": ["kabak", "şeker", "tahin", "ceviz"],
            "steps": ["Kabakları şekerle pişirin.", "Tahin ve cevizle servis edin."],
            "category": "Tatlılar"
        },
        {
            "id": 25,
            "name": "Etli Ekmek",
            "ingredients": ["hamur", "kıyma", "domates", "biber"],
            "steps": ["İnce hamur açın.", "Üzerine kıymalı harç yayın.", "Fırınlayın."],
            "category": "Hamur İşleri"
        },
        {
            "id": 26,
            "name": "Aşure",
            "ingredients": ["buğday", "fasulye", "nohut", "kayısı", "incir", "fındık"],
            "steps": ["Malzemeleri haşlayıp karıştırın.", "Şekerle pişirin."],
            "category": "Tatlılar"
        },
        {
            "id": 27,
            "name": "Cacık",
            "ingredients": ["yoğurt", "salatalık", "sarımsak", "nane"],
            "steps": ["Salatalıkları doğrayın.", "Yoğurt ve suyla karıştırın."],
            "category": "Salatalar & Mezeler"
        },
        {
            "id": 28,
            "name": "İzmir Köfte",
            "ingredients": ["kıyma", "patates", "domates", "biber"],
            "steps": ["Köfteleri ve patatesleri kızartıp fırınlayın."],
            "category": "Ana Yemekler (Etliler)"
        },
        {
            "id": 29,
            "name": "Mercimek Köftesi",
            "ingredients": ["kırmızı mercimek", "bulgur", "soğan", "salça", "maydanoz"],
            "steps": ["Mercimeği haşlayın, bulguru ekleyin, yoğurup şekil verin."],
            "category": "Salatalar & Mezeler"
        },
        {
            "id": 30,
            "name": "Biber Dolması",
            "ingredients": ["biber", "pirinç", "soğan", "kıyma", "salça"],
            "steps": ["İç harcı hazırlayıp biberleri doldurun ve pişirin."],
            "category": "Ana Yemekler (Sebzeliler)"
        },
        {
            "id": 31,
            "name": "Tavuk Sote",
            "ingredients": ["tavuk", "biber", "domates", "soğan"],
            "steps": ["Tavukları ve sebzeleri soteleyerek pişirin."],
            "category": "Ana Yemekler (Etliler)"
        },
        {
            "id": 32,
            "name": "Pilaki",
            "ingredients": ["fasulye", "havuç", "patates", "soğan", "zeytinyağı"],
            "steps": ["Fasulyeleri ve sebzeleri zeytinyağında pişirin."],
            "category": "Salatalar & Mezeler"
        },
        {
            "id": 33,
            "name": "Revani",
            "ingredients": ["irmik", "yoğurt", "yumurta", "un", "şerbet"],
            "steps": ["Keki pişirip şerbetleyin."],
            "category": "Tatlılar"
        },
        {
            "id": 34,
            "name": "Taze Fasulye",
            "ingredients": ["taze fasulye", "domates", "soğan", "zeytinyağı"],
            "steps": ["Fasulyeleri domates ve soğanla beraber pişirin."],
            "category": "Ana Yemekler (Sebzeliler)"
        },
        {
            "id": 35,
            "name": "Domates Çorbası",
            "ingredients": ["domates", "un", "tereyağı", "süt"],
            "steps": ["Unu kavurun, domatesi ekleyip pişirin ve sütleyin."],
            "category": "Çorbalar"
        },
        {
            "id": 36,
            "name": "Kuru Fasulye",
            "ingredients": ["kuru fasulye", "soğan", "salça", "pastırma", "zeytinyağı"],
            "steps": ["Fasulyeleri ıslatın.", "Soğan ve salçalı sosu hazırlayıp fasulyeleri ekleyin.", "Helmeleşene kadar pişirin.", "Şefin tavsiyesi: Yanına bol soğan kırın!"],
            "category": "Ana Yemekler (Baklagiller)"
        },
        {
            "id": 37,
            "name": "Nohut Yemeği",
            "ingredients": ["nohut", "kıyma", "soğan", "salça"],
            "steps": ["Nohudu pişirip kıymalı harçla birleştirin."],
            "category": "Ana Yemekler (Baklagiller)"
        },
        {
            "id": 38,
            "name": "Havuç Tarator",
            "ingredients": ["havuç", "yoğurt", "sarımsak", "ceviz"],
            "steps": ["Havuçları soteleyip sarımsaklı yoğurtla karıştırın."],
            "category": "Salatalar & Mezeler"
        },
        {
            "id": 39,
            "name": "Humus",
            "ingredients": ["nohut", "tahin", "limon", "sarımsak"],
            "steps": ["Nohudu haşlayıp diğer malzemelerle püre yapın."],
            "category": "Salatalar & Mezeler"
        },
        {
            "id": 40,
            "name": "Mücver",
            "ingredients": ["kabak", "yumurta", "un", "dereotu"],
            "steps": ["Kabakları rendeleyip malzemelerle kızartın."],
            "category": "Salatalar & Mezeler"
        }
    ]

    with open('data/recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)

    print(f"Toplam {len(recipes)} tarif yeni kategorilerle kaydedildi.")

if __name__ == "__main__":
    categorize_recipes()
