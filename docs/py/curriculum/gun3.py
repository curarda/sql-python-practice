"""Bölüm 3: Veri yapıları — list, tuple, dict, set."""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=3,
    baslik="Veri yapıları",
    anlatim=(
        "Bu bölümde dört temel koleksiyon tipini (list, tuple, dict, set) ve Python'da en "
        "sinsi tuzaklardan birini (bir listeyi kopyaladığını sanıp aslında aynı nesneyi "
        "paylaşmak) öğreneceksin."
    ),
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
        anlatim="""
- **list** `[1, 2, 3]`: sıralı, değiştirilebilir bir koleksiyondur. `.append(x)` sona ekler,
  `liste[i]` ile bir elemana erişirsin.
- **tuple** `(1, 2)`: list gibi ama değiştirilemez (immutable); genelde sabit bir ikili/üçlü
  için kullanılır, örn. `(ad, fiyat)`.
- **dict** `{"anahtar": değer}`: anahtar-değer eşleşmesidir. `d["k"]` değere erişir,
  `d.get("k", varsayılan)` anahtar yoksa hata vermez, `d.keys()/.values()/.items()` sırasıyla
  anahtarları/değerleri/çiftleri verir.

Bir sözlükte **değere göre** en büyük/küçük anahtarı bulmak için `max`/`min`'in `key=`
parametresi kullanılır: `max(d, key=d.get)` değeri en büyük olan anahtarı döndürür (anahtarın
kendisini, değerini değil).
""",
        ornek="""fiyatlar = {"Kulaklık": 750, "Mont": 2400, "Roman": 180}
en_ucuz = min(fiyatlar, key=fiyatlar.get)
print(en_ucuz, fiyatlar[en_ucuz])      # -> Roman 180""",
        ornek_dili="python",
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
        anlatim="""
**set** `{1, 2, 3}`: benzersiz değerlerden oluşan, sırasız bir koleksiyondur — aynı değeri
iki kez eklesen de kümede bir kez durur. Küme işlemleri iki listeyi karşılaştırmanın en
hızlı yoludur: `a & b` **kesişim** (ikisinde de olanlar), `a | b` **birleşim** (ikisinde
olan her şey), `a - b` **fark** (a'da olup b'de olmayanlar).
""",
        ornek="""elektronik_alanlar = {"C01", "C03", "C05"}
giyim_alanlar = {"C02", "C03"}
print(sorted(elektronik_alanlar & giyim_alanlar))   # -> ['C03'] (her iki kategoriden de almış)""",
        ornek_dili="python",
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
        anlatim="""
**Önemli tuzak**: `liste2 = liste1` bir kopya oluşturmaz; `liste2` yalnızca aynı nesneyi
gösteren **ikinci bir isimdir**. `liste2.append(...)` yaparsan `liste1` de değişir, çünkü
ikisi de bellekte aynı listeyi işaret eder. Gerçek bir kopya için `liste1.copy()` ya da
`list(liste1)` kullanman gerekir. Bu tuzak pandas'ta da vardır: `df2 = df` değil,
`df2 = df.copy()` yazman gerekir (Bölüm 7).
""",
        ornek="""orijinal = [10, 20]
kopya = orijinal.copy()     # .copy() ile GERÇEK bir kopya
kopya.append(30)
print(orijinal, kopya)      # -> [10, 20] [10, 20, 30]  (orijinal etkilenmedi)""",
        ornek_dili="python",
        soru='`liste1 = [1, 2, 3]` tanımla. `liste2 = liste1` yaz, sonra `liste2.append(4)` çağır. `liste1`\'in son hâlini `result`\'a yaz.',
        beklenen="result = [1, 2, 3, 4]",
        ipucu="liste2, liste1'in kopyası değil aynı nesnesidir; liste2'deki değişiklik liste1'de de görünür.",
        cozum="liste1 = [1, 2, 3]\nliste2 = liste1\nliste2.append(4)\nresult = liste1",
    ),
]
