# Python & SQL Çalışma Uygulaması (Veri Analisti Stajyeri)

"Veri Analisti Stajyeri için Python: Sıfırdan Uygulamalı Kitapçık" temel alınarak hazırlanmış,
kişisel ve tamamen yerel bir çalışma aracı. Kitapçığın 20 bölümünü (kurulumdan uçtan uca bir
e-ticaret vakasına kadar) izler; her bölüm kısa bir anlatımla başlar, ardından sorular gelir.
Kodunu yazarsın, **Çalıştır** ile sonucu görürsün, **Kontrol et** ile değerlendirilirsin.
Arayüz ve geri bildirimler Türkçedir. Harici API, hesap veya internet gerektirmez.

## iPhone'da kullanma (ana ekrana ekle)

Uygulamanın tarayıcı sürümü tamamen cihazda çalışır; sunucu, hesap veya API gerektirmez.

1. iPhone'da **Safari** ile https://curarda.github.io/sql-python-calisma/ adresini aç.
2. Alt ortadaki **Paylaş** (kare + yukarı ok) düğmesine dokun.
3. **Ana Ekrana Ekle**'yi seç, sonra **Ekle**'ye dokun.

Ana ekrandaki simgeden açtığında tarayıcı çubuğu olmadan tam ekran çalışır.

- İlk açılışta Python ortamı (Pyodide, pandas, scipy, statsmodels) internetten indirilir ve birkaç dakika sürebilir. Bu bir kez olur; sayfayı tamamen yüklediğinde sonraki açılışlarda çevrimdışı da çalışır.
- İlerleme yalnızca o cihazın tarayıcısında (localStorage) saklanır. Mac'teki Streamlit sürümüyle ya da başka cihazla paylaşılmaz.
- Kod, 5 saniyeden uzun sürerse durdurulur ve sayfa donmaz.

### Tarayıcı sürümünü güncelleme (geliştirici)

Tarayıcı sürümü `web/` ve kök Python dosyalarından üretilir; `docs/` klasörü GitHub Pages'in yayınladığı çıktıdır.

```bash
python3 scripts/build_web.py
```

Sonra `docs/` değişikliklerini commit edip push et. Testler `docs/py` kopyalarının kaynakla eşleştiğini kontrol eder.

## Kurulum

Python 3.11 veya üstü gerekir.

```bash
cd sql_python_calisma
```

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

## Çalıştırma

```bash
streamlit run app.py
```

Tarayıcıda `http://localhost:8501` açılır. Uygulama kapatılıp açılsa da ilerlemen korunur.

## Testleri çalıştırma

```bash
pytest
```

Testler veri seti, SQL/pandas değerlendirmesi, ilerleme kaydı, müfredat tutarlılığı ve arayüz akışını kapsar.
Her soru için referans çözümün kendi kontrolünden geçtiği de test edilir; Bölüm 19 (uçtan uca vaka)
sorularının sonuçları ayrıca pandas groupby **kullanmayan**, saf Python döngüleriyle bağımsızca
doğrulanır (`tests/test_vakalar.py`). Kitapçığın kendi yazdığı sayısal cevaplarla (ör. net ciro
5.035.451 TL, iade oranı %9,0) birebir eşleştiği doğrulanmıştır.

Kullanıcı kodunu gerçek alt süreçte çalıştıran testler `tests/test_sandbox.py` içindedir (`gercek_sandbox` işaretli).
Diğer testler hız için aynı kodu süreç içinde çalıştırır. Python 3.11 ile test etmek için:

```bash
.venv311/bin/python -m pytest
```

## Müfredat (20 bölüm)

| # | Bölüm | # | Bölüm |
|---|---|---|---|
| 1 | Kurulum ve çalışma ortamı | 11 | merge ve concat |
| 2 | Python temelleri | 12 | Tarih ve zaman serisi |
| 3 | Veri yapıları (list/tuple/dict/set) | 13 | Görselleştirme |
| 4 | Kontrol akışı | 14 | Temel istatistik (korelasyon, A/B, regresyon) |
| 5 | Fonksiyonlar ve hata yönetimi | 15 | SQL ve Python |
| 6 | NumPy temelleri | 16 | Excel ile çalışma |
| 7 | pandas I: okuma ve ilk bakış | 17 | API ve JSON |
| 8 | pandas II: seçme ve filtreleme | 18 | İyi pratikler |
| 9 | Veri temizleme | 19 | Uçtan uca vaka: e-ticaret |
| 10 | Gruplama ve özetleme | 20 | Alıştırmalar ve tekrar |

## Nasıl çalışır

- **Veri seti (`data.py`):** kitapçığın kendi örnek verileri, aynı tohum ve aynı kod ile birebir
  yeniden üretilir — sayılar kitapçıktaki yazılı sonuçlarla eşleşir:
  - `siparisler` (10 satır, Bölüm 7-13'ün ortak e-ticaret tablosu)
  - `musteriler_kucuk` (6 satır, Bölüm 11'in merge/JOIN örneği — bilerek eksik/fazla anahtar içerir)
  - `kirli` (6 satır, Bölüm 9'un temizlik örneği — dağınık sütun adları, Türkçe sayı/tarih biçimleri)
  - `musteriler` + `vaka_siparisler` (800 + ~6000 satır, Bölüm 19-20'nin e-ticaret vakası — bilerek
    tekrarlı, eksik/negatif tutarlı, karışık yazımlı kategorili)
  - `gunluk_satis`, `reklam_satis`, `sepet_testi` (Bölüm 12 ve 14'ün zaman serisi/istatistik örnekleri)
  - `API_ORNEGI`, `KUR_JSON_METNI` (Bölüm 17'nin JSON örnekleri; tablo değil, düz Python nesneleri)

  SQL sorguları bellekte bir SQLite veritabanında, pandas soruları aynı verinin DataFrame hâlinde çalışır.
- **Zaman sınırı (`sandbox.py`, `sandbox_runner.py`):** Kullanıcı kodu (SQL ve Python) ana Streamlit sürecinde değil, ayrı bir alt süreçte çalışır.
  Veri alt süreçte aynı tohumla yeniden üretilir. 5 saniyeyi geçen kod alt süreçle birlikte sonlandırılır ve
  "Kodun 5 saniyeden uzun sürdü, sonsuz döngü olabilir" mesajı gösterilir. Her çalıştırma yaklaşık 1–1,5 saniye ek yük getirir (pandas'ın yüklenmesi).
  Referans çözümler güvenilir olduğu için süreç içinde çalışır.
- **Değerlendirme (`checker.py`):**
  - SQL: sorgunun sonucu, referans sorgunun sonucuyla sütun adları ve değerler bakımından karşılaştırılır. Satır sırası yalnızca soru sıra istiyorsa kontrol edilir.
  - Python/pandas: kod `df` (ve diğer tablolar, `json`, `API_ORNEGI`, `KUR_JSON_METNI`, `VAKA_*_CSV` yolları hazır olan) bir ad alanında çalışır, sonucu `result` değişkenine yazman beklenir.
  - Her değerlendirme taze bir veri kopyasında çalışır; bir sorgu veya kod diğer soruların verisini bozamaz.
  - Hatalar yakalanır ve Türkçe açıklanır; uygulama çökmez.
- **İlerleme (`progress.py`):** `progress.json` dosyasında her sorunun deneme sayısı, doğru/yanlış sayısı ve son denemeleri tutulur.
  Son iki denemesinin biri yanlış olan sorular **zayıf** sayılır ve "Bugünkü tekrar" sekmesinde gelir. Dosya bozulursa `progress.bozuk.json` olarak yedeklenir.
- **Çözüm:** Üç yanlış denemeden sonra "Çözümü göster" açılır. İpucu her zaman açılabilir.

## Dosya yapısı

```
app.py              Streamlit arayüzü
sandbox.py          Kullanıcı kodunu alt süreçte, 5 sn zaman sınırıyla çalıştırır
sandbox_runner.py   Alt süreçte çalışan giriş noktası (sandbox.py başlatır)
data.py             Kitapçığın kendi veri setleri (siparisler, vaka, kirli, ...)
checker.py          SQL ve pandas/Python değerlendirmesi
progress.py         progress.json okuma/yazma ve zayıflık mantığı
curriculum/         Bölümler ve sorular
  models.py         Soru, Ders, Metrik, Gun veri sınıfları
  gun1.py ... gun20.py  Her bölümün anlatımı, dikkat çekici notu ve soruları
  __init__.py       Tüm bölümleri ve soruları birleştirir
tests/              pytest testleri
veri/               Üretilen CSV dosyaları (read_csv alıştırması için; otomatik oluşur)
progress.json       Senin ilerleme kaydın (otomatik oluşur)
```

## Yeni soru ekleme

1. İlgili bölümün dosyasını aç (ör. `curriculum/gun10.py`).
2. `SORULAR` listesine yeni bir `Soru(...)` ekle. Alanlar:
   - `id`: benzersiz, ör. `"b10-s05"` (b = bölüm)
   - `gun`: bölüm numarası
   - `tur`: `"sql"` veya `"python"` (pandas da `python`)
   - `kavram`: zayıf konu özetinde görünen kısa ad
   - `soru`, `beklenen`, `ipucu`: Türkçe metinler
   - `cozum`: referans çözüm. Bu, doğruluğun tek ölçütüdür, mutlaka çalıştırıp test et.
   - `tablo` (Python soruları için): `df` olarak yüklenecek tablo, varsayılan `"siparisler"`
   - `sirali=True`: satır sırası da önemliyse
   - `ozet_gerekli=True`: kullanıcıdan 3 cümlelik özet de isteniyorsa
   - `kirlilik`: vakadaki bilinçli veri sorunu (arayüzde gizli "Veri notu")
   - `rubrik`: 3 cümlelik özet için değerlendirme ölçütleri (arayüzde "Ürün özeti rubriği")
3. Python sorularında sonucu `result` değişkenine yazan bir referans kodu ver.
4. `pytest` çalıştır. `test_curriculum.py` yeni sorunun referans çözümünün kendi kontrolünden geçtiğini doğrular.

Yeni bir bölüm eklemek için `curriculum/gunN.py` dosyası oluştur (`DERS` ve `SORULAR` tanımla) ve `curriculum/__init__.py` içindeki `_GUN_MODULLERI` listesine ekle.

## Bilinen sınırlamalar

- Alt süreç izolasyonu ve 5 saniyelik zaman sınırı vardır, ama bu bir güvenlik sandbox'ı değildir: kod, bilgisayarınızdaki dosyalara erişebilir. Tek kişilik yerel bir araç olduğu için kendi yazdığın kodu çalıştırmak amaçlanmıştır.
- Eğer `progress.json` silinirse ilerleme sıfırlanır.
- Değerlendirme sonuç tabanlıdır: farklı ama doğru bir yaklaşım da kabul edilir, ama sonuç tutmuyorsa kabul edilmez.
- Bölüm 13 (görselleştirme) ve 16 (Excel) sorularında gerçek bir grafik/Excel dosyası üretilmez; yalnızca grafiğin/dosyanın kullanacağı veri değerlendirilir (tarayıcıda `openpyxl`/`seaborn` bulunmuyor).
- Bölüm 14 ve 20'deki istatistik sorularında `scipy` ve `statsmodels` kullanılır; her iki ortamda (masaüstü ve tarayıcı) da kuruludur.
