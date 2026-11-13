"""Bölüm 16: Excel ile çalışma ve raporlama otomasyonu."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=16,
    baslik="Excel ile çalışma ve raporlama",
    anlatim=(
        "Analizi Python'da yaparsın, ama raporu okuyan kişi büyük olasılıkla Excel açar. "
        "Bu bölümde çok sayfalı bir Excel raporu için veriyi hazırlamayı öğreneceksin "
        "(gerçek dosya yazımı `openpyxl` ile olur, tarayıcıda çalışmaz)."
    ),
    metrikler=[
        Metrik(
            baslik="Dikkat",
            aciklama="Excel'de sayfa adı en fazla 31 karakter olabilir ve / \\ ? * [ ] karakterlerini içeremez.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b16-s01",
        gun=16,
        tur="python",
        kavram="Çok sayfalı rapor için özet tablo",
        anlatim="""
Gerekli kütüphane `openpyxl`'dur (`pip install openpyxl`); pandas `.xlsx` okurken/yazarken
arka planda bunu kullanır. Okuma: `pd.read_excel("rapor.xlsx", sheet_name="Ocak")` tek
sayfa, `sheet_name=None` bütün sayfaları `{sayfa_adı: DataFrame}` sözlüğü olarak getirir;
`skiprows=3` üstteki logo/başlık satırlarını atlar.

Çok sayfalı bir rapor yazarken, her sayfaya gidecek tabloyu **önceden**, ayrı birer
DataFrame olarak hazırlarsın; sonra hepsini tek bir `ExcelWriter` ile aynı dosyaya,
farklı sayfa adlarıyla yazarsın:
""",
        ornek="""with pd.ExcelWriter("aylik_rapor.xlsx", engine="openpyxl") as yazici:
    sehir_ozet.to_excel(yazici, sheet_name="Şehir Özeti", index=False)
    df.to_excel(yazici, sheet_name="Ham Veri", index=False)   # okuyan kişi kaynağa inebilsin""",
        ornek_dili="python",
        soru=(
            "`ciro` sütununu ekle. 'Şehir Özeti' sayfasına yazılacak tabloyu hazırla: şehir bazında "
            "`siparis` (sipariş sayısı) ve `ciro` (toplam), `ciro`'ya göre azalan sıralı, `as_index=False`. "
            "Sonucu `result`'a yaz."
        ),
        beklenen="4 satır (sehir, siparis, ciro), ciro azalan sırada (Ankara en üstte).",
        ipucu="df.groupby('sehir', as_index=False).agg(siparis=('siparis_id','count'), ciro=('ciro','sum')).sort_values('ciro', ascending=False)",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            "result = (df.groupby('sehir', as_index=False)\n"
            "          .agg(siparis=('siparis_id', 'count'), ciro=('ciro', 'sum'))\n"
            "          .sort_values('ciro', ascending=False))"
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b16-s02",
        gun=16,
        tur="python",
        kavram="'Pivot' sayfası için tablo",
        anlatim="""
Biçimlendirme (başlığı kalınlaştırmak, sütun genişliği, sayı biçimi) `openpyxl` ile
dosyayı açıp düzenlenir (`Font`, `PatternFill`, `number_format`, `freeze_panes`). **Sayı
biçimi değeri değiştirmez**, sadece görünümü değiştirir — sayıyı f-string ile `"9.800 TL"`
metnine çevirip yazarsan Excel'de artık toplanamaz; sayıyı sayı olarak bırakıp biçimi
`number_format` ile vermelisin.

Otomasyonun anahtarı: değişen her şeyi (dosya yolu, ay) en üstte toplamak, geri kalanını
fonksiyonlara bölmek ve `if __name__ == "__main__":` ile betiği hem notebook'ta import
edilebilir hem terminalden çalıştırılabilir yapmaktır. Bir pivot tablosu da aynı mantıkla,
kaydetmeden önce ayrı bir DataFrame olarak hazırlanır.
""",
        ornek="""# openpyxl ile biçimlendirme (gerçek dosyada):
# ws["A1"].font = Font(bold=True)
# ws["C"][1:] için hucre.number_format = '#,##0 "TL"'  (değer değişmez, görünüm değişir)
pivot_ozet = df.pivot_table(values="adet", index="sehir", aggfunc="sum")
print(pivot_ozet)""",
        ornek_dili="python",
        soru="`ciro` sütununu ekle. 'Pivot' sayfasına yazılacak tabloyu hazırla: satırlarda `sehir`, sütunlarda `kategori`, değerlerde ciro toplamı, boş hücreler 0. Sonucu `result`'a yaz.",
        beklenen="4 satır (şehirler), 3 sütun (kategoriler), toplamı 18130.",
        ipucu="pd.pivot_table(df, values='ciro', index='sehir', columns='kategori', aggfunc='sum', fill_value=0)",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            "result = pd.pivot_table(df, values='ciro', index='sehir', columns='kategori', aggfunc='sum', fill_value=0)"
        ),
        tablo="siparisler",
    ),
]
