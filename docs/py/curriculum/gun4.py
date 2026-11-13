"""Bölüm 4: Kontrol akışı — if, for, while, comprehension."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=4,
    baslik="Kontrol akışı",
    anlatim=(
        "Bu bölümde if/elif/else ile dallanmayı, for ve while döngülerini, bir döngüyü tek "
        "satırda yazan comprehension'ı ve pandas varken ne zaman hâlâ döngü yazman gerektiğini "
        "öğreneceksin."
    ),
    metrikler=[
        Metrik(
            baslik="Kısa kural",
            aciklama="Basit bir filtre/dönüşümse comprehension yaz; birden çok adım ve okunabilirlik gerekiyorsa normal for döngüsüne geç. pandas varken satır satır döngü yerine vektörleştirilmiş işlem tercih et (Bölüm 6, 8).",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b4-s01",
        gun=4,
        tur="python",
        kavram="if / elif / else",
        anlatim="""
`if / elif / else`, koşula göre dallanma sağlar. Koşul bir karşılaştırma (`x > 5`) ya da
bir truthiness kontrolü (`if liste:`) olabilir. Birden çok dalı sırayla kontrol etmek için
`elif` kullanılır; ilk doğru olan dal çalışır, geri kalanlar atlanır. Bir sınıflandırmayı
birden fazla yerde tekrar kullanacaksan, onu bir fonksiyona yazıp `for`/comprehension ile
her elemana uygulamak tekrarı önler.
""",
        ornek="""def hiz_sinifi(km_saat):
    if km_saat < 50:
        return "Yavaş"
    if km_saat <= 90:
        return "Normal"
    return "Hızlı"

print([hiz_sinifi(h) for h in [30, 70, 120]])   # -> ['Yavaş', 'Normal', 'Hızlı']""",
        ornek_dili="python",
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
        anlatim="""
`for eleman in koleksiyon:` bir listeyi, sözlüğü ya da aralığı (`range(n)`) dolaşır. İki
listeyi **eş zamanlı** dolaşmak istediğinde (ör. ürün adları ve fiyatları aynı sırada)
`zip(liste1, liste2)` kullanılır; her adımda bir çiftin ikisini de verir.

**Comprehension**, bir döngüyü tek satırda yazmanın yoludur: `[ifade for eleman in liste
if koşul]`. `zip` ile birlikte kullanınca `[a for a, b in zip(liste1, liste2) if b > x]`
gibi "ikinci listeye göre filtrelenmiş birinci liste" kalıpları çok kısa yazılır.
""",
        ornek="""fiyatlar = [750, 2400, 1100, 180, 1900]
pahalilar = [f for f in fiyatlar if f > 1000]
print(pahalilar, sum(pahalilar))     # -> [2400, 1100, 1900] 5400""",
        ornek_dili="python",
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
        anlatim="""
`while koşul:` koşul doğru olduğu sürece tekrar eder. `for`'un aksine kaç kez
tekrarlanacağını önceden bilmediğin durumlarda kullanılır (ör. "stok bitene kadar").
Döngünün bir yerde durması için koşulu güncelleyen bir satır (ör. bir sayaç artırma)
mutlaka olmalı — yoksa döngü **sonsuza kadar** çalışır. Erken çıkmak için `break`
kullanılabilir.

**pandas varken döngü yazmalı mıyım?** Çoğu zaman hayır: pandas'ın vektörleştirilmiş
işlemleri (Bölüm 6, 8) aynı işi satır satır döngüden çok daha hızlı yapar. Döngü, pandas'ın
doğrudan karşılığı olmayan özel bir mantık gerektiğinde (bu alıştırmadaki gibi, "stok ne
zaman biter" sorusunda) tercih edilir.
""",
        ornek="""hedef = 20
toplam = 0
sayac = 0
degerler = [5, 8, 9, 3]
while toplam < hedef and sayac < len(degerler):
    toplam += degerler[sayac]
    sayac += 1
print(sayac, toplam)   # -> 3 22  (5+8+9=22, 20'yi ilk geçtiği an durdu)""",
        ornek_dili="python",
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
