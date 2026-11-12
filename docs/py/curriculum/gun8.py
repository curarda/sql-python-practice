"""Bölüm 8: pandas II — seçme, filtreleme, sıralama, yeni sütun."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=8,
    baslik="pandas II: seçme ve filtreleme",
    anlatim="""
- `df["sütun"]` bir Series, `df[["a", "b"]]` bir DataFrame seçer.
- `df.loc[satır_etiketi, "sütun"]` etiketle, `df.iloc[0:5]` konumla seçer.
- **Boolean filtre**: `df[df["adet"] >= 2]`. Birden fazla koşul `&` (ve) / `|` (veya) ile
  birleştirilir, her koşul kendi parantezine alınır: `df[(df["adet"] >= 2) & (df["sehir"]
  == "Ankara")]`.
- **Yeni sütun**: `df["ciro"] = df["adet"] * df["birim_fiyat"]` — var olan sütunlardan yenisini
  türetir, satır sayısını değiştirmez.
- **Sıralama**: `df.sort_values("ciro", ascending=False)`; en büyük n satır için
  `df.nlargest(n, "ciro")` daha kısadır.
- Sütun adı değiştirmek: `df.rename(columns={"eski": "yeni"})`; silmek: `df.drop(columns=["x"])`.
""",
    ornek="""df["ciro"] = df["adet"] * df["birim_fiyat"]
en_cirolu = df.sort_values("ciro", ascending=False)[["urun", "ciro"]].head(3)
print(en_cirolu)
# ->        urun  ciro
#      Monitör  6500
#         Mont  2400
#     Ayakkabı  1900""",
    ornek_dili="python",
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
        soru="`df`'teki `musteri_id` sütununun adını `musteri` olarak değiştir (orijinali bozma). Yeni sütun adlarının listesini `result`'a yaz.",
        beklenen="result = ['siparis_id', 'tarih', 'musteri', 'sehir', 'kategori', 'urun', 'adet', 'birim_fiyat']",
        ipucu="df.rename(columns={'musteri_id': 'musteri'}) yeni bir DataFrame döndürür; .columns.tolist() ile liste al.",
        cozum="result = df.rename(columns={'musteri_id': 'musteri'}).columns.tolist()",
        tablo="siparisler",
    ),
]
