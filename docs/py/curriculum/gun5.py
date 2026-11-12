"""Bölüm 5: Fonksiyonlar, modüller, hata yönetimi, dosya işlemleri."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=5,
    baslik="Fonksiyonlar ve hata yönetimi",
    anlatim="""
`def ad(parametreler):` ile fonksiyon tanımlanır, `return` sonucu geri verir. `lambda
parametre: ifade` tek satırlık, isimsiz bir fonksiyondur; genelde `sorted(..., key=lambda
x: ...)` gibi yerlerde kullanılır.

`import kutuphane` ile başkasının yazdığı kodu kullanırsın (`import pandas as pd` gibi
takma adla). Kendi dosyalarını da `import dosya_adi` ile içe aktarabilirsin.

**Hata yönetimi**: bir işlem başarısız olabileceğinde (`float("abc")` gibi) programın
çökmesini `try / except` ile engellersin:

```
try:
    sayi = float(metin)
except ValueError:
    sayi = None   # ya da bu satırı atla
```

Belirli bir hata türünü yakala (`except ValueError`), her şeyi yutan çıplak `except:`
yazma; gerçek bir programlama hatasını da gizleyebilir.

Dosya/klasör işlemleri için `pathlib.Path` kullanılır: `Path("veri").glob("*.csv")` bir
klasördeki bütün CSV dosyalarını listeler (Bölüm 11'de concat ile birlikte kullanılır).
""",
    ornek="""def buyume(eski, yeni):
    \"\"\"Yüzde değişim; eski 0 ise None döndürür.\"\"\"
    if eski == 0:
        return None
    return round((yeni - eski) / eski * 100, 1)

print(buyume(5000, 3340))   # -> -33.2""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Dikkat",
            aciklama="Çıplak `except:` her hatayı yutar; hangi hatayı beklediğini (ValueError, KeyError...) her zaman yaz.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b5-s01",
        gun=5,
        tur="python",
        kavram="def ile fonksiyon",
        soru='`buyume(eski, yeni)` adında, yüzde değişimi virgülden sonra bir basamakla döndüren ve `eski` sıfırsa `None` döndüren bir fonksiyon yaz. `result = [buyume(5000, 3340), buyume(3340, 9790)]` yaz.',
        beklenen="result = [-33.2, 193.1]",
        ipucu="Yüzde değişim: (yeni - eski) / eski * 100. round(..., 1) ile yuvarla.",
        cozum=(
            "def buyume(eski, yeni):\n"
            "    if eski == 0:\n"
            "        return None\n"
            "    return round((yeni - eski) / eski * 100, 1)\n\n"
            "result = [buyume(5000, 3340), buyume(3340, 9790)]"
        ),
    ),
    Soru(
        id="b5-s02",
        gun=5,
        tur="python",
        kavram="try / except",
        soru='`fiyatlar_metin = ["750", "abc", "1900"]` listesindeki her elemanı `float`\'a çevirmeyi dene; çevrilemeyeni (`"abc"`) atla. Çevrilebilenlerin toplamını `result`\'a yaz.',
        beklenen="result = 2650.0",
        ipucu="try/except ValueError içinde float(f) çağır; hata olursa continue ya da pass kullan.",
        cozum=(
            'fiyatlar_metin = ["750", "abc", "1900"]\n'
            "result = 0.0\n"
            "for f in fiyatlar_metin:\n"
            "    try:\n"
            "        result += float(f)\n"
            "    except ValueError:\n"
            "        pass"
        ),
    ),
    Soru(
        id="b5-s03",
        gun=5,
        tur="python",
        kavram="lambda ile sıralama",
        soru='`ciftler = [("Mont", 2400), ("Roman", 180), ("Klavye", 1100)]` listesini ikinci elemana (fiyata) göre küçükten büyüğe sırala, `result`\'a yaz.',
        beklenen="result = [('Roman', 180), ('Klavye', 1100), ('Mont', 2400)]",
        ipucu="sorted(ciftler, key=lambda x: x[1]) fiyata göre sıralar.",
        cozum='ciftler = [("Mont", 2400), ("Roman", 180), ("Klavye", 1100)]\nresult = sorted(ciftler, key=lambda x: x[1])',
    ),
]
