"""Bölüm 13: Görselleştirme — matplotlib ve seaborn."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=13,
    baslik="Görselleştirme",
    anlatim=(
        "Bu bölümde hangi sorunun hangi grafikle cevaplandığını ve bir grafiği çizmeden "
        "önce ona hazır hâle getirilmiş veriyi (gruplanmış, sıralanmış) öğreneceksin. "
        "Alıştırmalarda grafiğin kendisini değil, çizeceği veriyi hazırlıyorsun."
    ),
    metrikler=[
        Metrik(
            baslik="Dikkat",
            aciklama="Bir dağılımın histogramı iki tepeli çıkabilir (ör. hafta içi/hafta sonu farklı davranıyorsa); tek bir ortalamaya güvenmek bu durumda yanıltıcıdır.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b13-s01",
        gun=13,
        tur="python",
        kavram="Yatay çubuk grafiği için veri",
        anlatim="""
Grafik türünü veriye değil **soruya** göre seç: zaman içindeki değişim → çizgi; gruplar
arası karşılaştırma → çubuk (uzun etiketlerde **yatay** çubuk okunur olur); dağılım →
histogram/kutu grafiği; iki sayısal değişken ilişkisi → saçılım. **Pasta grafiğinden
kaçın**: göz açıları/alanları, uzunluklar kadar doğru karşılaştıramaz.

`fig, ax = plt.subplots()` bir çerçeve (figure) ve bir çizim alanı (axes) oluşturur;
sonraki her ayar `ax.` ile yapılır. Yatay çubuk için veriyi **küçükten büyüğe** sıralamak
gerekir — `ax.barh(...)` ilk elemanı en altta çizer, böylece en büyük değer en üstte
görünür:
""",
        ornek="""kategori_adet = df.groupby("kategori")["adet"].sum().sort_values()
print(kategori_adet)
# Çizim: fig, ax = plt.subplots(); ax.barh(kategori_adet.index, kategori_adet.values)""",
        ornek_dili="python",
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
        anlatim="""
İki temel kütüphane: `matplotlib` her ayrıntıyı kontrol ettiğin temel çizim kütüphanesi;
`seaborn` matplotlib'in üzerine kurulu, DataFrame ile doğrudan çalışan ve istatistiksel
grafikleri tek satırda çizen kütüphanedir. pandas'ın kendisi de hızlı grafik çizer:
`df["sütun"].value_counts().plot(kind="bar")` keşif aşamasında en hızlı yoldur.

Anlatım grafiği için beş kural: **başlık = mesaj** (grafiğin ne gösterdiğini değil ne
söylediğini yaz), eksenlerde birim olsun ("Ciro (TL)" gibi), çubukları sırala ve sıfırdan
başlat, rengi yalnızca vurgulamak istediğin tek şey için kullan, gereksiz çizgi/ızgarayı
kaldır.
""",
        ornek="""urun_tipi_sayisi = df["urun"].value_counts()
print(urun_tipi_sayisi.to_dict())
# Çizim: urun_tipi_sayisi.plot(kind="bar")  (ya da sns.barplot / ax.bar)""",
        ornek_dili="python",
        soru="`kategori` sütunundaki her değerin kaç kez geçtiğini (bir çubuk grafiğinde çizilecek şekilde) azalan sırada bir sözlük olarak `result`'a yaz.",
        beklenen="result = {'Elektronik': 5, 'Giyim': 3, 'Kitap': 2}",
        ipucu="df['kategori'].value_counts() zaten azalan sırada döner; .to_dict() ile sözlüğe çevir.",
        cozum="result = df['kategori'].value_counts().to_dict()",
        tablo="siparisler",
    ),
]
