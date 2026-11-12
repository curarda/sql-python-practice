"""Bölüm 11: Tabloları birleştirme — merge ve concat."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=11,
    baslik="Tabloları birleştirme: merge ve concat",
    anlatim="""
Şirket verisi hiçbir zaman tek tabloda durmaz. İki tabloyu ortak bir sütun (anahtar, key)
üzerinden yan yana getirmek **merge** (Excel'de DÜŞEYARA/VLOOKUP, SQL'de JOIN), aynı
yapıdaki tabloları alt alta eklemek **concat**'tır.

`musteriler_kucuk` tablosunda `C06` yok (siparişlerde var), `C07` var (siparişlerde yok) —
gerçek veride bu uyumsuzluk her zaman vardır. `how` parametresi eşleşmeyen satırlara ne
olacağını belirler: `"left"` (soldaki hepsi, en sık kullanılan), `"inner"` (sadece
eşleşenler), `"right"`, `"outer"` (her ikisi).

**Tuzak 1 — eşleşmeyen satırlar sessizce kaybolur**: `left` ile birleştirip sonra
`groupby("segment")` yaparsan, segmenti olmayan (NaN) satırlar varsayılan olarak
**atılır**. `groupby("segment", dropna=False)` yazmazsan toplam ciro gerçekte olduğundan
düşük çıkar.

**Tuzak 2 — tekrar eden anahtar satırları çoğaltır**: arama tablosunda bir anahtar iki kez
geçerse, o anahtara sahip her satır ikiye katlanır — hata vermeden. Korunma:
`validate="many_to_one"` yaz; ihlal varsa pandas hata fırlatır.

**Tuzak 3 — anahtar tipi/yazımı farklı**: biri sayı biri metin, ya da sonda boşluk varsa
hiçbir satır eşleşmez; birleştirmeden önce `.astype(str).str.strip()` ile eşitle.
""",
    ornek="""m = df.merge(musteriler_kucuk, on="musteri_id", how="left")
print(m.groupby("segment", dropna=False)["ciro"].sum())
# -> NaN (C06) 6500, Gold 5230, Silver 4500, Bronze 1900""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı rakam",
            aciklama="dropna=False yazmazsan, cironun %35,9'u (6.500 TL'lik C06 siparişi) raporda hiç görünmeden kaybolur.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b11-s01",
        gun=11,
        tur="python",
        kavram="LEFT JOIN ve dropna=False",
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
