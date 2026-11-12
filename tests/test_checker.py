"""checker.py birim testleri: doğru, yanlış, sözdizimi, boş sonuç ve boş cevap durumları."""

import pandas as pd
import pytest

import checker
from curriculum import TUM_SORULAR

OZET_3_CUMLE = "Giyimde iade oranı yüksek. Kasım sonu ciroyu belirgin artırıyor. Stok ve kampanya buna göre planlanmalı."


def soru(id_):
    return TUM_SORULAR[id_]


# --- SQL -------------------------------------------------------------------

def test_sql_dogru_cevap_bicim_farkina_ragmen_kabul_edilir():
    cevap = "select sehir, count(*) as siparis, sum(adet*birim_fiyat) as ciro from siparisler group by sehir order by ciro desc"
    sonuc = checker.check(soru("b15-s01"), cevap)
    assert sonuc.dogru, sonuc.mesaj


def test_sql_yanlis_satir_sayisi_geri_bildirim_verir():
    cevap = "SELECT urun, birim_fiyat FROM siparisler WHERE tarih >= '2026-02-01'"  # kategori filtresi eksik
    sonuc = checker.check(soru("b15-s04"), cevap)
    assert not sonuc.dogru
    assert sonuc.kategori == "yanlis"


def test_sql_sozdizimi_hatasi_turkce_mesaj_verir():
    sonuc = checker.check(soru("b15-s01"), "SELEC * FROM siparisler")
    assert sonuc.kategori == "sozdizimi"
    assert "Sözdizimi" in sonuc.mesaj


def test_sql_bilinmeyen_sutun_turkce_mesaj_verir():
    sonuc = checker.check(soru("b15-s01"), "SELECT olmayan_sutun FROM siparisler")
    assert sonuc.kategori == "sozdizimi"
    assert "Sütun bulunamadı" in sonuc.mesaj


def test_sql_bos_cevap():
    sonuc = checker.check(soru("b15-s01"), "   ")
    assert not sonuc.dogru
    assert sonuc.kategori == "bos_cevap"


def test_sql_bos_sonuc_uyarisi():
    sonuc = checker.check(soru("b15-s04"), "SELECT urun, birim_fiyat FROM siparisler WHERE 1=0")
    assert sonuc.kategori == "bos_sonuc"


def test_sql_birden_fazla_sorgu_reddedilir():
    sonuc = checker.check(soru("b15-s01"), "SELECT 1; SELECT 2")
    assert not sonuc.dogru
    assert sonuc.kategori == "sozdizimi"
    assert "bir sorgu" in sonuc.mesaj


def test_sql_siralama_gerekiyorsa_sira_yanlissa_hata_verir():
    cevap = "SELECT sehir, COUNT(*) AS siparis, SUM(adet*birim_fiyat) AS ciro FROM siparisler GROUP BY sehir ORDER BY ciro ASC"
    sonuc = checker.check(soru("b15-s01"), cevap)  # soru azalan sıra istiyor
    assert not sonuc.dogru


def test_sql_siralama_gerekmiyorsa_sira_farki_kabul_edilir():
    cevap = (
        "SELECT musteri_id, tarih, adet * birim_fiyat AS ciro, "
        "ROW_NUMBER() OVER (PARTITION BY musteri_id ORDER BY tarih) AS siparis_sirasi "
        "FROM siparisler WHERE musteri_id IN ('C02', 'C01') ORDER BY musteri_id DESC"
    )
    sonuc = checker.check(soru("b15-s03"), cevap)  # soru sıra istemiyor
    assert sonuc.dogru, sonuc.mesaj


# --- Python / pandas -------------------------------------------------------

def test_python_dogru_cevap():
    s = soru("b2-s01")
    sonuc = checker.check(s, s.cozum)
    assert sonuc.dogru, sonuc.mesaj


def test_python_yanlis_cevap():
    sonuc = checker.check(soru("b2-s01"), "result = 999")
    assert sonuc.kategori == "yanlis"


def test_python_sozdizimi_hatasi_satir_bilgisi_ile():
    sonuc = checker.check(soru("b2-s01"), "result = (1 +")
    assert sonuc.kategori == "sozdizimi"
    assert "Satır" in sonuc.mesaj


def test_python_calisma_hatasi_nameerror_turkce():
    sonuc = checker.check(soru("b2-s01"), "result = bilinmeyen_degisken + 1")
    assert sonuc.kategori == "calisma_hatasi"
    assert "Tanımlı olmayan" in sonuc.mesaj
    assert "Satır 1" in sonuc.mesaj


def test_python_result_tanimlanmamissa_uyari():
    sonuc = checker.check(soru("b2-s01"), "toplam = 20")
    assert sonuc.kategori == "calisma_hatasi"
    assert "result" in sonuc.mesaj


def test_python_bos_cevap():
    sonuc = checker.check(soru("b2-s01"), "")
    assert sonuc.kategori == "bos_cevap"


def test_python_print_ciktisi_yakalanir():
    s = soru("b2-s01")
    sonuc = checker.check(s, "print('merhaba')\n" + s.cozum)
    assert sonuc.dogru
    assert "merhaba" in sonuc.cikti


def test_python_dataframe_bos_sonuc():
    sonuc = checker.check(soru("b19-s03"), "result = pd.DataFrame(columns=['kategori', 'siparis'])")
    assert sonuc.kategori == "bos_sonuc"


def test_python_df_kopyasi_orijinal_veriyi_bozmaz():
    s = soru("b7-s01")
    kod = "df.drop(df.index, inplace=True)\nresult = df.shape"
    sonuc = checker.check(s, kod)
    assert sonuc.kategori == "yanlis"
    kontrol = checker.check(s, s.cozum)
    assert kontrol.dogru, "orijinal veri değişmemeli, referans hâlâ doğru çalışmalı"


def test_python_ozet_gerekli_soruda_ozet_eksikse_kabul_edilmez():
    s = soru("b19-s06")
    sonuc = checker.check(s, s.cozum, "Kısa.")
    assert sonuc.kategori == "ozet_eksik"


def test_python_ozet_gerekli_soruda_dogru_kod_ve_ozet_kabul_edilir():
    s = soru("b19-s06")
    sonuc = checker.check(s, s.cozum, OZET_3_CUMLE)
    assert sonuc.dogru, sonuc.mesaj


# --- Karşılaştırma yardımcıları -------------------------------------------

@pytest.mark.parametrize(
    "a,b,beklenen",
    [
        (0.1, 0.105, True),
        (0.1, 0.12, False),
        (5, 5.0, True),
        (None, float("nan"), True),
        ("a", "A", False),
    ],
)
def test_karsilastir_skalerler(a, b, beklenen):
    esit, _ = checker.karsilastir(a, b)
    assert esit == beklenen


def test_karsilastir_dataframe_sutun_adi_farkli_ise_yanlis():
    beklenen = pd.DataFrame({"kategori": ["Giyim"], "sayi": [1]})
    kullanici = pd.DataFrame({"kategori": ["Giyim"], "adet": [1]})
    esit, ayrinti = checker.karsilastir(kullanici, beklenen)
    assert not esit
    assert "Sütunlar" in ayrinti[0]


def test_karsilastir_siralama_onemsiz_ama_sirali_modda_onemli():
    beklenen = pd.DataFrame({"a": [1, 2]})
    kullanici = pd.DataFrame({"a": [2, 1]})
    assert checker.karsilastir(kullanici, beklenen, sirali=False)[0]
    assert not checker.karsilastir(kullanici, beklenen, sirali=True)[0]


def test_karsilastir_series_sirasiz_karsilastirilir():
    beklenen = pd.Series([3, 1, 2], index=["Giyim", "Elektronik", "Kitap"])
    kullanici = pd.Series([1, 2, 3], index=["Elektronik", "Kitap", "Giyim"])
    assert checker.karsilastir(kullanici, beklenen)[0]


def test_sql_hata_cevirici_bilinmeyen_hatayi_da_gosterir():
    mesaj = checker.sql_hatasini_cevir(RuntimeError("baska bir sey"))
    assert "baska bir sey" in mesaj
