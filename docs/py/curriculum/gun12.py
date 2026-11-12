"""Bölüm 12: Tarih ve zaman serisi."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=12,
    baslik="Tarih ve zaman serisi",
    anlatim="""
Satış, trafik, kur gibi verilerin çoğu tarihlidir. Tarih metin olduğu sürece hiçbir tarih
aracı çalışmaz; önce çevirmen gerekir: `pd.to_datetime(df["tarih"])` (biçimi biliyorsan
`format="%d.%m.%Y"` ile açıkça yaz, `dayfirst=True` ile tahmin ettirme — Bölüm 9'daki uyarı).

`.dt` ile tarihin parçalarına ulaşırsın: `.dt.month`, `.dt.quarter`, `.dt.dayofweek`
(0=Pazartesi), `.dt.day_name()`, `.dt.to_period("M")`.

Tarihi **index** yapınca (`seri = df.set_index("tarih")["satis"]`) güçlü araçlar açılır:

- `resample("ME")`: günlüğü aya toplar/ortalar (frekans kodları: `D`, `W`, `ME` ay sonu,
  `QE` çeyrek, `YE` yıl). **Takvim etkisine dikkat**: aylık toplamları karşılaştırmadan
  önce gün sayısı farkını hesaba kat (`resample("ME").mean()` günlük ortalamaya eşittir).
- `pct_change()`: bir önceki döneme göre yüzde değişim. `shift(n)`: seriyi n adım kaydırır
  (yıllık karşılaştırma için `shift(12)`, haftalık için `shift(7)`).
- `rolling(7).mean()`: hareketli ortalama, gürültüyü düzleştirip trendi görünür kılar.
- `asfreq("D")`: eksik günleri (satış olmayan günler) tabloya sıfır/NaN olarak ekler;
  aksi hâlde günlük ortalama sadece satış olan günlerden hesaplanıp olduğundan yüksek çıkar.
""",
    ornek="""satis = df.set_index("tarih")["satis"]
aylik = satis.resample("ME").sum()
print(aylik.pct_change().mul(100).round(1))
# -> ocak NaN, şubat +4.0, mart +17.2 (bir önceki aya göre yüzde değişim)""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı rakam",
            aciklama="Hafta sonu ortalaması (172,7), hafta içinin (112,6) yaklaşık 1,5 katı. Tek bir 'günlük ortalama' iki ayrı gün tipini gizler.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b12-s01",
        gun=12,
        tur="python",
        kavram="resample: aylık toplam",
        soru="`gunluk_satis` tablosunu `tarih` index'li bir Series'e çevir (`satis` sütunu). Aylık toplamı (`resample('ME').sum()`), `{ay_no: toplam}` biçiminde bir sözlük olarak `result`'a yaz (ay_no: 1, 2, 3).",
        beklenen="result = {1: 3588.0, 2: 3732.0, 3: 4374.0}",
        ipucu="set_index('tarih')['satis'].resample('ME').sum(); sözlük anahtarı için .index.month kullan.",
        cozum=(
            "seri = gunluk_satis.set_index('tarih')['satis']\n"
            "aylik = seri.resample('ME').sum()\n"
            "result = {ay.month: deger for ay, deger in aylik.items()}"
        ),
        tablo="gunluk_satis",
    ),
    Soru(
        id="b12-s02",
        gun=12,
        tur="python",
        kavram="rolling: hareketli ortalama",
        soru="`gunluk_satis`'i tarih index'li Series yap. 7 günlük hareketli ortalamanın (`rolling(7).mean()`) son (en son tarihli) değerini, 1 ondalığa yuvarlanmış olarak `result`'a yaz.",
        beklenen="result = 146.0",
        ipucu="seri.rolling(7).mean().iloc[-1] serinin son değerini verir.",
        cozum="seri = gunluk_satis.set_index('tarih')['satis']\nresult = round(seri.rolling(7).mean().iloc[-1], 1)",
        tablo="gunluk_satis",
    ),
    Soru(
        id="b12-s03",
        gun=12,
        tur="python",
        kavram="Mevsimsellik: haftaiçi/haftasonu",
        soru="`gunluk_satis`'i tarih index'li Series yap. Hafta içi (Pazartesi-Cuma) ve hafta sonu günlerinin ayrı ayrı ortalama satışını, 1 ondalığa yuvarlanmış `(hafta_ici, hafta_sonu)` tuple'ı olarak `result`'a yaz.",
        beklenen="result = (112.6, 172.7)",
        ipucu="seri.index.dayofweek 0-4 hafta içi, 5-6 hafta sonudur.",
        cozum=(
            "seri = gunluk_satis.set_index('tarih')['satis']\n"
            "hafta_ici = round(seri[seri.index.dayofweek < 5].mean(), 1)\n"
            "hafta_sonu = round(seri[seri.index.dayofweek >= 5].mean(), 1)\n"
            "result = (hafta_ici, hafta_sonu)"
        ),
        tablo="gunluk_satis",
    ),
]
