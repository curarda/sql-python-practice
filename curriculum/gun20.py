"""Bölüm 20: Alıştırmalar ve tekrar.

Kitapçığın kendi alıştırma listesi: 1-8 Bölüm 7'deki `siparisler` tablosuyla,
9-11 Bölüm 19'daki `vaka_siparisler` tablosuyla çözülür. Önce denemeden çözüme bakma.
"""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=20,
    baslik="Alıştırmalar ve tekrar",
    anlatim="""
Bu bölüm kitapçığın kendi alıştırma listesidir ve önceki bölümlerin konularını pekiştirir;
her sorunun beklenen sayısal cevabı bellidir, kendi sonucunu onunla karşılaştır.

Mülakatta sık sorulan sorular: `loc` ile `iloc` farkı nedir (Bölüm 8)? `merge` sonrası
satır sayısı arttı, ne olmuş olabilir (Bölüm 11)? Eksik veriyle ne yaparsın (Bölüm 9)?
`groupby+agg` ile `transform` farkı nedir (Bölüm 10)? Ortalama mı medyan mı raporlarsın
(Bölüm 7)? Neden döngü yerine vektörleştirme (Bölüm 6)?

**Stajın ilk haftası kontrol listesi**: Python sürümünü ve `requirements.txt`'i öğren;
veritabanından `SELECT ... LIMIT 10` çalıştırabildiğini gör; Git deposunu klonla, kendi
dalını aç; en sık kullanılan tabloların satır sayısını ve anahtar sütunlarını not al; bir
raporun nasıl üretildiğini öğren; her temizlik adımında satır sayısını yazdır.
""",
    metrikler=[
        Metrik(
            baslik="İyi bir portföy projesi",
            aciklama="Tek bir net soru sorar (ör. 'hangi metro hattı hafta sonu en çok yolcu kaybediyor?'), Bölüm 19'daki adımları izler ve kısa bir özetle biter.",
        ),
    ],
)

SORULAR = [
    Soru(
        id="b20-s01",
        gun=20,
        tur="python",
        kavram="Isınma: fonksiyon",
        anlatim="""
Tekrar: Bölüm 5'teki `def` ve `if` ile erken çıkış kalıbını hatırla — bir fonksiyon,
geçersiz bir girdide (burada `eski == 0`) özel bir değer (`None`) döndürüp hesaba devam
etmeyebilir.
""",
        ornek="""def indirimli_fiyat(fiyat, oran):
    if oran >= 1:
        return None    # %100 ve üzeri indirim anlamsız
    return round(fiyat * (1 - oran), 1)

print([indirimli_fiyat(100, 0.2), indirimli_fiyat(100, 1.5)])    # -> [80.0, None]""",
        ornek_dili="python",
        soru="`buyume(eski, yeni)` fonksiyonunu yaz (b5-s01'deki gibi). Ocak'tan Şubat'a ve Şubat'tan Mart'a ciro değişimini hesapla (aylık cirolar: 5000, 3340, 9790). `result`'a yaz.",
        beklenen="result = [-33.2, 193.1]",
        ipucu="buyume(5000, 3340) ve buyume(3340, 9790).",
        cozum=(
            "def buyume(eski, yeni):\n"
            "    if eski == 0:\n"
            "        return None\n"
            "    return round((yeni - eski) / eski * 100, 1)\n\n"
            "result = [buyume(5000, 3340), buyume(3340, 9790)]"
        ),
    ),
    Soru(
        id="b20-s02",
        gun=20,
        tur="python",
        kavram="Isınma: list comprehension",
        anlatim="""
Tekrar: Bölüm 4'teki comprehension kalıbı `[ifade for eleman in liste if koşul]`. Burada
hem filtrelenmiş listeyi hem de onun toplamını aynı anda istiyorsun — önce comprehension
ile filtrele, sonra `sum()` ile topla.
""",
        ornek="""adetler = [3, 12, 7, 1, 9]
coklar = [a for a in adetler if a > 5]
print(coklar, sum(coklar))    # -> [12, 7, 9] 28""",
        ornek_dili="python",
        soru="`[750, 2400, 1100, 180, 1900]` listesinden 1000'den büyük fiyatları bir list comprehension ile seç. `(secilenler, toplam)` tuple'ını `result`'a yaz.",
        beklenen="result = ([2400, 1100, 1900], 5400)",
        ipucu="buyukler = [f for f in fiyatlar if f > 1000]; sum(buyukler).",
        cozum="fiyatlar = [750, 2400, 1100, 180, 1900]\nbuyukler = [f for f in fiyatlar if f > 1000]\nresult = (buyukler, sum(buyukler))",
    ),
    Soru(
        id="b20-s03",
        gun=20,
        tur="python",
        kavram="pandas temelleri: filtre + toplam",
        anlatim="""
Tekrar: Bölüm 8'deki boolean filtre + Bölüm 10'daki yeni sütun/toplam kalıbı bir arada:
önce `ciro` sütununu türet, sonra bir koşulla filtrele, sonra `.sum()` ile topla.
""",
        ornek="""kucuk = pd.DataFrame({"adet": [1, 3, 2], "birim_fiyat": [100, 50, 200]})
kucuk["ciro"] = kucuk["adet"] * kucuk["birim_fiyat"]
print(kucuk[kucuk["adet"] >= 2]["ciro"].sum())    # -> 550  (3*50=150 ve 2*200=400)""",
        ornek_dili="python",
        soru="`df`'e `ciro` sütununu ekle (`adet * birim_fiyat`). Adedi 2 ve üzeri olan siparişlerin toplam cirosunu `result`'a yaz.",
        beklenen="result = 6230",
        ipucu="df[df['adet'] >= 2]['ciro'].sum()",
        cozum='df["ciro"] = df["adet"] * df["birim_fiyat"]\nresult = int(df[df["adet"] >= 2]["ciro"].sum())',
        tablo="siparisler",
    ),
    Soru(
        id="b20-s04",
        gun=20,
        tur="python",
        kavram="pandas temelleri: groupby + sort",
        anlatim="""
Tekrar: Bölüm 10'daki `groupby(...)['sütun'].sum().sort_values(...)` kalıbı; burada
`ciro` yerine `adet` toplanıyor, geri kalan mantık birebir aynı.
""",
        ornek="""kucuk = pd.DataFrame({"kategori": ["A", "B", "A"], "adet": [3, 1, 5]})
print(kucuk.groupby("kategori")["adet"].sum().sort_values(ascending=False).to_dict())
# -> {'A': 8, 'B': 1}""",
        ornek_dili="python",
        soru="Kategori bazında toplam satılan `adet`i büyükten küçüğe sıralı bir sözlük olarak `result`'a yaz.",
        beklenen="result = {'Elektronik': 9, 'Giyim': 6, 'Kitap': 5}",
        ipucu="df.groupby('kategori')['adet'].sum().sort_values(ascending=False).to_dict()",
        cozum="result = df.groupby('kategori')['adet'].sum().sort_values(ascending=False).to_dict()",
        tablo="siparisler",
    ),
    Soru(
        id="b20-s05",
        gun=20,
        tur="python",
        kavram="pandas temelleri: nlargest",
        anlatim="""
Tekrar: Bölüm 12'deki tarihi datetime'a çevirme + `.dt.month` filtresi, Bölüm 8'deki
`nlargest(n, "sütun")` ile birleşiyor: önce ayı filtrele, sonra en büyük n satırı al.
""",
        ornek="""kucuk = pd.DataFrame({"tarih": pd.to_datetime(["2026-02-01", "2026-03-05", "2026-03-20"]), "urun": ["A", "B", "C"], "ciro": [10, 50, 30]})
mart = kucuk[kucuk["tarih"].dt.month == 3].nlargest(1, "ciro")
print(mart[["urun", "ciro"]].values.tolist())    # -> [['B', 50]]""",
        ornek_dili="python",
        soru="`ciro` sütununu ekle. Mart ayında (tarihi 2026-03 olan) en yüksek cirolu iki siparişin `urun` ve `ciro` değerlerini, `(urun, ciro)` tuple'larından oluşan bir liste olarak `result`'a yaz.",
        beklenen="result = [('Monitör', 6500), ('Tişört', 1200)]",
        ipucu="df['tarih'] önce datetime'a çevrilmeli; .dt.month == 3 ile filtrele, nlargest(2, 'ciro') ile en büyük ikisini al.",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            'df["tarih"] = pd.to_datetime(df["tarih"])\n'
            'mart = df[df["tarih"].dt.month == 3].nlargest(2, "ciro")\n'
            'result = list(mart[["urun", "ciro"]].itertuples(index=False, name=None))'
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b20-s06",
        gun=20,
        tur="python",
        kavram="pandas temelleri: müşteri bazlı agg",
        anlatim="""
Tekrar: Bölüm 10'daki named aggregation, Bölüm 12'deki tarih farkı (`.dt.days`) ile
birleşiyor. Ekstra bir hile: `(sutun > esik).mean()` — bir karşılaştırmanın sonucu
(`True`/`False`) sayısal olarak 1/0 sayıldığı için, ortalaması doğrudan "yüzde kaçı
koşulu sağlıyor?" sorusunun cevabıdır; ayrı bir oran hesabı yazmana gerek kalmaz.
""",
        ornek="""kucuk = pd.DataFrame({"musteri": ["A", "A", "B"], "tarih": pd.to_datetime(["2026-01-01", "2026-01-10", "2026-01-05"])})
m = kucuk.groupby("musteri").agg(siparis=("tarih", "count"), ilk=("tarih", "min"), son=("tarih", "max"))
m["gun_farki"] = (m["son"] - m["ilk"]).dt.days
print((m["siparis"] > 1).mean())    # -> 0.5   (2 müşteriden 1'i birden fazla sipariş verdi)""",
        ornek_dili="python",
        soru=(
            "`ciro` ve datetime `tarih` ekle. Her müşteri için sipariş sayısı, ilk ve son sipariş "
            "tarihi arasındaki gün farkını hesapla. C01'in sipariş sayısını ve gün farkını, ayrıca "
            "birden fazla sipariş vermiş müşterilerin oranını `{'c01_siparis':.., 'c01_gun_farki':.., "
            "'coklu_siparis_orani':..}` biçiminde `result`'a yaz."
        ),
        beklenen="result = {'c01_siparis': 3, 'c01_gun_farki': 82, 'coklu_siparis_orani': 0.5}",
        ipucu="groupby('musteri_id').agg(siparis=('siparis_id','count'), ilk=('tarih','min'), son=('tarih','max')); (son-ilk).dt.days; (siparis>1).mean().",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            'df["tarih"] = pd.to_datetime(df["tarih"])\n'
            "m = df.groupby('musteri_id').agg(siparis=('siparis_id', 'count'), ilk=('tarih', 'min'), son=('tarih', 'max'))\n"
            "m['gun_farki'] = (m['son'] - m['ilk']).dt.days\n"
            "result = {\n"
            "    'c01_siparis': int(m.loc['C01', 'siparis']),\n"
            "    'c01_gun_farki': int(m.loc['C01', 'gun_farki']),\n"
            "    'coklu_siparis_orani': float((m['siparis'] > 1).mean()),\n"
            "}"
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b20-s07",
        gun=20,
        tur="python",
        kavram="pandas temelleri: şehir ortalaması vs genel ortalama",
        anlatim="""
Tekrar: bir grup ortalamasını genel ortalamayla yan yana koymak (Bölüm 7, 10), bir grubun
"ortalamanın üstünde mi altında mı" olduğunu gösterir — rapora yazarken tek başına bir
grup ortalaması yerine her zaman bu kıyası ekle.
""",
        ornek="""kucuk = pd.DataFrame({"sehir": ["A", "A", "B"], "ciro": [100, 300, 50]})
print(kucuk.groupby("sehir")["ciro"].mean().round(0).to_dict(), kucuk["ciro"].mean().round(0))
# -> {'A': 200.0, 'B': 50.0} 150.0""",
        ornek_dili="python",
        soru="`ciro` sütununu ekle. Şehir bazında ortalama sipariş cirosunu ve genel ortalamayı, `{'sehirler': {...}, 'genel': ..}` biçiminde (tam sayıya yuvarlı) `result`'a yaz.",
        beklenen="result = {'sehirler': {'Ankara': 3267, 'Bursa': 1900, 'İstanbul': 1072, 'İzmir': 1070}, 'genel': 1813}",
        ipucu="df.groupby('sehir')['ciro'].mean().round(0) ve df['ciro'].mean().round(0).",
        cozum=(
            'df["ciro"] = df["adet"] * df["birim_fiyat"]\n'
            "sehirler = df.groupby('sehir')['ciro'].mean().round(0).astype(int).to_dict()\n"
            "result = {'sehirler': sehirler, 'genel': int(round(df['ciro'].mean()))}"
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b20-s08",
        gun=20,
        tur="python",
        kavram="pandas temelleri: recency",
        anlatim="""
Tekrar: Bölüm 12'deki tarih aritmetiği. **Recency** (son işlemden bu yana geçen gün),
müşteri analizinde en sık kullanılan ölçütlerden biridir: `(referans_tarih -
son_islem_tarihi).dt.days`. Küçük recency "yakın zamanda aktifti", büyük recency "uzun
süredir görünmüyor" demektir.
""",
        ornek="""kucuk = pd.DataFrame({"musteri": ["A", "B"], "son": pd.to_datetime(["2026-01-20", "2026-01-05"])})
referans = pd.Timestamp("2026-01-25")
fark = (referans - kucuk.set_index("musteri")["son"]).dt.days.sort_values()
print(fark.to_dict())    # -> {'A': 5, 'B': 20}""",
        ornek_dili="python",
        soru="Datetime `tarih` ekle. 31 Mart 2026'yı referans alarak her müşterinin son siparişinden bu yana kaç gün geçtiğini hesapla; en yeniden en eskiye sıralı bir sözlük olarak `result`'a yaz.",
        beklenen="result = {'C01': 3, 'C06': 16, 'C03': 20, 'C05': 28, 'C02': 39, 'C04': 45}",
        ipucu="referans = pd.Timestamp('2026-03-31'); (referans - df.groupby('musteri_id')['tarih'].max()).dt.days.sort_values()",
        cozum=(
            'df["tarih"] = pd.to_datetime(df["tarih"])\n'
            "referans = pd.Timestamp('2026-03-31')\n"
            "fark = (referans - df.groupby('musteri_id')['tarih'].max()).dt.days.sort_values()\n"
            "result = {k: int(v) for k, v in fark.items()}"
        ),
        tablo="siparisler",
    ),
    Soru(
        id="b20-s09",
        gun=20,
        tur="python",
        kavram="Vaka verisi: pivot ile iade oranı",
        anlatim="""
Tekrar: Bölüm 19'daki temizlik adımları + Bölüm 10'daki `pivot_table`. Burada toplam
yerine **oran** (`aggfunc="mean"` bir 0/1 sütununda doğrudan orana dönüşür) iki boyutlu
kırılımda (kategori × kanal) gösteriliyor — bir örüntünün tek bir boyutta mı yoksa her
yerde mi geçerli olduğunu anlamanın yolu budur.
""",
        ornek="""s = vaka_siparisler.copy()
s["kategori"] = s["kategori"].str.strip().str.title()
s = s.drop_duplicates()
s = s[s["tutar"].notna() & (s["tutar"] > 0)]
print(pd.pivot_table(s, values="iade", index="kanal", aggfunc="mean").round(3))
# kanal bazında (kategori ayrımı olmadan) genel iade oranı""",
        ornek_dili="python",
        soru=(
            "`vaka_siparisler`'i temizle (kategori düzelt, tekrarları at, boş/negatif tutarı çıkar). "
            "Kategori × kanal kırılımında ortalama iade oranını (3 ondalık) içeren bir `pivot_table` "
            "kur, `result`'a yaz."
        ),
        beklenen="5 satır (kategori) x 3 sütun (kanal). Giyim'in iade oranı bütün kanallarda diğerlerinden belirgin yüksek (~0.18-0.20).",
        ipucu="pd.pivot_table(s, values='iade', index='kategori', columns='kanal', aggfunc='mean').round(3)",
        cozum=(
            "s = vaka_siparisler.copy()\n"
            "s['kategori'] = s['kategori'].str.strip().str.title()\n"
            "s = s.drop_duplicates()\n"
            "s = s[s['tutar'].notna() & (s['tutar'] > 0)]\n"
            "result = pd.pivot_table(s, values='iade', index='kategori', columns='kanal', aggfunc='mean').round(3)"
        ),
        tablo="vaka_siparisler",
    ),
    Soru(
        id="b20-s10",
        gun=20,
        tur="python",
        kavram="Vaka verisi: takvim etkisi",
        anlatim="""
Tekrar: Bölüm 12'deki takvim etkisi uyarısı. **Toplam** sipariş sayısını hafta içi/hafta
sonu diye karşılaştırmak yanıltır, çünkü bir ayda hafta içi günü hafta sonu gününden
fazladır. Doğru karşılaştırma **günlük ortalamadır**: toplamı, o türden kaç farklı gün
olduğuna (`nunique`) böl.
""",
        ornek="""kucuk = pd.DataFrame({
    "tarih": pd.to_datetime(["2026-01-03", "2026-01-03", "2026-01-05"]),  # 3 Oca Cumartesi, 5 Oca Pazartesi
    "siparis_no": [1, 2, 3],
})
kucuk["hafta_sonu"] = kucuk["tarih"].dt.dayofweek >= 5
hs = kucuk.groupby("hafta_sonu").agg(gun=("tarih", "nunique"), siparis=("siparis_no", "count"))
print((hs["siparis"] / hs["gun"]).round(1).to_dict())    # -> {False: 1.0, True: 2.0}""",
        ornek_dili="python",
        soru=(
            "`vaka_siparisler`'i temizle ve tarihi datetime'a çevir. Hafta içi ve hafta sonu günlerinde "
            "**günlük ortalama** sipariş sayısını (toplam değil; kaç farklı gün olduğuna böl) "
            "`{'hafta_ici':.., 'hafta_sonu':..}` biçiminde (1 ondalık) `result`'a yaz."
        ),
        beklenen="result = {'hafta_ici': 14.5, 'hafta_sonu': 21.0}",
        ipucu="dayofweek >= 5 hafta sonu. groupby(hafta_sonu).agg(gun=('tarih','nunique'), siparis=('siparis_no','count')); siparis/gun.",
        cozum=(
            "s = vaka_siparisler.copy()\n"
            "s['kategori'] = s['kategori'].str.strip().str.title()\n"
            "s = s.drop_duplicates()\n"
            "s = s[s['tutar'].notna() & (s['tutar'] > 0)]\n"
            "s['tarih'] = pd.to_datetime(s['tarih'], format='%d.%m.%Y')\n"
            "s['hafta_sonu'] = s['tarih'].dt.dayofweek >= 5\n"
            "hs = s.groupby('hafta_sonu').agg(gun=('tarih', 'nunique'), siparis=('siparis_no', 'count'))\n"
            "hs['gunluk'] = (hs['siparis'] / hs['gun']).round(1)\n"
            "result = {'hafta_ici': hs.loc[False, 'gunluk'], 'hafta_sonu': hs.loc[True, 'gunluk']}"
        ),
        tablo="vaka_siparisler",
    ),
    Soru(
        id="b20-s11",
        gun=20,
        tur="python",
        kavram="Vaka verisi: oran z-testi",
        anlatim="""
Bölüm 14'te iki **ortalamayı** t-testiyle karşılaştırmıştık; iki **oranı** (ör. iki
kategorinin iade oranı) karşılaştırmak için `statsmodels.stats.proportion.
proportions_ztest` kullanılır. `proportions_ztest([a_sayisi, b_sayisi], [a_toplam,
b_toplam])`, `(z, p)` döndürür. `z`'nin mutlak değeri ne kadar büyükse (ör. 3'ün üstü),
fark o kadar az tesadüfidir; `p` çok küçükse (`0.05`'in çok altında) fark istatistiksel
olarak anlamlıdır.
""",
        ornek="""from statsmodels.stats.proportion import proportions_ztest
a_tiklama, a_toplam = 40, 1000     # A grubunda 1000 gösterimden 40 tıklama
b_tiklama, b_toplam = 90, 1000     # B grubunda 1000 gösterimden 90 tıklama
z, p = proportions_ztest([b_tiklama, a_tiklama], [b_toplam, a_toplam])
print(round(z, 1), p < 0.05)    # -> büyük bir z, anlamlı bir fark""",
        ornek_dili="python",
        soru=(
            "`vaka_siparisler`'i temizle. Giyim kategorisinin iade oranı, diğer kategorilerin toplamından "
            "istatistiksel olarak farklı mı? `statsmodels.stats.proportion.proportions_ztest` ile "
            "z istatistiğini (1 ondalık) `result`'a yaz."
        ),
        beklenen="result = 16.6 (çok büyük bir z değeri; fark tesadüf olamayacak kadar belirgin, p değeri sıfıra çok yakın).",
        ipucu="proportions_ztest([giyim_iade_sayisi, diger_iade_sayisi], [len(giyim), len(diger)]) (z, p) döner.",
        cozum=(
            "from statsmodels.stats.proportion import proportions_ztest\n"
            "s = vaka_siparisler.copy()\n"
            "s['kategori'] = s['kategori'].str.strip().str.title()\n"
            "s = s.drop_duplicates()\n"
            "s = s[s['tutar'].notna() & (s['tutar'] > 0)]\n"
            "giyim = s[s['kategori'] == 'Giyim']\n"
            "diger = s[s['kategori'] != 'Giyim']\n"
            "z, p = proportions_ztest([giyim['iade'].sum(), diger['iade'].sum()], [len(giyim), len(diger)])\n"
            "result = round(float(z), 1)"
        ),
        tablo="vaka_siparisler",
    ),
]
