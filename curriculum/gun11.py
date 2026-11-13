"""Bölüm 11: Tabloları birleştirme — merge ve concat."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=11,
    baslik="Tabloları birleştirme: merge ve concat",
    anlatim=(
        "Şirket verisi hiçbir zaman tek tabloda durmaz. Bu bölümde iki tabloyu ortak bir "
        "anahtar üzerinden yan yana getirmeyi (merge/JOIN) ve bunun üç yaygın tuzağını "
        "öğreneceksin: sessizce kaybolan satırlar, çoğalan satırlar ve eşleşmeyen anahtarlar."
    ),
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı tuzak",
            aciklama="groupby, varsayılan olarak anahtarı NaN olan grubu ATAR. dropna=False yazmazsan, eşleşmeyen bir satırın cirosu raporda hiç görünmeden sessizce kaybolur.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b11-s01",
        gun=11,
        tur="python",
        kavram="LEFT JOIN ve dropna=False",
        anlatim="""
İki tabloyu ortak bir sütun (anahtar, key) üzerinden yan yana getirmek **merge**'dür
(Excel'de DÜŞEYARA/VLOOKUP, SQL'de JOIN). `how` parametresi eşleşmeyen satırlara ne
olacağını belirler: `"left"` (soldaki tablonun tüm satırları, sağda eşi yoksa NaN — en sık
kullanılan), `"inner"` (sadece iki tarafta da olanlar), `"right"`, `"outer"` (her ikisi).

**Tuzak 1 — eşleşmeyen satırlar sessizce kaybolur**: `left` ile birleştirip sonra
`groupby("sütun")` yaparsan, o sütunu boş (NaN) olan satırlar varsayılan olarak
**atılır**. `groupby("sütun", dropna=False)` yazmazsan toplam, gerçekte olduğundan
düşük çıkar.
""",
        ornek="""siparis = pd.DataFrame({"musteri_id": ["A1", "A2", "A3"], "tutar": [100, 200, 50]})
musteri = pd.DataFrame({"musteri_id": ["A1", "A2"], "sehir": ["X", "Y"]})   # A3 eksik
m = siparis.merge(musteri, on="musteri_id", how="left")
print(m.groupby("sehir", dropna=False)["tutar"].sum().to_dict())
# -> {'X': 100, 'Y': 200, nan: 50}   dropna=False olmasaydı A3'ün 50'si kaybolurdu""",
        ornek_dili="python",
        soru=(
            "`df`'e `ciro = adet * birim_fiyat` ekle. `musteriler_kucuk` ile `musteri_id` üzerinden "
            "`how='left'` birleştir. Segment bazında ciro toplamını, segmenti olmayanları da "
            "(anahtar: Python'da `None`) dahil ederek bir sözlük olarak `result`'a yaz."
        ),
        beklenen="result = {'Bronze': 1900, 'Gold': 5230, 'Silver': 4500, None: 6500}",
        ipucu="merge sonrası groupby('segment', dropna=False)['ciro'].sum().to_dict() kullan.",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            "m = df.merge(musteriler_kucuk, on='musteri_id', how='left')\n"
            "ozet = m.groupby('segment', dropna=False)['ciro'].sum()\n"
            "result = {(k if pd.notna(k) else None): int(v) for k, v in ozet.items()}"
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b11-s02",
        gun=11,
        tur="python",
        kavram="Eşleşmeyen satırları bulmak",
        anlatim="""
Birleştirmeden sonra "kaç satır eşleşmedi?" sorusunun cevabı, sağ taraftan gelen bir
sütunun `isna()` sayısıdır: `how='left'` ile birleştirdiğinde, sağda karşılığı olmayan
satırlarda sağdan gelen bütün sütunlar `NaN` olur.

**Tuzak 3 — anahtar tipi/yazımı farklı**: bir tabloda anahtar sayı (`101`), diğerinde
metin (`"101"`) ise, ya da birinde sonda boşluk (`"C01 "`) varsa hiçbir satır eşleşmez,
hata da almazsın. Birleştirmeden önce iki anahtarı da `.astype(str).str.strip()` ile aynı
biçime getirmek bu sorunu önler.
""",
        ornek="""siparis = pd.DataFrame({"musteri_id": ["A1", "A2", "A3"], "tutar": [100, 200, 50]})
musteri = pd.DataFrame({"musteri_id": ["A1", "A2"], "sehir": ["X", "Y"]})
m = siparis.merge(musteri, on="musteri_id", how="left")
print(int(m["sehir"].isna().sum()))    # -> 1   (A3 için eşleşme yok)""",
        ornek_dili="python",
        soru="`df`'i `musteriler_kucuk` ile `musteri_id` üzerinden `how='left'` birleştir. Müşteri tablosunda karşılığı bulunamayan (`ad` sütunu boş kalan) sipariş satırı sayısını `result`'a yaz.",
        beklenen="result = 1",
        ipucu="merge sonrası m['ad'].isna().sum() eşleşmeyen satırları sayar.",
        cozum="m = df.merge(musteriler_kucuk, on='musteri_id', how='left')\nresult = int(m['ad'].isna().sum())",
        tablo="siparisler",
    ),
    Soru(
        id="b11-s03",
        gun=11,
        tur="sql",
        kavram="INNER JOIN ile satır kaybı",
        anlatim="""
**Tuzak 2 — tekrar eden anahtar satırları çoğaltır**: arama tablosunda bir anahtar iki kez
geçerse, o anahtara sahip her satır sessizce ikiye katlanır. pandas'ta korunma yolu
`validate="many_to_one"` yazmaktır; ihlal varsa pandas hata fırlatır. SQL'in karşılığı
**INNER JOIN**'dür: yalnızca her iki tabloda da anahtarı bulunan satırları tutar — soldaki
tabloda eşi olmayan bir satır, hiçbir uyarı vermeden sonuçtan düşer.
""",
        ornek="""-- Genel kalıp: iki tabloyu ortak anahtar üzerinden birleştir, yalnızca eşleşenleri say
SELECT COUNT(*) AS toplam
FROM tablo_a a
INNER JOIN tablo_b b ON a.anahtar = b.anahtar;""",
        ornek_dili="sql",
        soru=(
            "`siparisler` tablosunu `musteriler_kucuk` ile `musteri_id` üzerinden INNER JOIN yap. "
            "Sonuçtaki satır sayısını `toplam` adıyla getir."
        ),
        beklenen="1 satır, 1 sütun (toplam). Değer 9 olmalı (C06'nın siparişi musteriler_kucuk'ta eşleşmediği için düşer).",
        ipucu="INNER JOIN yalnızca her iki tarafta da anahtarı olan satırları tutar.",
        cozum=(
            "SELECT COUNT(*) AS toplam FROM siparisler s "
            "INNER JOIN musteriler_kucuk m ON s.musteri_id = m.musteri_id;"
        ),
        tablo="siparisler",
    ),
]
