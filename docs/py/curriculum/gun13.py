"""Bölüm 13: Görselleştirme — matplotlib ve seaborn."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=13,
    baslik="Görselleştirme",
    anlatim="""
Bir grafiğin iki ayrı işi vardır: **keşfetmek** (veriye kendin bakmak, hızlı ve çirkin
olabilir) ve **anlatmak** (bulguyu yöneticiye göstermek, temiz ve tek mesajlı olmalı).
`matplotlib` her ayrıntıyı kontrol ettiğin temel kütüphane, `seaborn` üzerine kurulu ve
DataFrame ile doğrudan çalışan, istatistiksel grafikleri tek satırda çizen kütüphanedir.

Grafik türünü soruya göre seç: zaman içindeki değişim → çizgi; gruplar arası karşılaştırma →
çubuk (uzun etiketlerde yatay); dağılım → histogram/kutu grafiği; iki sayısal değişken
ilişkisi → saçılım. **Pasta grafiğinden kaçın**: göz açıları/alanları, uzunluklar kadar
doğru karşılaştıramaz.

`fig, ax = plt.subplots()` bir çerçeve (figure) ve bir çizim alanı (axes) oluşturur; sonraki
her ayar `ax.` ile yapılır. Anlatım grafiği için beş kural: **başlık = mesaj** (ne gösterdiğini
değil ne söylediğini yaz), eksenlerde birim olsun, çubukları sırala ve sıfırdan başlat,
rengi sadece vurgulamak için kullan, gereksiz çizgileri kaldır.

```
sehir_ciro = df.groupby("sehir")["ciro"].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(sehir_ciro.index, sehir_ciro.values)
ax.set_title("Ankara, 3 siparişle cironun yarısından fazlasını getiriyor")
```

Bu alıştırmalarda grafiğin kendisini değil, grafiğin çizeceği veriyi hazırlıyorsun —
gerçek işte bu veriyi `.plot()`, `ax.barh()` ya da `sns.barplot()`'a verirsin.
""",
    ornek="""sehir_ciro = df.groupby("sehir")["ciro"].sum().sort_values()
print(sehir_ciro)
# Çizim: fig, ax = plt.subplots(); ax.barh(sehir_ciro.index, sehir_ciro.values)""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Dikkat",
            aciklama="Günlük satışın histogramı iki tepelidir (hafta içi ~112, hafta sonu ~173); tek bir ortalamaya (130) güvenmek yanıltıcıdır.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b13-s01",
        gun=13,
        tur="python",
        kavram="Yatay çubuk grafiği için veri",
        soru="`ciro` sütununu ekle. Şehir bazında toplam ciroyu, küçükten büyüğe sıralı bir sözlük olarak `result`'a yaz (bir sonraki adımda `ax.barh(...)` ile çizilecek).",
        beklenen="result = {'Bursa': 1900, 'İzmir': 2140, 'İstanbul': 4290, 'Ankara': 9800}",
        ipucu="sort_values() varsayılan olarak küçükten büyüğe sıralar (barh'ta en büyük en üstte görünür).",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            "result = df.groupby('sehir')['ciro'].sum().sort_values().to_dict()"
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b13-s02",
        gun=13,
        tur="python",
        kavram="Histogram/çubuk için kategori sayımı",
        soru="`kategori` sütunundaki her değerin kaç kez geçtiğini (bir çubuk grafiğinde çizilecek şekilde) azalan sırada bir sözlük olarak `result`'a yaz.",
        beklenen="result = {'Elektronik': 5, 'Giyim': 3, 'Kitap': 2}",
        ipucu="df['kategori'].value_counts() zaten azalan sırada döner; .to_dict() ile sözlüğe çevir.",
        cozum="result = df['kategori'].value_counts().to_dict()",
        tablo="siparisler",
    ),
]
