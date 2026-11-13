"""Bölüm 8: pandas II — seçme, filtreleme, sıralama, yeni sütun."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=8,
    baslik="pandas II: seçme ve filtreleme",
    anlatim=(
        "Bu bölümde satır/sütun seçmeyi (loc, iloc), boolean filtrelemeyi, yeni sütun "
        "türetmeyi, sıralamayı ve sütun adlarıyla oynamayı öğreneceksin."
    ),
    metrikler=[
        Metrik(
            baslik="Dikkat",
            aciklama="df[koşul1 & koşul2] yazarsan öncelik hatası alırsın; her koşulu kendi parantezine al: (koşul1) & (koşul2).",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b8-s01",
        gun=8,
        tur="python",
        kavram="Yeni sütun ve sıralama",
        anlatim="""
**Yeni sütun**: `df["yeni"] = df["a"] * df["b"]` var olan sütunlardan yenisini türetir,
satır sayısını değiştirmez. **Sıralama**: `df.sort_values("sutun", ascending=False)`
büyükten küçüğe sıralar; en büyük n satırı istiyorsan `df.nlargest(n, "sutun")` daha
kısadır ve aynı işi yapar. Belirli sütunları seçip listeye çevirmek için sıralanmış
tablonun üzerine `[["a", "b"]]` ile sütun seç, sonra `.itertuples(index=False, name=None)`
ile satırları tuple'a çevir.
""",
        ornek="""kucuk = pd.DataFrame({"urun": ["Kalem", "Defter", "Silgi"], "adet": [10, 2, 5], "fiyat": [5, 40, 8]})
kucuk["tutar"] = kucuk["adet"] * kucuk["fiyat"]
print(kucuk.nlargest(2, "tutar")[["urun", "tutar"]])
#      urun  tutar
#    Defter     80
#     Kalem     50""",
        ornek_dili="python",
        soru="`df`'e `ciro = adet * birim_fiyat` sütununu ekle. En yüksek cirolu 3 ürünü, `(urun, ciro)` tuple'larından oluşan bir liste olarak (büyükten küçüğe) `result`'a yaz.",
        beklenen="result = [('Monitör', 6500), ('Mont', 2400), ('Ayakkabı', 1900)]",
        ipucu="sort_values('ciro', ascending=False).head(3) ile en yüksek 3 satırı al, itertuples ya da values ile tuple listesine çevir.",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            'en_yuksek = df.sort_values("ciro", ascending=False).head(3)\n'
            'result = list(en_yuksek[["urun", "ciro"]].itertuples(index=False, name=None))'
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b8-s02",
        gun=8,
        tur="python",
        kavram="Boolean filtre",
        anlatim="""
`df["sütun"]` bir Series, `df[["a", "b"]]` bir DataFrame seçer. `df.loc[etiket, "sütun"]`
satır **etiketiyle**, `df.iloc[0:5]` satır **konumuyla** (sıra numarasıyla) seçer.

**Boolean filtre**: `df[df["adet"] >= 2]` koşulu sağlayan satırları getirir. Birden fazla
koşulu birleştirirken `&` (ve) / `|` (veya) kullanılır ve **her koşul kendi parantezine
alınmalıdır**: `df[(df["adet"] >= 2) & (df["sehir"] == "Ankara")]`. Parantezleri unutursan
Python işlem önceliğini yanlış yorumlar ve hata alırsın.
""",
        ornek="""kucuk = pd.DataFrame({"urun": ["Kalem", "Defter", "Silgi"], "adet": [10, 2, 5], "fiyat": [5, 40, 8]})
print(kucuk[kucuk["adet"] >= 5]["fiyat"].mean())    # -> 6.5  (Kalem ve Silgi'nin ortalama fiyatı)""",
        ornek_dili="python",
        soru="`adet` değeri 2 veya üzeri olan siparişlerin ortalama `birim_fiyat`ını, 1 ondalığa yuvarlanmış olarak `result`'a yaz.",
        beklenen="result = 425.0",
        ipucu="df[df['adet'] >= 2]['birim_fiyat'].mean() filtrelenmiş ortalamayı verir.",
        cozum="result = round(df[df['adet'] >= 2]['birim_fiyat'].mean(), 1)",
        tablo="siparisler",
    ),
    Soru(
        id="b8-s03",
        gun=8,
        tur="python",
        kavram="iloc",
        anlatim="""
`iloc`, "integer location" demektir: satırları **konumlarına** (0'dan başlayan sıra
numarasına) göre seçer, satır etiketleri ne olursa olsun. `df.iloc[:3]` ilk 3 satırı,
`df["sütun"].iloc[:3]` ise bir sütunun ilk 3 değerini verir. `loc`'tan farkı: `loc` satır
**etiketiyle** (index değeriyle) çalışır, etiketler sıra numarasından farklı olabilir
(ör. filtrelemeden sonra 0,1,2 yerine 3,7,9 kalabilir); `iloc` her zaman 0,1,2... sırasına
göre gider.
""",
        ornek="""kucuk = pd.DataFrame({"urun": ["Kalem", "Defter", "Silgi", "Cetvel"]})
print(kucuk["urun"].iloc[:2].tolist())    # -> ['Kalem', 'Defter']  (ilk 2 satır, konuma göre)""",
        ornek_dili="python",
        soru="`df`'in ilk 3 satırının `urun` sütununu, sıralı bir liste olarak `result`'a yaz.",
        beklenen="result = ['Kulaklık', 'Mont', 'Klavye']",
        ipucu="df['urun'].iloc[:3].tolist() ilk 3 satırın ürün adlarını verir.",
        cozum="result = df['urun'].iloc[:3].tolist()",
        tablo="siparisler",
    ),
    Soru(
        id="b8-s04",
        gun=8,
        tur="python",
        kavram="Sütun adı değiştirmek",
        anlatim="""
Sütun adı değiştirmek için `df.rename(columns={"eski": "yeni"})` kullanılır; bu, **yeni
bir DataFrame döndürür**, orijinali değiştirmez (orijinali de değiştirmek istiyorsan
`inplace=True` eklenir, ama genelde yeni bir değişkene atamak daha güvenlidir). Bir sütunu
tamamen silmek için `df.drop(columns=["x"])` kullanılır.
""",
        ornek="""kucuk = pd.DataFrame({"urun_adi": ["Kalem"], "fiyat": [5]})
yeni = kucuk.rename(columns={"urun_adi": "urun"})
print(yeni.columns.tolist())    # -> ['urun', 'fiyat']
print(kucuk.columns.tolist())   # -> ['urun_adi', 'fiyat']  (orijinal değişmedi)""",
        ornek_dili="python",
        soru="`df`'teki `musteri_id` sütununun adını `musteri` olarak değiştir (orijinali bozma). Yeni sütun adlarının listesini `result`'a yaz.",
        beklenen="result = ['siparis_id', 'tarih', 'musteri', 'sehir', 'kategori', 'urun', 'adet', 'birim_fiyat']",
        ipucu="df.rename(columns={'musteri_id': 'musteri'}) yeni bir DataFrame döndürür; .columns.tolist() ile liste al.",
        cozum="result = df.rename(columns={'musteri_id': 'musteri'}).columns.tolist()",
        tablo="siparisler",
    ),
]
