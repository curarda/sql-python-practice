"""Bölüm 17: API ve JSON ile veri çekme."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=17,
    baslik="API ve JSON ile veri çekme",
    anlatim="""
Bazı veriler dosyada ya da şirket veritabanında değil, bir **API**'nin (Application
Programming Interface) arkasındadır: döviz kuru, hava durumu, bir CRM'in müşteri listesi.
Cevap neredeyse her zaman **JSON** biçimindedir — Python'daki sözlük ve listelere çok
benzeyen, iç içe yapılar taşıyabilen bir metin biçimi.

```
veri = json.loads(metin)          # JSON metni -> Python sözlüğü/listesi
pd.DataFrame(veri["kurlar"])      # sözlük listesi -> tablo
```

İç içe JSON'u düzleştirmek için `pd.json_normalize` kullanılır:

- `pd.json_normalize(kayitlar, sep="_")`: her kaydı tek bir satır yapar, iç içe sözlükler
  (`musteri.ad`) sütunlara açılır.
- `pd.json_normalize(kayitlar, record_path="urunler", meta=["id", ["musteri","ad"]])`: bir
  kayıt içindeki listeyi (bire-çok ilişki, ör. bir siparişte birden çok ürün) ayrı satırlara
  açar, üst bilgileri (id, müşteri adı) her satıra taşır.

`requests.get(adres, params=..., timeout=10)` bir HTTP isteği gönderir;
`cevap.raise_for_status()` 200 dışında bir durum kodunda hata fırlatır,
`cevap.json()` cevabı Python nesnesine çevirir. Kurumsal API'lerde üç gerçek: **kimlik
doğrulama** (anahtar, ortam değişkeninden okunur — koda yazılmaz), **sayfalama**
(binlerce kayıt sayfa sayfa gelir, döngüyle gezilir) ve **sınırlar** (rate limit; sonucu
bir dosyaya kaydedip tekrar tekrar istek atmaktan kaçın).
""",
    ornek="""siparisler = [
    {"id": 1, "musteri": {"ad": "Ayşe", "sehir": "İzmir"},
     "urunler": [{"ad": "Kulaklık", "fiyat": 750}, {"ad": "Kılıf", "fiyat": 120}]},
]
pd.json_normalize(siparisler, sep="_").drop(columns="urunler")
#    id musteri_ad musteri_sehir
#     1       Ayşe         İzmir""",
    ornek_dili="python",
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
