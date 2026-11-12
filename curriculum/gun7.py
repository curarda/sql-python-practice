"""Bölüm 7: pandas I — Series, DataFrame, veri okuma ve ilk bakış."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=7,
    baslik="pandas I: okuma ve ilk bakış",
    anlatim="""
pandas'ın iki temel nesnesi: **DataFrame** (satır-sütunlu bir tablo, Excel'deki bir sayfa
gibi) ve **Series** (tek bir sütun). Her DataFrame, yan yana dizilmiş Series'lerden oluşur.
Her satırın bir **index**'i (satır etiketi) vardır; varsayılan olarak 0, 1, 2...

Bu bölümden Bölüm 13'e kadar aynı küçük e-ticaret sipariş tablosunu (`siparisler`,
10 satır: `siparis_id, tarih, musteri_id, sehir, kategori, urun, adet, birim_fiyat`)
kullanacağız. `df = pd.read_csv("siparisler.csv")` ile gerçek işte böyle bir tablo gelir.

Her yeni veri setinde çalıştırılacak beş komut:

```
df.head(3)                    # ilk 3 satır
df.shape                      # (satır, sütun) sayısı
df.info()                     # sütun tipleri ve dolu değer sayıları
df.describe().round(1)        # sayısal sütunların özeti
df["sehir"].value_counts()    # bir sütundaki her değerin sayısı
```

`df["sütun"]` tek köşeli parantezle bir **Series** döndürür; `df[["a", "b"]]` çift köşeli
parantezle bir **DataFrame** döndürür (içteki parantez aslında bir liste).
""",
    ornek="""fiyat = df["birim_fiyat"]
print(type(fiyat))                                  # -> <class 'pandas.Series'>
print(fiyat.mean(), fiyat.median(), fiyat.max())     # -> 1445.0 635.0 6500""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı rakam",
            aciklama="birim_fiyat'ın ortalaması (1445) medyanının (635) iki katından fazla: tek bir 6500 TL'lik monitör dağılımı sağa çekiyor.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b7-s01",
        gun=7,
        tur="python",
        kavram="shape",
        soru="`df` (siparisler tablosu) kaç satır ve sütundan oluşuyor? `(satır, sütun)` tuple'ını `result`'a yaz.",
        beklenen="result = (10, 8)",
        ipucu="df.shape bir (satır_sayisi, sutun_sayisi) tuple'ı döndürür.",
        cozum="result = df.shape",
        tablo="siparisler",
    ),
    Soru(
        id="b7-s02",
        gun=7,
        tur="python",
        kavram="value_counts",
        soru="`sehir` sütunundaki her şehrin kaç kez geçtiğini bir sözlük olarak `result`'a yaz.",
        beklenen="result = {'İstanbul': 4, 'Ankara': 3, 'İzmir': 2, 'Bursa': 1}",
        ipucu="df['sehir'].value_counts().to_dict() her şehrin sayısını sözlük yapar.",
        cozum="result = df['sehir'].value_counts().to_dict()",
        tablo="siparisler",
    ),
    Soru(
        id="b7-s03",
        gun=7,
        tur="python",
        kavram="nunique",
        soru="`kategori` sütununda kaç farklı değer olduğunu `result`'a tam sayı olarak yaz.",
        beklenen="result = 3",
        ipucu="df['kategori'].nunique() farklı değer sayısını verir.",
        cozum="result = df['kategori'].nunique()",
        tablo="siparisler",
    ),
    Soru(
        id="b7-s04",
        gun=7,
        tur="python",
        kavram="describe: ortalama ve medyan farkı",
        soru="`birim_fiyat` sütununun ortalaması ile medyanı arasındaki farkı (ortalama - medyan), 1 ondalığa yuvarlanmış olarak `result`'a yaz.",
        beklenen="result = 810.0",
        ipucu="df['birim_fiyat'].mean() ve .median() arasındaki farkı round(..., 1) ile yuvarla.",
        cozum="result = round(df['birim_fiyat'].mean() - df['birim_fiyat'].median(), 1)",
        tablo="siparisler",
    ),
]
