"""Bölüm 9: Veri temizleme."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=9,
    baslik="Veri temizleme",
    anlatim="""
"Analistin zamanının yaklaşık %80'i veriyi temizlemekle geçer." `kirli` tablosu, Excel'den
gelen dosyaların tipik sorunlarını taşır: sütun adlarında boşluk/Türkçe karakter, isimlerde
karışık harf ve fazladan boşluk, Türkçe biçimli sayılar (`"1.250,50"`), üç farklı tarih
biçimi, kural dışı bir puan (120, 1-5 arası olmalı) ve tekrar eden satırlar.

Önerilen sıra:

1. **Sütun adları**: `.str.strip().str.lower().str.replace(" ", "_")` ile standartlaştır.
2. **Metinler**: Python'un `title()` metodu Türkçe "i"yi "I"ya çevirir (`"istanbul".title()`
   → `"Istanbul"`, yanlış); özel bir `tr_baslik` fonksiyonu gerekir.
3. **Tipler**: `"1.250,50"` için önce binlik noktayı sil, sonra virgülü noktaya çevir;
   `pd.to_numeric(..., errors="coerce")` çeviremediğini (`"abc"`) NaN yapar. Karışık tarih
   biçimlerini tek seferde `dayfirst=True` ile çözmeye çalışma — sessizce yanlış tarih üretir;
   her biçimi ayrı `pd.to_datetime(..., format=...)` ile çöz, sonra `fillna` ile birleştir.
4. **Tekrarlar**: `duplicated()` ile bul, **temizlikten sonra** ara (temizlemeden önce
   `"  ayşe yılmaz"` ile `"Ayşe Yılmaz"` farklı görünür ve tekrar sayılmaz).
5. **Geçersiz/aykırı değerler**: kural dışı bir değer (1-5 arası puanda 120) `df.loc[koşul,
   "sütun"] = np.nan` ile düzeltilir. Aykırı değer (outlier) ise olası ama alışılmadık bir
   değerdir; **IQR kuralı** ile bulunur: `alt = Q1 - 1.5·IQR`, `üst = Q3 + 1.5·IQR`.
6. **Eksik veri**: `isna().sum()` ile say; satırı at, bir değerle doldur ya da (zaman
   serisinde) `ffill()` ile bir önceki değeri taşı — seçim, eksikliğin *nedenine* bağlıdır.
""",
    ornek="""kirli.columns = (kirli.columns.str.strip().str.lower()
                 .str.replace(" ", "_")
                 .str.replace("ü", "u").str.replace("ş", "s").str.replace("ı", "i"))
print(kirli.columns.tolist())
# -> ['musteri_adi', 'sehir', 'tutar', 'tarih', 'puan']""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı rakam",
            aciklama="Tek bir 300'lük aykırı gün yüzünden 8 günün ortalaması 49,9 çıkar; oysa diğer 7 günün ortalaması 14,1'dir. Tek bir değer sonucu 3,5 katına çıkarabilir.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b9-s01",
        gun=9,
        tur="python",
        kavram="Sütun adlarını standartlaştırma",
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
