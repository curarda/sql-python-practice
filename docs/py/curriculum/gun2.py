"""Bölüm 2: Python temelleri — değişkenler, veri tipleri, operatörler, metin."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=2,
    baslik="Python temelleri",
    anlatim="""
Dört temel tip: `int` (tam sayı), `float` (ondalıklı sayı), `str` (metin), `bool`
(`True`/`False`). Bir CSV'den okunan sayılar bazen metin gelir; `int("3")`, `float("1850.5")`
ile sayıya, `str(5)` ile metne çevirirsin.

Aritmetik operatörler: `+ - * /` (bölme her zaman float döner), `//` (tam bölüm), `%` (kalan),
`**` (üs). Karşılaştırma: `== != < > <= >=`, sonuçları her zaman `bool`.

**f-string**, bir sayıyı okunur metne çevirmenin yoludur: `f"{tutar:,.0f} TL"` binlik ayraçlı,
ondalıksız bir metin üretir (`:,.2f` iki ondalıklı, `:.1%` yüzde biçimi için).

**Doğruluk değeri (truthiness)**: `if` bir koşulu değil, herhangi bir değeri de kabul eder.
`0`, `0.0`, `""`, `None`, boş liste/sözlük `False` sayılır; geri kalan her şey `True`'dur.
Bu yüzden `if liste:` ifadesi "liste boş değilse" anlamına gelir.
""",
    ornek="""adet_metni = "3"
birim_fiyat = 450.5
toplam = int(adet_metni) * birim_fiyat     # -> 1351.5
print(f"Toplam: {toplam:,.1f} TL")          # -> "Toplam: 1,351.5 TL\"""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Dikkat",
            aciklama="CSV'den okunan sayılar genelde metindir (str); doğrudan toplamaya çalışırsan TypeError alırsın. Önce dönüştür.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b2-s01",
        gun=2,
        tur="python",
        kavram="Tip dönüşümü",
        soru='`adet_metni = "3"` (metin) ve `birim_fiyat = 450.5` değişkenlerini tanımla. `adet_metni`yi tam sayıya çevirip `birim_fiyat` ile çarp, sonucu `result`\'a yaz.',
        beklenen="result = 1351.5",
        ipucu="int(adet_metni) ile önce metni tam sayıya çevir.",
        cozum='adet_metni = "3"\nbirim_fiyat = 450.5\nresult = int(adet_metni) * birim_fiyat',
    ),
    Soru(
        id="b2-s02",
        gun=2,
        tur="python",
        kavram="f-string ile biçimlendirme",
        soru='`tutar = 1850.5` değişkenini `"Toplam: 1,850 TL"` biçiminde (binlik ayraçlı, ondalıksız) bir metne çevirip `result`\'a yaz.',
        beklenen='result = "Toplam: 1,850 TL"',
        ipucu='f"{tutar:,.0f} TL" biçimini kullan; :,.0f binlik ayraç ekler ve ondalığı atar.',
        cozum='tutar = 1850.5\nresult = f"Toplam: {tutar:,.0f} TL"',
    ),
    Soru(
        id="b2-s03",
        gun=2,
        tur="python",
        kavram="Doğruluk değeri (truthiness)",
        soru="`[0, 1, '', 'a', None, [], [0]]` listesindeki her elemanın `bool(...)` değerini, sırayı koruyarak bir liste olarak `result`'a yaz.",
        beklenen="result = [False, True, False, True, False, False, True]",
        ipucu="Liste üretimi: [bool(x) for x in liste].",
        cozum='result = [bool(x) for x in [0, 1, "", "a", None, [], [0]]]',
    ),
]
