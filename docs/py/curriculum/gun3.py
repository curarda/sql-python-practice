"""Bölüm 3: Veri yapıları — list, tuple, dict, set."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=3,
    baslik="Veri yapıları",
    anlatim="""
- **list** `[1, 2, 3]`: sıralı, değiştirilebilir koleksiyon. `.append()`, `[i]` ile erişim.
- **tuple** `(1, 2)`: list gibi ama değiştirilemez; genelde sabit bir ikili/üçlü için kullanılır.
- **dict** `{"anahtar": değer}`: anahtar-değer eşleşmesi. `d["k"]`, `d.get("k", varsayılan)`,
  `d.keys()/.values()/.items()`.
- **set** `{1, 2, 3}`: benzersiz değerler, sırasız. Küme işlemleri: `a & b` (kesişim),
  `a | b` (birleşim), `a - b` (fark). İki listedeki ortak elemanları bulmanın en hızlı yolu.

**Önemli tuzak**: `liste2 = liste1` kopya oluşturmaz, aynı nesneyi gösteren ikinci bir isimdir.
`liste2.append(...)` yaparsan `liste1` de değişir. Gerçek bir kopya için `liste1.copy()` ya
da `list(liste1)` kullan. Bu tuzak pandas'ta da vardır: `df2 = df` değil, `df2 = df.copy()`.
""",
    ornek="""sepet = {"Kulaklık": 750, "Mont": 2400, "Roman": 180}
en_pahali = max(sepet, key=sepet.get)       # değere göre en büyük anahtar
print(en_pahali, sepet[en_pahali])          # -> Mont 2400""",
    ornek_dili="python",
    metrikler=[
        Metrik(
            baslik="Şaşırtıcı tuzak",
            aciklama="liste2 = liste1 bir kopya değil, aynı listeye ikinci bir isimdir. liste2'yi değiştirirsen liste1 de değişir.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b3-s01",
        gun=3,
        tur="python",
        kavram="dict ve max(key=...)",
        soru='`sepet = {"Kulaklık": 750, "Mont": 2400, "Roman": 180}` sözlüğünde en pahalı ürünün adını ve fiyatını bir `(ad, fiyat)` tuple\'ı olarak `result`\'a yaz.',
        beklenen="result = ('Mont', 2400)",
        ipucu="max(sepet, key=sepet.get) sözlükte değeri en büyük olan anahtarı verir.",
        cozum='sepet = {"Kulaklık": 750, "Mont": 2400, "Roman": 180}\nen_pahali = max(sepet, key=sepet.get)\nresult = (en_pahali, sepet[en_pahali])',
    ),
    Soru(
        id="b3-s02",
        gun=3,
        tur="python",
        kavram="set ve kesişim",
        soru='`istanbul_musteri = {"C01", "C02", "C03"}` ve `ankara_musteri = {"C02", "C04"}` kümelerinin kesişimini (her iki şehirden de sipariş veren ortak müşteriler), alfabetik sıralı bir liste olarak `result`\'a yaz.',
        beklenen="result = ['C02']",
        ipucu="& operatörü iki kümenin kesişimini verir; sorted() ile sırala.",
        cozum='istanbul_musteri = {"C01", "C02", "C03"}\nankara_musteri = {"C02", "C04"}\nresult = sorted(istanbul_musteri & ankara_musteri)',
    ),
    Soru(
        id="b3-s03",
        gun=3,
        tur="python",
        kavram="Kopya değil, aynı nesne",
        soru='`liste1 = [1, 2, 3]` tanımla. `liste2 = liste1` yaz, sonra `liste2.append(4)` çağır. `liste1`\'in son hâlini `result`\'a yaz.',
        beklenen="result = [1, 2, 3, 4]",
        ipucu="liste2, liste1'in kopyası değil aynı nesnesidir; liste2'deki değişiklik liste1'de de görünür.",
        cozum="liste1 = [1, 2, 3]\nliste2 = liste1\nliste2.append(4)\nresult = liste1",
    ),
]
