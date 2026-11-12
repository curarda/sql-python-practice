"""Bölüm 15: SQL ve Python."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=15,
    baslik="SQL ve Python",
    anlatim="""
Şirket verisi genelde veritabanında durur (PostgreSQL, MySQL, BigQuery...). Tipik iş akışı:
veriyi SQL ile çek ve mümkünse orada filtrele/özetle, sonucu pandas'a al, kalan analizi ve
grafiği Python'da yap — 500 milyon satırı indirmek yerine veritabanında özetleyip 50 satır
indirmek, saatle saniye arasındaki farktır.

`pd.read_sql(sorgu, baglanti)` bir SQL sorgusunu doğrudan DataFrame'e çevirir. **Parametreli
sorgu**: bir değeri sorguya f-string ile yapıştırma (SQL injection riski); `?` yer tutucusu
ve `params=(...)` kullan.

**Pencere fonksiyonu** (`ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`), grup sonucunu
satır sayısını değiştirmeden her satıra yazar — pandas'taki `transform`'un SQL karşılığıdır.

SQL ↔ pandas sözlüğü (en sık kullanılanlar):

| SQL | pandas |
|---|---|
| `WHERE x IN (...)` | `t[t["x"].isin([...])]` |
| `WHERE x IS NULL` | `t[t["x"].isna()]` |
| `GROUP BY g, SUM(x)` | `t.groupby("g")["x"].sum()` |
| `LEFT JOIN ON t.k=m.k` | `t.merge(m, on="k", how="left")` |
| `CASE WHEN x>5 THEN 'A' ELSE 'B' END` | `np.where(t["x"]>5, "A", "B")` |
| `ROW_NUMBER() OVER (PARTITION BY g ORDER BY d)` | `t.sort_values("d").groupby("g").cumcount()+1` |

**Önemli fark**: SQL'in `GROUP BY`'ı eşleşmeyen (NULL) grubu ayrı bir satır olarak tutar;
pandas'ın `groupby`'ı varsayılan olarak atar (Bölüm 11).
""",
    ornek="""SELECT musteri_id, tarih, adet * birim_fiyat AS ciro,
       ROW_NUMBER() OVER (PARTITION BY musteri_id ORDER BY tarih) AS siparis_sirasi
FROM siparisler
WHERE musteri_id IN ('C01', 'C02');""",
    ornek_dili="sql",
    metrikler=[
        Metrik(
            baslik="Dikkat",
            aciklama="Kullanıcı girdisini asla f-string ile sorguya yapıştırma; ? yer tutucusu ve params kullan (SQL injection).",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b15-s01",
        gun=15,
        tur="sql",
        kavram="read_sql: GROUP BY ve ORDER BY",
        soru="`siparisler` tablosunda şehir bazında sipariş sayısını (`siparis`) ve ciroyu (`adet * birim_fiyat` toplamı, `ciro`) getir; `ciro`'ya göre azalan sırala.",
        beklenen="4 satır (Ankara, İstanbul, İzmir, Bursa), ciro azalan sırada (Ankara 9800 en üstte).",
        ipucu="SUM(adet * birim_fiyat) AS ciro, GROUP BY sehir, ORDER BY ciro DESC.",
        cozum=(
            "SELECT sehir, COUNT(*) AS siparis, SUM(adet * birim_fiyat) AS ciro "
            "FROM siparisler GROUP BY sehir ORDER BY ciro DESC;"
        ),
        sirali=True,
    ),
    Soru(
        id="b15-s02",
        gun=15,
        tur="sql",
        kavram="LEFT JOIN: eşleşmeyen grup",
        soru=(
            "`siparisler`'i `musteriler_kucuk` ile `musteri_id` üzerinden LEFT JOIN yap. Segment bazında "
            "ciro toplamını getir (`segment`, `ciro`); eşleşmeyenler de (NULL segment) ayrı bir satır "
            "olarak görünsün. `ciro`'ya göre azalan sırala."
        ),
        beklenen="4 satır: NULL (6500), Gold (5230), Silver (4500), Bronze (1900).",
        ipucu="SQL'in GROUP BY'ı NULL'ı pandas'tan farklı olarak otomatik ayrı bir grup sayar; ekstra bir şey yazmana gerek yok.",
        cozum=(
            "SELECT m.segment AS segment, SUM(s.adet * s.birim_fiyat) AS ciro "
            "FROM siparisler s LEFT JOIN musteriler_kucuk m ON s.musteri_id = m.musteri_id "
            "GROUP BY m.segment ORDER BY ciro DESC;"
        ),
        sirali=True,
    ),
    Soru(
        id="b15-s03",
        gun=15,
        tur="sql",
        kavram="Pencere fonksiyonu: ROW_NUMBER",
        soru=(
            "`siparisler` tablosunda, yalnızca `musteri_id` 'C01' veya 'C02' olan satırlar için "
            "`musteri_id`, `tarih`, ciro (`adet * birim_fiyat`, adı `ciro`) ve her müşterinin kendi "
            "içindeki sipariş sırasını (`tarih`'e göre artan, adı `siparis_sirasi`) getir."
        ),
        beklenen="5 satır (C01'den 3, C02'den 2), her müşteri için 1'den başlayan bir sipariş sırası.",
        ipucu="ROW_NUMBER() OVER (PARTITION BY musteri_id ORDER BY tarih) AS siparis_sirasi.",
        cozum=(
            "SELECT musteri_id, tarih, adet * birim_fiyat AS ciro, "
            "ROW_NUMBER() OVER (PARTITION BY musteri_id ORDER BY tarih) AS siparis_sirasi "
            "FROM siparisler WHERE musteri_id IN ('C01', 'C02');"
        ),
    ),
    Soru(
        id="b15-s04",
        gun=15,
        tur="sql",
        kavram="Tarih ve kategori filtresi",
        soru="`siparisler` tablosunda `tarih` 2026-02-01 veya sonrası olan ve `kategori`si 'Elektronik' olan siparişlerin `urun` ve `birim_fiyat` sütunlarını getir.",
        beklenen="3 satır: Mouse, Monitör, Şarj Aleti.",
        ipucu="WHERE tarih >= '2026-02-01' AND kategori = 'Elektronik'.",
        cozum="SELECT urun, birim_fiyat FROM siparisler WHERE tarih >= '2026-02-01' AND kategori = 'Elektronik';",
    ),
]
