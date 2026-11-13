"""Bölüm 17: API ve JSON ile veri çekme."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=17,
    baslik="API ve JSON ile veri çekme",
    anlatim=(
        "Bazı veriler dosyada ya da veritabanında değil, bir API'nin arkasındadır. Bu "
        "bölümde JSON'u okumayı, iç içe yapıları `json_normalize` ile düzleştirmeyi ve "
        "`requests` ile istek atmanın temel kurallarını öğreneceksin."
    ),
    metrikler=[
        Metrik(
            baslik="Dikkat",
            aciklama="requests.get çağrısına her zaman timeout= ekle; sunucu cevap vermezse kodun sonsuza kadar beklemesin.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b17-s01",
        gun=17,
        tur="python",
        kavram="json.loads ile iç içe veriye erişmek",
        anlatim="""
Bazı veriler dosyada ya da şirket veritabanında değil, bir **API**'nin (Application
Programming Interface) arkasındadır: döviz kuru, hava durumu, bir CRM'in müşteri listesi.
Cevap neredeyse her zaman **JSON** biçimindedir — Python'daki sözlük ve listelere çok
benzeyen, iç içe yapılar taşıyabilen bir metin biçimidir. `json.loads(metin)` bir JSON
metnini Python sözlüğüne/listesine çevirir; ondan sonra normal sözlük/liste erişimiyle
(`veri["anahtar"][0]`) istediğin değere ulaşırsın.
""",
        ornek="""import json
metin = '{"sehir": "Ankara", "sicaklik": [{"saat": 9, "derece": 12}, {"saat": 15, "derece": 18}]}'
veri = json.loads(metin)
ogle_derece = [s["derece"] for s in veri["sicaklik"] if s["saat"] == 15][0]
print(ogle_derece)    # -> 18""",
        ornek_dili="python",
        soru="`KUR_JSON_METNI` değişkenini `json.loads` ile Python nesnesine çevir. `kurlar` listesindeki 'EUR' kaydının `satis` değerini `result`'a yaz.",
        beklenen="result = 48.55",
        ipucu="json.loads(KUR_JSON_METNI)['kurlar'] bir liste döndürür; kod alanı 'EUR' olan elemanı bul.",
        cozum=(
            "veri = json.loads(KUR_JSON_METNI)\n"
            "eur = [k for k in veri['kurlar'] if k['kod'] == 'EUR'][0]\n"
            "result = eur['satis']"
        ),
    ),
    Soru(
        id="b17-s02",
        gun=17,
        tur="python",
        kavram="json_normalize: sipariş başına bir satır",
        anlatim="""
İç içe JSON'u düzleştirmek için `pd.json_normalize` kullanılır. `pd.json_normalize(kayitlar,
sep="_")`, her kaydı tek bir satır yapar; iç içe sözlükler (`{"musteri": {"ad": ...}}`)
`musteri_ad` gibi tek bir sütuna açılır. Bir listeyi (ör. bir siparişteki ürünler) bu
şekilde düzleştirmeye çalışırsan, o sütun liste olarak kalır — ayrı ele alınması gerekir
(bir sonraki noktada).
""",
        ornek="""kayitlar = [
    {"siparis_no": 501, "musteri": {"ad": "Mehmet", "sehir": "Ankara"}, "urunler": [{"ad": "Defter", "fiyat": 40}]},
    {"siparis_no": 502, "musteri": {"ad": "Zeynep", "sehir": "Bursa"}, "urunler": [{"ad": "Kalem", "fiyat": 5}]},
]
print(pd.json_normalize(kayitlar, sep="_").drop(columns="urunler"))
#    siparis_no musteri_ad musteri_sehir
#           501     Mehmet        Ankara
#           502     Zeynep         Bursa""",
        ornek_dili="python",
        soru="`API_ORNEGI` listesini `pd.json_normalize(..., sep='_')` ile düzleştir, `urunler` sütununu çıkar (`drop`). Sonucu `result`'a yaz.",
        beklenen="2 satır, 3 sütun: id, musteri_ad, musteri_sehir.",
        ipucu="pd.json_normalize(API_ORNEGI, sep='_').drop(columns='urunler')",
        cozum="result = pd.json_normalize(API_ORNEGI, sep='_').drop(columns='urunler')",
    ),
    Soru(
        id="b17-s03",
        gun=17,
        tur="python",
        kavram="json_normalize: ürün başına bir satır (record_path)",
        anlatim="""
`pd.json_normalize(kayitlar, record_path="liste_sutunu", meta=["ust_alan", [...]])`, bir
kayıt içindeki **listeyi** (bire-çok ilişki, ör. bir siparişte birden çok ürün) ayrı
satırlara açar; `meta` ile üst bilgileri (sipariş no, müşteri adı gibi) her satıra taşır.
Hangisini seçeceğin sorduğun soruya bağlıdır: sipariş sayısı mı, ürün bazında ciro mu?

`requests.get(adres, params=..., timeout=10)` bir HTTP isteği gönderir;
`cevap.raise_for_status()` 200 dışında bir durum kodunda hata fırlatır, `cevap.json()`
cevabı Python nesnesine çevirir. Kurumsal API'lerde üç gerçek: **kimlik doğrulama**
(anahtar ortam değişkeninden okunur, koda yazılmaz), **sayfalama** (binlerce kayıt sayfa
sayfa gelir, döngüyle gezilir) ve **sınırlar** (rate limit; sonucu bir dosyaya kaydedip
tekrar tekrar istek atmaktan kaçın).
""",
        ornek="""kayitlar = [
    {"siparis_no": 501, "musteri": {"ad": "Mehmet"}, "urunler": [{"ad": "Defter", "fiyat": 40}, {"ad": "Silgi", "fiyat": 8}]},
]
print(pd.json_normalize(kayitlar, record_path="urunler", meta=["siparis_no", ["musteri", "ad"]], record_prefix="urun_"))
#    urun_ad  urun_fiyat  siparis_no musteri.ad
#     Defter          40         501     Mehmet
#      Silgi           8         501     Mehmet""",
        ornek_dili="python",
        soru="`API_ORNEGI` içindeki `urunler` listesini `record_path` ile satırlara aç; her satırda `urun_ad`, `urun_fiyat`, `id` ve müşterinin adı (`musteri.ad`) olsun. Sonucu `result`'a yaz.",
        beklenen="3 satır (toplam ürün sayısı kadar).",
        ipucu='pd.json_normalize(API_ORNEGI, record_path="urunler", meta=["id", ["musteri", "ad"]], record_prefix="urun_")',
        cozum=(
            "result = pd.json_normalize(\n"
            "    API_ORNEGI, record_path='urunler', meta=['id', ['musteri', 'ad']], record_prefix='urun_'\n"
            ")"
        ),
    ),
]
