"""Bölüm 10: Gruplama ve özetleme — groupby, agg, pivot_table, crosstab."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=10,
    baslik="Gruplama ve özetleme",
    anlatim=(
        "Yöneticinin sorularının çoğu \"... başına\" ile biter. Bu bölümde groupby'ın "
        "mantığını, birden fazla özeti aynı anda hesaplamayı (agg), pivot_table'ı ve "
        "müşteri yoğunlaşmasını (Pareto) öğreneceksin."
    ),
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı gözlem",
            aciklama="Sipariş SAYISINDA önde olan bir şehir, toplam CİRODA geride kalabilir: tek bir pahalı sipariş sonucu değiştirebilir. Hangi ölçütle baktığını raporda her zaman yaz.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b10-s01",
        gun=10,
        tur="python",
        kavram="groupby ve sum",
        anlatim="""
Yöneticinin sorularının çoğu "... başına" ile biter: şehir başına ciro, kategori başına
sipariş sayısı. `groupby` üç adımda çalışır: **böl** (seçtiğin sütunun her farklı değeri
için tabloyu ayrı bir parçaya böl), **uygula** (her parçaya aynı özet fonksiyonunu
uygula), **birleştir** (sonuçları tek bir tabloda topla, her grup bir satır olsun).
""",
        ornek="""kucuk = pd.DataFrame({"kategori": ["A", "B", "A", "A"], "adet": [3, 1, 2, 5]})
print(kucuk.groupby("kategori")["adet"].sum().sort_values(ascending=False))
# kategori
# A    10
# B     1""",
        ornek_dili="python",
        soru="`df`'e `ciro = adet * birim_fiyat` sütununu ekle. Şehir başına toplam ciroyu, azalan sırada bir sözlük olarak `result`'a yaz.",
        beklenen="result = {'Ankara': 9800, 'İstanbul': 4290, 'İzmir': 2140, 'Bursa': 1900}",
        ipucu="df.groupby('sehir')['ciro'].sum().sort_values(ascending=False).to_dict()",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            "result = df.groupby('sehir')['ciro'].sum().sort_values(ascending=False).to_dict()"
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b10-s02",
        gun=10,
        tur="python",
        kavram="agg (named aggregation)",
        anlatim="""
Gerçek bir rapor tablosu tek bir sayıdan fazlasını ister. Birden fazla özet istiyorsan
**named aggregation** kullanılır: her yeni sütuna bir ad verip hangi sütunun hangi
fonksiyonla özetleneceği söylenir — `agg(yeni_ad=("kaynak_sutun", "fonksiyon"))`. Sık
kullanılan fonksiyonlar: `sum`, `mean`, `count` (boş olmayanları sayar), `nunique` (farklı
değer sayısı). `as_index=False` yazmazsan grup sütunu index'e gider; sonucu başka bir
işlemde kullanacaksan `as_index=False` ya da `.reset_index()` ekle.
""",
        ornek="""kucuk = pd.DataFrame({"sehir": ["A", "A", "B"], "musteri": ["M1", "M2", "M1"], "tutar": [10, 20, 5]})
print(kucuk.groupby("sehir", as_index=False).agg(
    siparis=("tutar", "count"), toplam=("tutar", "sum"), musteri=("musteri", "nunique"),
))
#   sehir  siparis  toplam  musteri
#      A        2      30        2
#      B        1       5        1""",
        ornek_dili="python",
        soru=(
            "`ciro` sütununu ekledikten sonra kategori bazında `siparis` (sipariş sayısı), `toplam_ciro` "
            "(ciro toplamı), `ort_ciro` (ciro ortalaması) ve `musteri` (benzersiz müşteri sayısı) "
            "sütunlarını içeren bir DataFrame'i (as_index=False) `result`'a yaz."
        ),
        beklenen="3 satır (Elektronik, Giyim, Kitap), 5 sütun (kategori dahil).",
        ipucu=(
            "df.groupby('kategori').agg(siparis=('siparis_id','count'), toplam_ciro=('ciro','sum'), "
            "ort_ciro=('ciro','mean'), musteri=('musteri_id','nunique')) ve as_index=False ekle."
        ),
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            "result = df.groupby('kategori', as_index=False).agg(\n"
            "    siparis=('siparis_id', 'count'),\n"
            "    toplam_ciro=('ciro', 'sum'),\n"
            "    ort_ciro=('ciro', 'mean'),\n"
            "    musteri=('musteri_id', 'nunique'),\n"
            ")"
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b10-s03",
        gun=10,
        tur="python",
        kavram="pivot_table",
        anlatim="""
`pivot_table`, iki kategorik değişkeni satır-sütuna yayar — Excel'deki pivot tablonun
birebir karşılığı: `index=` (satırlar), `columns=` (sütunlar), `values=` (hangi sayı),
`aggfunc=` (nasıl özetlenecek), boş hücreler için `fill_value=0`. Yakın akrabası
`crosstab`, iki kategorinin birlikte kaç kez göründüğünü sayar (`normalize="index"` ile
orana çevirir). `transform` ise grup özetini, satır sayısını **koruyarak** her satıra geri
yazar: `agg` N grup için N satır döner, `transform` orijinal satır sayısı kadar döner.
""",
        ornek="""kucuk = pd.DataFrame({"sehir": ["A", "A", "B"], "kategori": ["X", "Y", "X"], "tutar": [10, 20, 5]})
print(pd.pivot_table(kucuk, values="tutar", index="sehir", columns="kategori", aggfunc="sum", fill_value=0))
# kategori   X   Y
# sehir
#        A  10  20
#        B   5   0""",
        ornek_dili="python",
        soru="`ciro` sütununu ekle. Satırlarda `sehir`, sütunlarda `kategori`, değerlerde ciro toplamı olacak şekilde bir `pivot_table` kur (boş hücreler 0). Sonucu `result`'a yaz.",
        beklenen="4 satır (şehirler), 3 sütun (kategoriler). Sağ alt köşe olmasa da toplam 18130 olmalı.",
        ipucu="pd.pivot_table(df, values='ciro', index='sehir', columns='kategori', aggfunc='sum', fill_value=0)",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            "result = pd.pivot_table(df, values='ciro', index='sehir', columns='kategori', aggfunc='sum', fill_value=0)"
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b10-s04",
        gun=10,
        tur="python",
        kavram="Pareto: müşteri yoğunlaşması",
        anlatim="""
"En büyük müşterilerimiz cironun ne kadarını getiriyor?" sorusu **müşteri yoğunlaşması**
(Pareto) analizidir. `cumsum()` (kümülatif toplam), sıralanmış bir serinin her satırına
kadar olan toplamı verir; bunu genel toplama bölüp yüzdeye çevirince, "en büyük N
müşteri cironun yüzde kaçını getiriyor?" sorusunu cevaplarsın. Bu tablo, "kimi kaybedersek
en çok canımız yanar" sorusunun ve müşteri segmentasyonunun başlangıç noktasıdır.
""",
        ornek="""satislar = pd.Series([50, 30, 15, 5], index=["M1", "M2", "M3", "M4"])  # zaten azalan sıralı
pay = (satislar.cumsum() / satislar.sum() * 100).round(1)
print(pay.iloc[0])    # -> 50.0   (M1 tek başına toplamın yarısı)""",
        ornek_dili="python",
        soru="`ciro` sütununu ekle. Müşteri bazında toplam ciroyu azalan sırala, kümülatif payı (%) hesapla. En büyük tek müşterinin toplam ciro içindeki payını (1 ondalık, yüzde) `result`'a yaz.",
        beklenen="result = 35.9",
        ipucu="musteri_ciro.cumsum() / musteri_ciro.sum() * 100, ilk (en büyük) satırı al.",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            "musteri_ciro = df.groupby('musteri_id')['ciro'].sum().sort_values(ascending=False)\n"
            "kumulatif_pay = (musteri_ciro.cumsum() / musteri_ciro.sum() * 100).round(1)\n"
            "result = kumulatif_pay.iloc[0]"
        ),
        tablo="siparisler",
    ),
]
