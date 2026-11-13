"""SQL parkuru — Bölüm 21: SQL temelleri.

Python parkurundaki Bölüm 15 pencere fonksiyonlarıyla başladığı için, SQL'i hiç
bilmeyen biri için buraya iki temel bölüm ekledim: SELECT'in yapı taşları (bu dosya)
ve toplulaştırma (gun22.py). İkisi de aynı `siparisler`/`musteriler_kucuk` tablolarını
kullanır, böylece SQL ve Python parkurları aynı veriye farklı araçlarla bakar.
"""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=21,
    baslik="SQL temelleri",
    anlatim=(
        "SQL parkuruna hoş geldin. Bu bölümde bir sorgunun yapı taşlarını öğreneceksin: "
        "SELECT/FROM/ORDER BY/LIMIT, WHERE ile filtreleme, DISTINCT/IN/BETWEEN, LIKE ve "
        "COALESCE. Python bilmene gerek yok; SQL kendi başına, tablo sorgulamak için "
        "tasarlanmış ayrı bir dildir."
    ),
    metrikler=[
        Metrik(
            baslik="Sorgunun okunuş sırası",
            aciklama="Yazdığın sıra SELECT → FROM → WHERE → GROUP BY → ORDER BY → LIMIT'tir, ama veritabanı sorguyu önce FROM/WHERE ile çalıştırır, SELECT'i en son uygular.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b21-s01",
        gun=21,
        tur="sql",
        kavram="SELECT, ORDER BY, LIMIT",
        anlatim="""
Bir SQL sorgusu dört temel parçadan oluşur: `SELECT` hangi sütunların geleceğini söyler
(`*` hepsi demektir), `FROM` hangi tablodan okunacağını, `ORDER BY sütun` sonucu sıralar
(`DESC` azalan, yazmazsan artan), `LIMIT n` yalnızca ilk n satırı getirir. Her satırın
sonu noktalı virgülle (`;`) bitirilir (zorunlu değil ama alışkanlık iyidir).
""",
        ornek="""SELECT ad, segment FROM musteriler_kucuk ORDER BY kayit_yili LIMIT 3;
-- en eski kayıtlı 3 müşterinin adı ve segmenti""",
        ornek_dili="sql",
        soru="`siparisler` tablosunda `siparis_id`'ye göre artan sırayla ilk 4 siparişin `urun` ve `birim_fiyat` sütunlarını getir.",
        beklenen="4 satır (Kulaklık, Mont, Klavye, Roman), siparis_id artan sırada.",
        ipucu="SELECT urun, birim_fiyat FROM siparisler ORDER BY siparis_id LIMIT 4;",
        cozum="SELECT urun, birim_fiyat FROM siparisler ORDER BY siparis_id LIMIT 4;",
        sirali=True,
    ),
    Soru(
        id="b21-s02",
        gun=21,
        tur="sql",
        kavram="WHERE ile filtreleme",
        anlatim="""
`WHERE koşul`, yalnızca koşulu sağlayan satırları getirir. Karşılaştırma operatörleri
`= != > < >= <=` metinde ve SQL'de aynıdır. Birden fazla koşulu `AND` (ikisi de doğru
olmalı) ya da `OR` (biri doğru olsa yeter) ile birleştirirsin.
""",
        ornek="""SELECT ad FROM musteriler_kucuk WHERE kayit_yili >= 2024;
-- 2024 ve sonrasında kayıt olan müşteriler""",
        ornek_dili="sql",
        soru="`siparisler` tablosunda `birim_fiyat`ı 1000'den büyük olan siparişlerin `urun` ve `birim_fiyat` sütunlarını getir.",
        beklenen="4 satır: Mont, Klavye, Ayakkabı, Monitör.",
        ipucu="SELECT urun, birim_fiyat FROM siparisler WHERE birim_fiyat > 1000;",
        cozum="SELECT urun, birim_fiyat FROM siparisler WHERE birim_fiyat > 1000;",
    ),
    Soru(
        id="b21-s03",
        gun=21,
        tur="sql",
        kavram="DISTINCT, IN, BETWEEN",
        anlatim="""
`DISTINCT`, sonuçtaki tekrar eden satırları tek satıra indirir. `IN (a, b, c)`, bir
sütunun listedeki değerlerden birine eşit olup olmadığını kontrol eder (`kategori IN
('Elektronik', 'Giyim')`, `kategori = 'Elektronik' OR kategori = 'Giyim'` yazmaktan
kısadır). `BETWEEN a AND b`, bir sayının iki uç **dahil** aralıkta olup olmadığına bakar.
""",
        ornek="""SELECT DISTINCT segment FROM musteriler_kucuk WHERE kayit_yili BETWEEN 2023 AND 2025;
-- 2023-2025 arası kayıt olan müşterilerin tekrarsız segmentleri""",
        ornek_dili="sql",
        soru=(
            "`siparisler` tablosunda `musteri_id`'si `('C01', 'C02', 'C03')` listesinde (IN) olan VE `adet`'i "
            "1 ile 2 arasında (BETWEEN, dahil) olan siparişlerin tekrarsız (DISTINCT) `kategori` değerlerini getir."
        ),
        beklenen="3 satır: Elektronik, Giyim, Kitap (DISTINCT olmadan 5 satır gelirdi, Elektronik 3 kez tekrarlardı).",
        ipucu="WHERE musteri_id IN ('C01','C02','C03') AND adet BETWEEN 1 AND 2; başına SELECT DISTINCT kategori ekle.",
        cozum="SELECT DISTINCT kategori FROM siparisler WHERE musteri_id IN ('C01', 'C02', 'C03') AND adet BETWEEN 1 AND 2;",
    ),
    Soru(
        id="b21-s04",
        gun=21,
        tur="sql",
        kavram="LIKE ile desen eşleştirme",
        anlatim="""
`LIKE 'desen'`, bir metnin belli bir kalıba uyup uymadığını kontrol eder. `%` herhangi bir
uzunlukta (sıfır dahil) karakter dizisi yerine geçer: `'M%'` M ile başlayan, `'%a'` a ile
biten, `'%kit%'` içinde "kit" geçen her şeyi yakalar. `_` tek bir karakter yerine geçer.
""",
        ornek="""SELECT ad FROM musteriler_kucuk WHERE ad LIKE '%e%';
-- adında 'e' harfi geçen müşteriler""",
        ornek_dili="sql",
        soru="`siparisler` tablosunda `urun` adı 'M' ile başlayan siparişlerin `urun` ve `birim_fiyat` sütunlarını getir.",
        beklenen="3 satır: Mont, Mouse, Monitör.",
        ipucu="WHERE urun LIKE 'M%' — % herhangi bir devamı kabul eder.",
        cozum="SELECT urun, birim_fiyat FROM siparisler WHERE urun LIKE 'M%';",
    ),
    Soru(
        id="b21-s05",
        gun=21,
        tur="sql",
        kavram="COALESCE ile boş değer doldurma",
        anlatim="""
`COALESCE(a, b)`, `a` boş (NULL) değilse `a`'yı, boşsa `b`'yi döndürür — bir sütundaki
eksik değerleri raporda "boş" yerine bir sayı/metinle göstermenin yoludur. Eksik değer
kontrolü için `=` değil `IS NULL` / `IS NOT NULL` kullanılır; SQL'de `NULL = NULL`
**yanlış** sonucunu verir (bilinmeyenle bilinmeyen karşılaştırılamaz).
""",
        ornek="""SELECT ad, COALESCE(segment, 'Bilinmiyor') AS segment_duzeltilmis FROM musteriler_kucuk;
-- segment boşsa 'Bilinmiyor' yazar (bu tabloda hiçbiri boş değil, hepsi olduğu gibi kalır)""",
        ornek_dili="sql",
        soru=(
            "`vaka_siparisler` tablosunda `tutar` boşsa (NULL) 0 kabul et (`COALESCE`, adı `tutar_duzeltilmis`). "
            "Düzeltilmiş tutara göre azalan sırada ilk 5 siparişin `siparis_no` ve `tutar_duzeltilmis` sütunlarını getir."
        ),
        beklenen="5 satır, tutar_duzeltilmis azalan sırada (en yüksek tutarlı 5 sipariş; en yüksek değerler zaten dolu olduğu için COALESCE burada devreye girmez ama sözdizimi doğru olmalı).",
        ipucu="SELECT siparis_no, COALESCE(tutar, 0) AS tutar_duzeltilmis FROM vaka_siparisler ORDER BY tutar_duzeltilmis DESC LIMIT 5;",
        cozum="SELECT siparis_no, COALESCE(tutar, 0) AS tutar_duzeltilmis FROM vaka_siparisler ORDER BY tutar_duzeltilmis DESC LIMIT 5;",
        tablo="vaka_siparisler",
        sirali=True,
    ),
]
