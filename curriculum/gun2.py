"""Bölüm 2: Python temelleri — değişkenler, veri tipleri, operatörler, metin."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=2,
    baslik="Python temelleri",
    anlatim=(
        "Bu bölümde dört temel veri tipini, tip dönüşümünü, sayıyı okunur metne çeviren "
        "f-string'i ve `if`'in bir değeri nasıl True/False saydığını (truthiness) öğreneceksin."
    ),
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
        anlatim="""
Dört temel tip: `int` (tam sayı), `float` (ondalıklı sayı), `str` (metin), `bool`
(`True`/`False`). Bir CSV'den okunan sayılar bazen metin gelir; `int("3")`, `float("1850.5")`
ile sayıya, `str(5)` ile metne çevirirsin. Metin ile sayı doğrudan toplanmaz/çarpılmaz —
önce dönüştürmen gerekir, yoksa `TypeError` alırsın.

Aritmetik operatörler: `+ - * /` (bölme her zaman `float` döner), `//` (tam bölüm, ondalığı
atar), `%` (kalan), `**` (üs). Karşılaştırma operatörleri (`== != < > <= >=`) her zaman bir
`bool` sonuç verir.
""",
        ornek="""adet_metni = "4"
birim_fiyat = 120.0
toplam = int(adet_metni) * birim_fiyat
print(toplam)      # -> 480.0  (önce int(...) ile çevirmeseydin TypeError alırdın)""",
        ornek_dili="python",
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
        anlatim="""
**f-string**, bir sayıyı okunur metne çevirmenin yoludur: bir metnin başına `f` koyup süslü
parantez `{}` içine bir değişken/ifade yazarsın. `f"{tutar:,.0f} TL"` binlik ayraçlı,
ondalıksız bir metin üretir. Biçim kodunun okunuşu: `,` binlik ayraç ekle, `.0f` ondalığı 0
basamağa yuvarla (yani tamamen at); `.2f` iki ondalık basamak bırakır, `.1%` oranı yüzdeye
çevirip bir ondalıkla gösterir (`0.157` → `"15.7%"`).
""",
        ornek="""adet = 3
birim_fiyat = 2400.0
print(f"{adet} adet, toplam {adet * birim_fiyat:,.0f} TL")   # -> "3 adet, toplam 7,200 TL\"""",
        ornek_dili="python",
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
        anlatim="""
**Doğruluk değeri (truthiness)**: `if` yalnızca bir karşılaştırmayı değil, herhangi bir
değeri de koşul olarak kabul eder. `0`, `0.0`, `""` (boş metin), `None`, boş liste `[]` ve
boş sözlük `{}` **False** sayılır; geri kalan hemen hemen her şey **True**'dur. Bu yüzden
`if liste:` yazmak "liste boş değilse" anlamına gelir, `len(liste) > 0` yazmaya gerek
kalmaz. `bool(deger)` bir değerin truthiness'ini doğrudan True/False olarak verir.
""",
        ornek="""for deger in [0, "merhaba", [], {"a": 1}]:
    print(deger, "->", bool(deger))
# -> 0 -> False   merhaba -> True   [] -> False   {'a': 1} -> True""",
        ornek_dili="python",
        soru="`[0, 1, '', 'a', None, [], [0]]` listesindeki her elemanın `bool(...)` değerini, sırayı koruyarak bir liste olarak `result`'a yaz.",
        beklenen="result = [False, True, False, True, False, False, True]",
        ipucu="Liste üretimi: [bool(x) for x in liste].",
        cozum='result = [bool(x) for x in [0, 1, "", "a", None, [], [0]]]',
    ),
]
