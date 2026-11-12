"""Bölüm 20: Alıştırmalar ve tekrar.

Kitapçığın kendi alıştırma listesi: 1-8 Bölüm 7'deki `siparisler` tablosuyla,
9-11 Bölüm 19'daki `vaka_siparisler` tablosuyla çözülür. Önce denemeden çözüme bakma.
"""

from curriculum.models import Ders, Metrik, Soru

DERS = Ders(
    gun=20,
    baslik="Alıştırmalar ve tekrar",
    anlatim="""
Bu bölüm kitapçığın kendi alıştırma listesidir; her sorunun beklenen sayısal cevabı
bellidir, kendi sonucunu onunla karşılaştır. **Isınma** (Bölüm 2-5) ve **pandas temelleri**
(Bölüm 7-10) soruları `siparisler` tablosuyla, **vaka verisi** (Bölüm 9-14, 19) soruları
`vaka_siparisler` ile çözülür.

Mülakatta sık sorulan sorular: `loc` ile `iloc` farkı nedir? `merge` sonrası satır sayısı
arttı, ne olmuş olabilir? Eksik veriyle ne yaparsın? `groupby+agg` ile `transform` farkı
nedir? Ortalama mı medyan mı raporlarsın? Neden döngü yerine vektörleştirme?

**Stajın ilk haftası kontrol listesi**: Python sürümünü ve `requirements.txt`'i öğren;
veritabanından `SELECT ... LIMIT 10` çalıştırabildiğini gör; Git deposunu klonla, kendi
dalını aç; en sık kullanılan tabloların satır sayısını ve anahtar sütunlarını not al; bir
raporun nasıl üretildiğini öğren; her temizlik adımında satır sayısını yazdır.
""",
    ornek="""# (m["siparis"] > 1).mean() hilesi: True 1, False 0 sayıldığı için
# bir doğru/yanlış sütununun ortalaması doğrudan "yüzde kaçı" sorusunun cevabıdır.""",
    ornek_dili="python",
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
