"""Bölüm 15: SQL ve Python."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=15,
    baslik="SQL ve Python",
    anlatim=(
        "Şirket verisi genelde veritabanında durur. Bu bölümde SQL ile pandas'ı birlikte "
        "kullanmayı, LEFT JOIN'in NULL grupları nasıl tuttuğunu, pencere fonksiyonlarını ve "
        "SQL↔pandas karşılıklarını öğreneceksin."
    ),
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
        anlatim="""
Şirket verisi genelde veritabanında durur (PostgreSQL, MySQL, BigQuery...). Tipik iş akışı:
veriyi SQL ile çek ve mümkünse orada filtrele/özetle, sonucu pandas'a al, kalan analizi ve
grafiği Python'da yap — 500 milyon satırı indirmek yerine veritabanında özetleyip 50 satır
indirmek, saatle saniye arasındaki farktır. `pd.read_sql(sorgu, baglanti)` bir SQL sorgusunu
doğrudan DataFrame'e çevirir.

SQL'de gruplama pandas'taki `groupby` ile aynı mantıkla çalışır: `GROUP BY sütun` her farklı
değer için bir satır döner, `ORDER BY` sonucu sıralar.
""",
        ornek="""SELECT segment, COUNT(*) AS musteri_sayisi
FROM musteriler_kucuk
GROUP BY segment
ORDER BY musteri_sayisi DESC;""",
        ornek_dili="sql",
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
        anlatim="""
**Parametreli sorgu**: bir değeri sorguya f-string ile yapıştırmak cazip gelir ama
yapılmamalı; değer içinde tırnak işareti varsa sorgu bozulur, kötü niyetli bir girdi SQL
injection'a yol açabilir. Doğru yol `?` yer tutucusu ve `params=(...)` kullanmaktır:
`pd.read_sql("SELECT * FROM t WHERE x = ?", con, params=(deger,))`.

**Önemli fark**: SQL'in `GROUP BY`'ı eşleşmeyen (NULL) satırları **ayrı bir grup** olarak
tutar; pandas'ın `groupby`'ı varsayılan olarak bu grubu atar (Bölüm 11). Aynı soruya iki
araçla bakıp farklı toplam görürsen, ilk bakılacak yer burasıdır.
""",
        ornek="""-- Genel kalıp: LEFT JOIN sonrası eşleşmeyenler NULL grubu olarak kalır, ekstra kod gerekmez
SELECT m.sehir AS sehir, COUNT(*) AS adet
FROM siparis_tablosu s
LEFT JOIN musteri_tablosu m ON s.musteri_id = m.musteri_id
GROUP BY m.sehir;""",
        ornek_dili="sql",
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
        anlatim="""
**Pencere fonksiyonu** (`ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`), grup
sonucunu satır sayısını **değiştirmeden** her satıra yazar — pandas'taki `transform`'un
SQL karşılığıdır (Bölüm 10). `PARTITION BY` "her grup için ayrı say" demektir, `ORDER BY`
grup içindeki sırayı belirler. Mülakatlarda en sık sorulan SQL konularından biridir.
""",
        ornek="""SELECT kategori, urun, birim_fiyat,
       ROW_NUMBER() OVER (PARTITION BY kategori ORDER BY birim_fiyat DESC) AS sira
FROM siparisler
WHERE kategori = 'Giyim';
-- her kategori içinde fiyata göre en pahalıdan başlayarak 1, 2, 3... numaralar""",
        ornek_dili="sql",
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
        anlatim="""
SQL ↔ pandas sözlüğü (en sık kullanılanlar):

| SQL | pandas |
|---|---|
| `WHERE x IN (...)` | `t[t["x"].isin([...])]` |
| `WHERE x IS NULL` | `t[t["x"].isna()]` |
| `WHERE urun LIKE '%Kit%'` | `t[t["urun"].str.contains("Kit")]` |
| `CASE WHEN x>5 THEN 'A' ELSE 'B' END` | `np.where(t["x"]>5, "A", "B")` |

Birden fazla koşulu `AND`/`OR` ile birleştirebilirsin; tarih sütunu metin olarak saklansa
bile `'2026-02-01'` gibi ISO biçimli bir tarihle karşılaştırma genelde doğru çalışır,
çünkü ISO tarihler alfabetik sırayla da kronolojik sıradadır.
""",
        ornek="""SELECT urun, birim_fiyat
FROM siparisler
WHERE adet >= 3 AND sehir = 'İstanbul';""",
        ornek_dili="sql",
        soru="`siparisler` tablosunda `tarih` 2026-02-01 veya sonrası olan ve `kategori`si 'Elektronik' olan siparişlerin `urun` ve `birim_fiyat` sütunlarını getir.",
        beklenen="3 satır: Mouse, Monitör, Şarj Aleti.",
        ipucu="WHERE tarih >= '2026-02-01' AND kategori = 'Elektronik'.",
        cozum="SELECT urun, birim_fiyat FROM siparisler WHERE tarih >= '2026-02-01' AND kategori = 'Elektronik';",
    ),
]
