"""Bölüm 10: Gruplama ve özetleme — groupby, agg, pivot_table, crosstab."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=10,
    baslik="Gruplama ve özetleme",
    anlatim="""
Yöneticinin sorularının çoğu "... başına" ile biter: şehir başına ciro, kategori başına
sipariş sayısı. `groupby` üç adımda çalışır: **böl** (her farklı değer için ayrı parça),
**uygula** (her parçaya aynı özeti hesapla), **birleştir** (sonuçları tek tabloda topla).

```
df.groupby("sehir")["ciro"].sum().sort_values(ascending=False)
```

Birden fazla özet istiyorsan **named aggregation** kullan:

```
df.groupby("kategori").agg(
    siparis=("siparis_id", "count"), toplam_ciro=("ciro", "sum"),
    ort_ciro=("ciro", "mean"), musteri=("musteri_id", "nunique"),
)
```

`as_index=False` yazmazsan grup sütunu index'e gider; sonucu başka bir işlemde
kullanacaksan `as_index=False` ya da `.reset_index()` ekle.

`pivot_table` iki kategoriyi satır-sütuna yayar (Excel'deki pivot'un birebir karşılığı):
`index=`, `columns=`, `values=`, `aggfunc=`, boş hücreler için `fill_value=0`.
`crosstab` iki kategorinin birlikte kaç kez göründüğünü sayar; `normalize="index"` ile
orana çevirir. `transform`, grup özetini satır sayısını koruyarak her satıra geri yazar
(agg 4 şehir için 4 satır döner, transform 10 sipariş için 10 satır döner).
""",
    ornek="""musteri_ciro = df.groupby("musteri_id")["ciro"].sum().sort_values(ascending=False)
kumulatif_pay = (musteri_ciro.cumsum() / musteri_ciro.sum() * 100).round(1)
print(kumulatif_pay)
# -> en büyük müşteri tek başına cironun %35,9'unu getiriyor (Pareto)""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı rakam",
            aciklama="İstanbul'un 4 siparişi var ama ciroda Ankara (3 sipariş) önde: tek bir 6.500 TL'lik monitör yüzünden. Ölçüt değişince cevap değişir.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b10-s01",
        gun=10,
        tur="python",
        kavram="groupby ve sum",
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
