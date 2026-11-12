"""Bölüm 4: Kontrol akışı — if, for, while, comprehension."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=4,
    baslik="Kontrol akışı",
    anlatim="""
- `if / elif / else`: koşula göre dallanma. Koşul bir karşılaştırma ya da truthiness olabilir.
- `for eleman in koleksiyon:` bir listeyi, sözlüğü ya da aralığı (`range(n)`) dolaşır.
- `while koşul:` koşul doğru olduğu sürece tekrar eder; döngüyü bir yerde durdurman gerekir,
  yoksa sonsuza kadar çalışır (`break` ile çıkılır).
- **Comprehension**, bir döngüyü tek satırda yazar: `[ifade for eleman in liste if koşul]`.
  Okunabilir ve genelde döngüden hızlıdır.

**pandas varken döngü yazmalı mıyım?** Çoğu zaman hayır: pandas'ın vektörleştirilmiş
işlemleri (Bölüm 6, 8) aynı işi satır satır döngüden çok daha hızlı yapar. Döngü, pandas'ın
doğrudan karşılığı olmayan özel bir mantık gerektiğinde ya da tek seferlik küçük işlerde
tercih edilir.
""",
    ornek="""fiyatlar = [750, 2400, 1100, 180, 1900]
pahalilar = [f for f in fiyatlar if f > 1000]
print(pahalilar, sum(pahalilar))     # -> [2400, 1100, 1900] 5400""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Kısa kural",
            aciklama="Basit bir filtre/dönüşümse comprehension yaz; birden çok adım ve okunabilirlik gerekiyorsa normal for döngüsüne geç.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b4-s01",
        gun=4,
        tur="python",
        kavram="if / elif / else",
        soru='`tutarlar = [180, 750, 1900, 6500]` listesindeki her tutarı sınıflandır: 500\'den küçükse "Ucuz", 500-2000 arası (2000 dahil) "Orta", üstü "Pahalı". Sonuçları sırayla bir liste olarak `result`\'a yaz.',
        beklenen="result = ['Ucuz', 'Orta', 'Orta', 'Pahalı']",
        ipucu="Bir sınıflandırma fonksiyonu yaz, sonra liste üretimiyle her tutara uygula.",
        cozum=(
            "def sinif(t):\n"
            "    if t < 500:\n"
            "        return 'Ucuz'\n"
            "    if t <= 2000:\n"
            "        return 'Orta'\n"
            "    return 'Pahalı'\n\n"
            "tutarlar = [180, 750, 1900, 6500]\n"
            "result = [sinif(t) for t in tutarlar]"
        ),
    ),
    Soru(
        id="b4-s02",
        gun=4,
        tur="python",
        kavram="for, zip ve comprehension",
        soru='`urunler = ["Kulaklık", "Mont", "Klavye"]` ve `fiyatlar = [750, 2400, 1100]` listelerini `zip` ile eşleştir; fiyatı 1000\'den büyük olan ürünlerin adlarını bir liste olarak `result`\'a yaz.',
        beklenen="result = ['Mont', 'Klavye']",
        ipucu="zip(urunler, fiyatlar) iki listeyi eş zamanlı dolaştırır: [u for u, f in zip(urunler, fiyatlar) if f > 1000].",
        cozum=(
            'urunler = ["Kulaklık", "Mont", "Klavye"]\n'
            "fiyatlar = [750, 2400, 1100]\n"
            "result = [u for u, f in zip(urunler, fiyatlar) if f > 1000]"
        ),
    ),
    Soru(
        id="b4-s03",
        gun=4,
        tur="python",
        kavram="while döngüsü",
        soru="`stok = 10` ile başla. `satislar = [2, 3, 4, 5]` listesindeki satışları sırayla stoktan düş. Stok 0 veya altına düştüğünde (ya da liste biterse) durdur; kaç satış işlendiğini (döngünün kaç kez çalıştığını) `result`'a tam sayı olarak yaz.",
        beklenen="result = 4",
        ipucu="while stok > 0 and i < len(satislar): ile ilerle, her adımda i'yi 1 artır.",
        cozum=(
            "stok = 10\n"
            "satislar = [2, 3, 4, 5]\n"
            "i = 0\n"
            "while stok > 0 and i < len(satislar):\n"
            "    stok -= satislar[i]\n"
            "    i += 1\n"
            "result = i"
        ),
    ),
]
