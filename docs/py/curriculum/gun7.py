"""Bölüm 7: pandas I — Series, DataFrame, veri okuma ve ilk bakış."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=7,
    baslik="pandas I: okuma ve ilk bakış",
    anlatim=(
        "Bölüm 7'den 13'e kadar aynı küçük e-ticaret sipariş tablosunu (`siparisler`, "
        "10 satır) kullanacağız. Bu bölümde her yeni veri setinde ilk çalıştıracağın "
        "komutları (shape, value_counts, nunique, describe) öğreneceksin."
    ),
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı gözlem",
            aciklama="Fiyat gibi sütunlarda ortalama ile medyan genelde birbirinden epey uzaktır: tek bir pahalı ürün ortalamayı yukarı çeker, medyanı etkilemez.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b7-s01",
        gun=7,
        tur="python",
        kavram="shape",
        anlatim="""
pandas'ın iki temel nesnesi: **DataFrame** (satır-sütunlu bir tablo, Excel'deki bir sayfa
gibi) ve **Series** (tek bir sütun). Her DataFrame, yan yana dizilmiş Series'lerden oluşur.
Her satırın bir **index**'i (satır etiketi) vardır; varsayılan olarak 0, 1, 2... diye gider.

Bir veri setini aldığın an, analiz yapmadan önce ona "ne olduğunu" sorarsın. `df.shape`,
`(satır_sayısı, sütun_sayısı)` biçiminde bir tuple döndürür — her yeni tabloda ilk
çalıştıracağın komutlardan biri budur.
""",
        ornek="""ornek_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
print(ornek_df.shape)    # -> (3, 2)   3 satır, 2 sütun""",
        ornek_dili="python",
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
        anlatim="""
`df["sütun"]` tek köşeli parantezle bir **Series** döndürür; `df[["a", "b"]]` çift köşeli
parantezle (içteki parantez aslında bir liste) bir **DataFrame** döndürür. Bir Series'in
`.value_counts()` metodu, o sütundaki her farklı değerin kaç kez geçtiğini, azalan sırada
döndürür — kategorik bir sütunu (şehir, kategori, durum...) tanımanın en hızlı yoludur.
""",
        ornek="""renkler = pd.Series(["kırmızı", "mavi", "kırmızı", "yeşil", "mavi", "kırmızı"])
print(renkler.value_counts().to_dict())    # -> {'kırmızı': 3, 'mavi': 2, 'yeşil': 1}""",
        ornek_dili="python",
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
        anlatim="""
Diğer hızlı tanıma soruları: `df["sütun"].nunique()` kaç **farklı** değer olduğunu sayar
(tekrarları bir kez sayar), `df["sütun"].unique()` o farklı değerlerin kendisini bir dizi
olarak verir, `df.columns.tolist()` ise bütün sütun adlarının listesini verir.
""",
        ornek="""seri = pd.Series(["A", "B", "A", "C", "B", "A"])
print(seri.nunique())    # -> 3   (A, B, C: üç farklı değer)
print(list(seri.unique()))     # -> ['A', 'B', 'C']""",
        ornek_dili="python",
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
        anlatim="""
`df.describe().round(1)`, sayısal sütunların özetini (count, mean, std, min, çeyrekler,
max) tek tabloda verir. Önemli bir okuma alışkanlığı: **ortalama (mean) ile medyanı
(median, %50'lik değer) karşılaştır**. İkisi birbirine yakınsa dağılım dengelidir; ortalama
medyandan belirgin yüksekse, birkaç büyük/aykırı değer ortalamayı yukarı çekiyor demektir —
bu durumda "tipik" değeri raporlarken medyanı tercih et.
""",
        ornek="""seri = pd.Series([10, 12, 11, 9, 100])
print(seri.mean(), seri.median())    # -> 28.4 11.0   (tek bir 100, ortalamayı çok yukarı çekti)""",
        ornek_dili="python",
        soru="`birim_fiyat` sütununun ortalaması ile medyanı arasındaki farkı (ortalama - medyan), 1 ondalığa yuvarlanmış olarak `result`'a yaz.",
        beklenen="result = 810.0",
        ipucu="df['birim_fiyat'].mean() ve .median() arasındaki farkı round(..., 1) ile yuvarla.",
        cozum="result = round(df['birim_fiyat'].mean() - df['birim_fiyat'].median(), 1)",
        tablo="siparisler",
    ),
]
