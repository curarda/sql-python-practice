"""Müfredat tutarlılığı: her referans çözüm kendi kontrolünden geçmeli, sorular yeterli ve benzersiz olmalı."""

import checker
from curriculum import GUNLER, TUM_SORULAR

OZET = "Giyimde iade oranı yüksek. Kasım sonu ciroyu belirgin artırıyor. Stok ve kampanya buna göre planlanmalı."


def test_yirmi_bolum_var_ve_her_bolumde_en_az_iki_soru():
    assert len(GUNLER) == 20
    assert [g.numara for g in GUNLER] == list(range(1, 21))
    for gun in GUNLER:
        assert len(gun.sorular) >= 2, f"Bölüm {gun.numara} en az 2 soru içermeli"


def test_toplam_soru_sayisi_makul():
    assert len(TUM_SORULAR) >= 60


def test_soru_kimlikleri_benzersiz():
    kimlikler = [s.id for g in GUNLER for s in g.sorular]
    assert len(kimlikler) == len(set(kimlikler))


def test_her_soru_alanlari_dolu_ve_turu_gecerli():
    for soru in TUM_SORULAR.values():
        assert soru.tur in {"sql", "python"}, soru.id
        assert soru.soru.strip() and soru.beklenen.strip() and soru.ipucu.strip(), soru.id
        assert soru.cozum.strip(), soru.id
        assert soru.kavram.strip(), soru.id


def test_her_bolumun_anlatimi_ve_dikkat_cekici_notu_var():
    for gun in GUNLER:
        assert gun.ders.anlatim.strip(), f"Bölüm {gun.numara} anlatımı boş"
        assert gun.ders.metrikler, f"Bölüm {gun.numara} dikkat çekici notu yok"


def test_her_referans_cozum_kendi_kontrolunden_gecer():
    for soru in TUM_SORULAR.values():
        ozet = OZET if soru.ozet_gerekli else None
        sonuc = checker.check(soru, soru.cozum, ozet)
        assert sonuc.dogru, f"{soru.id}: {sonuc.mesaj} {sonuc.detay}"


def test_referans_sonuclari_hatasiz_calisir():
    for soru in TUM_SORULAR.values():
        if soru.tur == "sql":
            sonuc = checker.run_sql(soru.cozum)
            assert not sonuc.empty, f"{soru.id} boş sonuç döndürüyor"
        else:
            sonuc, _, hata = checker.run_python(soru.cozum, soru.tablo)
            assert hata is None, f"{soru.id}: {hata}"


def test_bos_veya_yanlis_cevap_hicbir_soruda_dogru_sayilmaz():
    for soru in TUM_SORULAR.values():
        cevap = "SELECT 1 AS yanlis" if soru.tur == "sql" else "result = 'yanlış cevap'"
        sonuc = checker.check(soru, cevap, OZET)
        assert not sonuc.dogru, soru.id


def test_vaka_csv_dosyasi_ile_tablo_satir_sayisi_ayni():
    import data

    sonuc, _, hata = checker.run_python(
        "result = len(pd.read_csv(VAKA_SIPARISLER_CSV, sep=';', decimal=','))", "vaka_siparisler"
    )
    assert hata is None
    assert sonuc == len(data.tablolari_uret()["vaka_siparisler"])
