"""SQL parkuru — Bölüm 22: SQL toplulaştırma."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=22,
    baslik="SQL toplulaştırma",
    anlatim=(
        "Bu bölümde çok satırı tek sayıya indiren fonksiyonları (COUNT, SUM, AVG), "
        "satırları gruplara ayırmayı (GROUP BY), grupları filtrelemeyi (HAVING) ve "
        "koşullu toplamayı (CASE WHEN) öğreneceksin — raporların çoğu bunlardan çıkar."
    ),
    metrikler=[
        Metrik(
            baslik="Dikkat",
            aciklama="WHERE, gruplamadan ÖNCE satırları filtreler; HAVING, gruplamadan SONRA grupları filtreler. WHERE içinde COUNT/SUM kullanamazsın, HAVING içinde kullanabilirsin.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b22-s01",
        gun=22,
        tur="sql",
        kavram="COUNT, SUM, AVG",
        anlatim="""
Toplulaştırma fonksiyonları birden fazla satırı **tek bir değere** indirir: `COUNT(*)`
satır sayar, `SUM(sütun)` toplar, `AVG(sütun)` ortalama alır (`MIN`/`MAX` en küçük/büyük).
Bunları aynı `SELECT` içinde birden fazla yazabilirsin; sonuç tek bir satır olur.
`ROUND(sayi, n)` bir sayıyı n ondalık basamağa yuvarlar.
""",
        ornek="""SELECT COUNT(*) AS musteri_sayisi, ROUND(AVG(kayit_yili), 1) AS ortalama_yil
FROM musteriler_kucuk;""",
        ornek_dili="sql",
        soru="`siparisler` tablosunda toplam sipariş sayısını (`toplam_siparis`) ve ortalama `birim_fiyat`ı (`ortalama_fiyat`, 1 ondalık) getir.",
        beklenen="1 satır, 2 sütun: toplam_siparis = 10, ortalama_fiyat = 1445.0",
        ipucu="SELECT COUNT(*) AS toplam_siparis, ROUND(AVG(birim_fiyat), 1) AS ortalama_fiyat FROM siparisler;",
        cozum="SELECT COUNT(*) AS toplam_siparis, ROUND(AVG(birim_fiyat), 1) AS ortalama_fiyat FROM siparisler;",
    ),
    Soru(
        id="b22-s02",
        gun=22,
        tur="sql",
        kavram="GROUP BY",
        anlatim="""
`GROUP BY sütun`, tabloyu o sütunun her farklı değeri için ayrı bir gruba böler ve her
grup için **bir satır** döner. `SELECT` içindeki toplulaştırma olmayan her sütun, `GROUP
BY`'da da geçmelidir — "her grup için bu değer zaten tek" olmalı. `ORDER BY`, toplulaştırma
sonucuna göre de sıralayabilir (alias'ı kullanabilirsin).
""",
        ornek="""SELECT segment, COUNT(*) AS musteri_sayisi
FROM musteriler_kucuk GROUP BY segment ORDER BY musteri_sayisi DESC;""",
        ornek_dili="sql",
        soru="`siparisler` tablosunda kategori bazında sipariş sayısını (`adet_sayisi`) getir; `adet_sayisi`'na göre azalan sırala.",
        beklenen="3 satır: Elektronik (5), Giyim (3), Kitap (2) — azalan sırada.",
        ipucu="SELECT kategori, COUNT(*) AS adet_sayisi FROM siparisler GROUP BY kategori ORDER BY adet_sayisi DESC;",
        cozum="SELECT kategori, COUNT(*) AS adet_sayisi FROM siparisler GROUP BY kategori ORDER BY adet_sayisi DESC;",
        sirali=True,
    ),
    Soru(
        id="b22-s03",
        gun=22,
        tur="sql",
        kavram="HAVING",
        anlatim="""
`HAVING koşul`, `GROUP BY`'dan **sonra**, gruplar üzerinde filtre uygular — `WHERE` grup
oluşmadan önce tek tek satırları, `HAVING` gruplandıktan sonra grupların kendisini (ör.
grup toplamını) filtreler. Bu yüzden `HAVING SUM(x) > 100` yazılabilir ama aynı şeyi
`WHERE` içinde yazamazsın.
""",
        ornek="""SELECT segment, COUNT(*) AS adet
FROM musteriler_kucuk GROUP BY segment HAVING COUNT(*) >= 2;
-- yalnızca 2 ve üzeri müşterisi olan segmentler""",
        ornek_dili="sql",
        soru="`siparisler` tablosunda şehir bazında toplam ciroyu (`adet * birim_fiyat` toplamı, adı `toplam_ciro`) hesapla; yalnızca `toplam_ciro`'su 2000'den büyük olan şehirleri getir.",
        beklenen="3 satır: Ankara (9800), İstanbul (4290), İzmir (2140) — Bursa (1900) elenir.",
        ipucu="GROUP BY sehir yap, HAVING SUM(adet * birim_fiyat) > 2000 ekle.",
        cozum="SELECT sehir, SUM(adet * birim_fiyat) AS toplam_ciro FROM siparisler GROUP BY sehir HAVING SUM(adet * birim_fiyat) > 2000;",
    ),
    Soru(
        id="b22-s04",
        gun=22,
        tur="sql",
        kavram="CASE WHEN ve koşullu toplama",
        anlatim="""
`CASE WHEN koşul THEN deger ELSE deger2 END`, SQL'in if/else'idir; bir sütunu koşula göre
başka bir değere çevirir. Bunu bir toplulaştırma fonksiyonunun **içine** koyarsan
(`SUM(CASE WHEN ... THEN x ELSE 0 END)`), **koşullu toplama** elde edersin: yalnızca
koşulu sağlayan satırları topla, geri kalanı 0 say — tek bir `GROUP BY` yazmadan, birden
çok kategoriyi yan yana sütun olarak raporlayabilirsin.
""",
        ornek="""SELECT
  SUM(CASE WHEN segment = 'Gold' THEN 1 ELSE 0 END) AS gold_sayisi,
  SUM(CASE WHEN segment != 'Gold' THEN 1 ELSE 0 END) AS diger_sayisi
FROM musteriler_kucuk;""",
        ornek_dili="sql",
        soru=(
            "`siparisler` tablosunda kategori'si 'Elektronik' olan siparişlerin toplam cirosunu (`adet * birim_fiyat`, "
            "CASE WHEN ile, adı `elektronik_cirosu`) ve diğer kategorilerin toplam cirosunu (adı `diger_cirosu`) "
            "**tek satırda** getir."
        ),
        beklenen="1 satır, 2 sütun: elektronik_cirosu = 11050, diger_cirosu = 7080.",
        ipucu="SUM(CASE WHEN kategori = 'Elektronik' THEN adet * birim_fiyat ELSE 0 END) AS elektronik_cirosu, aynı mantıkla diğeri için != kullan.",
        cozum=(
            "SELECT SUM(CASE WHEN kategori = 'Elektronik' THEN adet * birim_fiyat ELSE 0 END) AS elektronik_cirosu, "
            "SUM(CASE WHEN kategori != 'Elektronik' THEN adet * birim_fiyat ELSE 0 END) AS diger_cirosu FROM siparisler;"
        ),
    ),
    Soru(
        id="b22-s05",
        gun=22,
        tur="sql",
        kavram="COUNT(DISTINCT ...)",
        anlatim="""
`COUNT(DISTINCT sütun)`, o sütundaki **farklı** değerlerin sayısını verir — aynı müşterinin
birden fazla siparişi varsa `COUNT(*)` sipariş sayısını, `COUNT(DISTINCT musteri_id)` ise
kaç **farklı** müşteri olduğunu söyler. Bu ikisinin farklı çıkması, bazı müşterilerin
birden fazla sipariş verdiğinin işaretidir.
""",
        ornek="""SELECT COUNT(*) AS satir_sayisi, COUNT(DISTINCT segment) AS farkli_segment
FROM musteriler_kucuk;""",
        ornek_dili="sql",
        soru="`siparisler` tablosunda kaç farklı müşterinin (`musteri_id`) sipariş verdiğini (`musteri_sayisi`) getir.",
        beklenen="1 satır, 1 sütun: musteri_sayisi = 6 (10 sipariş var ama 6 farklı müşteriden).",
        ipucu="SELECT COUNT(DISTINCT musteri_id) AS musteri_sayisi FROM siparisler;",
        cozum="SELECT COUNT(DISTINCT musteri_id) AS musteri_sayisi FROM siparisler;",
    ),
]
