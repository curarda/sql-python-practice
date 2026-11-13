"""Bölüm 9: Veri temizleme."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=9,
    baslik="Veri temizleme",
    anlatim=(
        '"Analistin zamanının yaklaşık %80\'i veriyi temizlemekle geçer." Bu bölümde sütun '
        "adlarını standartlaştırmayı, Türkçe karakterli metinleri doğru düzeltmeyi, Türkçe "
        "biçimli sayı/tarihleri çevirmeyi, tekrarları ve aykırı değerleri bulmayı öğreneceksin — "
        "hepsini `kirli` adlı, bilerek sorunlu küçük bir tabloda."
    ),
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı rakam",
            aciklama="Tek bir aşırı büyük (aykırı) değer, 8 günlük bir ortalamayı gerçek değerinin 3,5 katına çıkarabilir.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b9-s01",
        gun=9,
        tur="python",
        kavram="Sütun adlarını standartlaştırma",
        anlatim="""
`kirli` tablosu, Excel'den gelen dosyaların tipik sorunlarını taşır: sütun adlarında
boşluk/Türkçe karakter, isimlerde karışık harf ve fazladan boşluk, Türkçe biçimli sayılar
(`"1.250,50"`), üç farklı tarih biçimi, kural dışı bir puan (120, oysa 1-5 arası olmalı) ve
tekrar eden satırlar. Temizliğin **ilk adımı her zaman sütun adları**: `.str.strip()`
(baştaki/sondaki boşluk), `.str.lower()` (küçük harf), `.str.replace(" ", "_")` (boşluk
yerine alt çizgi). Bunu ilk iş yapmak gerekir, çünkü sonraki her satırda bu adları
yazacaksın; `" Müşteri Adı "` gibi görünmeyen bir boşluk, `KeyError` hatalarının en sinsi
kaynağıdır.
""",
        ornek="""toy = pd.DataFrame({" Ürün Adı ": ["Kalem"], "Fİyat (TL)": [5]})
toy.columns = toy.columns.str.strip().str.lower().str.replace(" ", "_")
print(toy.columns.tolist())    # -> ['ürün_adı', 'fİyat_(tl)']  (harf/karakter temizliği ayrı adım)""",
        ornek_dili="python",
        soru="`kirli` tablosunun sütun adlarını standartlaştır: baştaki/sondaki boşlukları sil, küçük harfe çevir, boşlukları alt çizgiye çevir, ü/ş/ı harflerini u/s/i yap. Yeni sütun adlarının listesini `result`'a yaz.",
        beklenen="result = ['musteri_adi', 'sehir', 'tutar', 'tarih', 'puan']",
        ipucu='kirli.columns.str.strip().str.lower().str.replace(" ", "_") ile başla, sonra ü/ş/ı harflerini ayrı ayrı değiştir.',
        cozum=(
            "kirli.columns = (kirli.columns.str.strip().str.lower()\n"
            '                 .str.replace(" ", "_")\n'
            '                 .str.replace("ü", "u").str.replace("ş", "s").str.replace("ı", "i"))\n'
            "result = kirli.columns.tolist()"
        ),
        tablo="kirli",
    ),
    Soru(
        id="b9-s02",
        gun=9,
        tur="python",
        kavram="Türkçe biçimli sayı temizliği",
        anlatim="""
`"1.250,50"` Türkçe biçimde "bin iki yüz elli virgül elli" demektir. Python için önce
binlik noktayı silip sonra virgülü noktaya çevirmek gerekir — **sıra önemlidir**: virgülü
önce noktaya çevirseydin `"1.250.50"` olurdu ve hangi noktanın ondalık olduğu kaybolurdu.
`pd.to_numeric(..., errors="coerce")`, çevrilemeyen değerleri (`"abc"` gibi) hata vermek
yerine `NaN` yapar; dosyayı en baştan `pd.read_csv(..., sep=";", decimal=",",
thousands=".")` ile okumak çoğu zaman bu adımı hiç gerektirmez.
""",
        ornek="""metinler = pd.Series(["2.500,00", "1.300", "???"])
sayilar = pd.to_numeric(
    metinler.str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
    errors="coerce",
)
print(sayilar.tolist())    # -> [2500.0, 1300.0, nan]""",
        ornek_dili="python",
        soru="`kirli` tablosundaki `Tutar` sütununu sayıya çevir (binlik nokta sil, virgülü noktaya çevir; çevrilemeyeni, örn. \"abc\", NaN yap). Geçerli (NaN olmayan) tutarların toplamını `result`'a yaz.",
        beklenen="result = 7681.0",
        ipucu='str.replace(".", "", regex=False).str.replace(",", ".", regex=False) sonra pd.to_numeric(..., errors="coerce").',
        cozum=(
            'tutar = pd.to_numeric(\n'
            '    kirli["Tutar"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False),\n'
            '    errors="coerce",\n'
            ")\n"
            "result = float(tutar.sum())"
        ),
        tablo="kirli",
    ),
    Soru(
        id="b9-s03",
        gun=9,
        tur="python",
        kavram="Tekrar, geçersiz değer ve eksik veri (tam temizlik)",
        anlatim="""
Python'un `title()` metodu Türkçe "i" harfini yanlış büyütür (`"istanbul".title()` →
`"Istanbul"`, noktasız I; doğrusu `"İstanbul"`). Bunun için özel bir `tr_baslik`
fonksiyonu yazılır (örnekte).

Tarihler bu bölümün en tehlikeli tuzağıdır: karışık biçimli tarihleri tek komutla
`dayfirst=True` ile çözmeye kalkarsan, aynı sütunda ISO biçimli (yıl-ay-gün) bir tarih
varsa hata vermeden **sessizce yanlış tarih üretir**. Güvenli yol: her biçimi ayrı
`pd.to_datetime(..., format=...)` ile çöz, sonra `.fillna(...)` ile sırayla birleştir.

Geçersiz değer (1-5 arası puanda 120 gibi) `df.loc[koşul, "sütun"] = np.nan` ile düzeltilir.
**Tekrarları ara sırası önemlidir**: `duplicated()` kontrolünü metinleri/tipleri
temizledikten **sonra** yap — temizlemeden önce `"  ayşe yılmaz"` ile `"Ayşe Yılmaz"`
farklı görünür ve tekrar sayılmaz.
""",
        ornek="""def tr_baslik(metin):
    if pd.isna(metin):
        return metin
    kucuk = metin.strip().replace("I", "ı").replace("İ", "i").lower()
    return " ".join((("İ" if k[0] == "i" else ("I" if k[0] == "ı" else k[0].upper())) + k[1:]) for k in kucuk.split())

print(tr_baslik("  izmir "))     # -> "İzmir"   (title() "Izmir" derdi, yanlış)""",
        ornek_dili="python",
        soru=(
            "`kirli` tablosunu baştan sona temizle: sütun adlarını standartlaştır (b9-s01'deki gibi), "
            "`musteri_adi` ve `sehir`'i `.str.strip().str.lower().str.title()` ile normalize et, "
            "1-5 arası olması gereken `puan`'da 5'ten büyük olanları `NaN` yap, sonra tekrar eden "
            "satırları at. Kalan satır sayısı ile `puan`'ı hâlâ eksik olan satır sayısını "
            "`(satir_sayisi, eksik_puan)` biçiminde `result`'a yaz."
        ),
        beklenen="result = (4, 2)",
        ipucu=(
            "Python'un .str.title() metodu Türkçe 'i' harfinde hata yapar ('istanbul' -> 'Istanbul', "
            "noktasız). Bölüm 2'deki gibi küçük bir tr_baslik(metin) yardımcı fonksiyonu yaz ve "
            ".apply(tr_baslik) ile kullan. Sıra önemli: en son drop_duplicates()."
        ),
        cozum=(
            "def tr_baslik(metin):\n"
            "    if pd.isna(metin):\n"
            "        return metin\n"
            "    kucuk = metin.strip().replace('I', 'ı').replace('İ', 'i').lower()\n"
            "    kelimeler = []\n"
            "    for k in kucuk.split():\n"
            "        ilk = {'i': 'İ', 'ı': 'I'}.get(k[0], k[0].upper())\n"
            "        kelimeler.append(ilk + k[1:])\n"
            "    return ' '.join(kelimeler)\n\n"
            "k = kirli.copy()\n"
            "k.columns = (k.columns.str.strip().str.lower().str.replace(' ', '_')\n"
            "             .str.replace('ü', 'u').str.replace('ş', 's').str.replace('ı', 'i'))\n"
            "k['musteri_adi'] = k['musteri_adi'].apply(tr_baslik)\n"
            "k['sehir'] = k['sehir'].apply(tr_baslik)\n"
            "k.loc[k['puan'] > 5, 'puan'] = None\n"
            "k = k.drop_duplicates()\n"
            "result = (len(k), int(k['puan'].isna().sum()))"
        ),
        tablo="kirli",
    ),
    Soru(
        id="b9-s04",
        gun=9,
        tur="python",
        kavram="IQR ile aykırı değer",
        anlatim="""
Aykırı değer (outlier), mümkün ama alışılmadık bir değerdir (veri giriş hatasından farklı).
Bulmanın en yaygın yolu **IQR kuralıdır**: IQR (interquartile range, çeyrekler arası
açıklık) verinin ortadaki %50'sinin genişliğidir, `Q3 - Q1` (üçüncü çeyrek eksi birinci
çeyrek). Sınırlar: `alt = Q1 - 1.5 × IQR`, `üst = Q3 + 1.5 × IQR`; bu aralığın dışında
kalan değer aykırı sayılır. Bulduktan sonra ne yapacağın (düzelt/tut/sınıra çek) otomatik
bir adım değil, bir karardır — hangi kuralı kullandığını her zaman not al. Son olarak:
`isna().sum()` ile eksik veriyi say; satırı atmak, bir değerle (medyan gibi aykırıya
dayanıklı bir ölçü) doldurmak ya da zaman serisinde `ffill()` ile önceki değeri taşımak
arasında seçim, eksikliğin *nedenine* bağlıdır.
""",
        ornek="""sicakliklar = pd.Series([21, 22, 20, 23, 21, 45])
q1, q3 = sicakliklar.quantile([0.25, 0.75])
iqr = q3 - q1
alt, ust = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(sicakliklar[(sicakliklar < alt) | (sicakliklar > ust)].tolist())    # -> [45]""",
        ornek_dili="python",
        soru="`gunluk = [12, 15, 14, 13, 16, 15, 14, 300]` günlük sipariş sayıları için IQR kuralıyla (Q1-1.5·IQR, Q3+1.5·IQR dışındakiler aykırı) aykırı değerleri bir liste olarak `result`'a yaz.",
        beklenen="result = [300]",
        ipucu="pd.Series(gunluk).quantile([0.25, 0.75]) ile Q1 ve Q3'ü bul, IQR = Q3 - Q1.",
        cozum=(
            "gunluk = pd.Series([12, 15, 14, 13, 16, 15, 14, 300])\n"
            "q1, q3 = gunluk.quantile([0.25, 0.75])\n"
            "iqr = q3 - q1\n"
            "alt, ust = q1 - 1.5 * iqr, q3 + 1.5 * iqr\n"
            "result = gunluk[(gunluk < alt) | (gunluk > ust)].tolist()"
        ),
        tablo="kirli",
    ),
]
