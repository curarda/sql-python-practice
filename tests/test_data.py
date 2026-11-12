"""Veri seti testleri: tekrarlanabilirlik, kitapçıkla eşleşen tam sayılar ve SQLite/CSV dönüşümleri."""

import data


def test_ayni_tohum_ayni_veriyi_uretir():
    uretim_1 = data._vaka_uret.__wrapped__()
    uretim_2 = data._vaka_uret.__wrapped__()
    m1, s1 = uretim_1
    m2, s2 = uretim_2
    assert m1.equals(m2)
    assert s1.equals(s2)


def test_tum_tablolar_uretilir():
    t = data.tablolari_uret()
    assert set(t) == {
        "siparisler", "musteriler_kucuk", "kirli", "musteriler", "vaka_siparisler",
        "gunluk_satis", "reklam_satis", "sepet_testi",
    }
    assert t["siparisler"].shape == (10, 8)
    assert t["musteriler_kucuk"].shape == (6, 4)
    assert t["kirli"].shape == (6, 5)
    assert t["musteriler"].shape == (800, 3)
    assert t["vaka_siparisler"].shape[0] == 6030
    assert t["gunluk_satis"].shape == (90, 2)
    assert t["reklam_satis"].shape == (60, 3)
    assert t["sepet_testi"].shape == (600, 2)


def test_siparisler_tablosu_kitapcikla_birebir_ayni():
    df = data.tablolari_uret()["siparisler"]
    assert df["siparis_id"].tolist() == list(range(1001, 1011))
    assert df["birim_fiyat"].sum() == 750 + 2400 + 1100 + 180 + 1900 + 450 + 300 + 520 + 6500 + 350
    assert df["sehir"].value_counts().to_dict() == {"İstanbul": 4, "Ankara": 3, "İzmir": 2, "Bursa": 1}


def test_musteriler_kucuk_c06_eksik_c07_fazladan():
    mk = data.tablolari_uret()["musteriler_kucuk"]
    assert "C06" not in mk["musteri_id"].tolist()
    assert "C07" in mk["musteri_id"].tolist()


def test_kirli_tablo_bilerek_kirli():
    kirli = data.tablolari_uret()["kirli"]
    assert " Müşteri Adı " in kirli.columns
    assert kirli[" Müşteri Adı "].isna().sum() == 1
    assert kirli.duplicated().sum() >= 1  # Can Demir satırları tıpatıp aynı
    assert (kirli["Puan"] > 5).sum() == 2  # 120, 120 -> kural dışı


def test_vaka_siparisler_bilerek_kirli():
    s = data.tablolari_uret()["vaka_siparisler"]
    assert s["tutar"].isna().sum() == 25
    assert (s["tutar"] < 0).sum() == 3
    assert s.duplicated().sum() == 30
    assert s["kategori"].str.contains(" $", regex=True).any(), "büyük harfli/boşluklu kategori kirliliği olmalı"
    import pandas as pd

    assert not pd.api.types.is_datetime64_any_dtype(s["tarih"]), "tarih henüz metin olmalı (gg.aa.yyyy), öğrenci kendisi çevirmeli"
    assert s["tarih"].iloc[0:5].str.match(r"^\d{2}\.\d{2}\.\d{4}$").all()


def test_vaka_musteriler_temiz():
    m = data.tablolari_uret()["musteriler"]
    assert m["musteri_id"].is_unique
    assert m["kayit_tarihi"].dtype.kind == "M"  # datetime


def test_sqlite_baglantisi_tum_tablolari_tasir():
    t = data.tablolari_uret()
    baglanti = data.sqlite_baglantisi_olustur(t)
    try:
        for ad, df in t.items():
            (sayi,) = baglanti.execute(f'SELECT COUNT(*) FROM "{ad}"').fetchone()
            assert sayi == len(df), ad
    finally:
        baglanti.close()


def test_csv_dosyalari_yazilir_ve_vaka_csv_okunabilir(tmp_path):
    import pandas as pd

    yollar = data.csv_dosyalari(tmp_path)
    assert "vaka_siparisler" in yollar and "vaka_musteriler" in yollar
    okunan = pd.read_csv(yollar["vaka_siparisler"], sep=";", decimal=",", encoding="utf-8-sig")
    assert len(okunan) == len(data.tablolari_uret()["vaka_siparisler"])


def test_api_ornegi_ve_kur_json_tanimli():
    assert len(data.API_ORNEGI) == 2
    assert data.API_ORNEGI[0]["musteri"]["ad"] == "Ayşe"
    import json

    kur = json.loads(data.KUR_JSON_METNI)
    assert kur["kurlar"][1]["kod"] == "EUR"
