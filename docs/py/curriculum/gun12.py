"""Bölüm 12: Tarih ve zaman serisi."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=12,
    baslik="Tarih ve zaman serisi",
    anlatim=(
        "Satış, trafik, kur gibi verilerin çoğu tarihlidir. Bu bölümde tarihi doğru tipe "
        "çevirmeyi, aylık/haftalık özetlemeyi (resample), hareketli ortalamayı (rolling) ve "
        "haftaiçi/haftasonu örüntüsünü öğreneceksin."
    ),
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı gözlem",
            aciklama="Hafta sonu ortalaması genelde hafta içinin epey üzerindedir. Tek bir 'günlük ortalama' sayısı, iki farklı gün tipini (hafta içi/hafta sonu) birbirine karıştırıp gizleyebilir.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b12-s01",
        gun=12,
        tur="python",
        kavram="resample: aylık toplam",
        anlatim="""
Tarih metin olduğu sürece hiçbir tarih aracı çalışmaz; önce çevirmen gerekir:
`pd.to_datetime(df["tarih"])` (biçimi biliyorsan `format="%d.%m.%Y"` ile açıkça yaz,
`dayfirst=True` ile tahmin ettirme — Bölüm 9'daki uyarı geçerli). `.dt` ile tarihin
parçalarına ulaşırsın: `.dt.month`, `.dt.quarter`, `.dt.dayofweek` (0=Pazartesi).

Tarihi **index** yapınca (`seri = df.set_index("tarih")["satis"]`) güçlü araçlar açılır.
`resample("ME")`, günlük bir seriyi **aya toplar/ortalar** (frekans kodları: `D` gün, `W`
hafta, `ME` ay sonu, `QE` çeyrek, `YE` yıl). **Takvim etkisine dikkat**: 28 günlük Şubat ile
31 günlük Ocak'ın toplamlarını doğrudan karşılaştırmak yanıltır; `resample("ME").mean()`
günlük ortalamaya eşit olduğu için takvim etkisinden arınmıştır.
""",
        ornek="""gunler = pd.date_range("2026-01-01", "2026-01-10", freq="D")
seri = pd.Series([5, 6, 4, 7, 5, 6, 8, 5, 6, 7], index=gunler)
print(seri.resample("W").sum())    # haftalık toplam (W = hafta)""",
        ornek_dili="python",
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
        anlatim="""
Günlük veri gürültülüdür; **hareketli ortalama (rolling mean)**, her gün için son n günün
ortalamasını alarak bu dalgalanmayı düzleştirir ve trendi görünür kılar:
`seri.rolling(7).mean()`. İlk `n-1` değer `NaN` çıkar, çünkü pencere henüz dolmamıştır.
İlgili iki araç daha: `pct_change()` bir önceki döneme göre yüzde değişimi verir;
`shift(n)` seriyi n adım kaydırır (yıllık karşılaştırma için `shift(12)`, haftalık için
`shift(7)` kullanılır — `seri / seri.shift(7) - 1` geçen haftanın aynı günüyle kıyaslar).
""",
        ornek="""gunler = pd.date_range("2026-01-01", "2026-01-10", freq="D")
seri = pd.Series([5, 6, 4, 7, 5, 6, 8, 5, 6, 7], index=gunler)
print(seri.rolling(3).mean().round(1))    # ilk 2 değer NaN, sonra son 3 günün ortalaması""",
        ornek_dili="python",
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
        anlatim="""
`seri.index.dayofweek`, her tarihin haftanın hangi günü olduğunu 0 (Pazartesi) ile 6
(Pazar) arasında verir; `< 5` hafta içi, `>= 5` hafta sonu demektir. Hafta içi/hafta sonu
ortalamalarını ayrı ayrı hesaplamak, tek bir genel ortalamanın gizleyebileceği bir
örüntüyü (mevsimsellik) ortaya çıkarır.

Son bir uyarı: gerçek veride satış olmayan günler genelde tabloda hiç **görünmez** (satır
yoktur). Bu durumda günlük ortalama, sadece satış olan günlerin ortalaması olur ve gerçeği
olduğundan yüksek gösterir. `seri.asfreq("D")` eksik günleri sıfır/NaN olarak tabloya ekler.
""",
        ornek="""gunler = pd.date_range("2026-01-01", "2026-01-14", freq="D")   # 2 hafta
seri = pd.Series(range(14), index=gunler)
print(seri[seri.index.dayofweek < 5].mean(), seri[seri.index.dayofweek >= 5].mean())""",
        ornek_dili="python",
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
