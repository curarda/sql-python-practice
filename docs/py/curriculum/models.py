"""Müfredat veri modelleri. Yeni soru ya da gün eklemek için bu yapıları kullanın."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Soru:
    """Tek bir alıştırma.

    id:           benzersiz kimlik, ör. "b1-s01"
    tur:          "sql" veya "python" (python = pandas dahil)
    kavram:       bu noktanın kısa başlığı; zayıf konu raporunda da gösterilir, ör. "GROUP BY"
    anlatim:      bu tek noktanın kısa açıklaması (Markdown). Soru gösterilmeden önce okunur.
    ornek:        anlatımın hemen altında gösterilen, soruyla aynı sayıları KULLANMAYAN örnek kod
    ornek_dili:   "python" veya "sql" (örnek kodun söz dizimi vurgusu için)
    soru:         kullanıcıya gösterilen soru metni
    beklenen:     beklenen çıktının açıklaması (sütunlar, sıralama, biçim)
    ipucu:        ipucu butonunda gösterilir
    cozum:        referans çözüm (SQL sorgusu veya Python kodu); karşılaştırma buna göre yapılır
    tablo:        Python sorularında `df` olarak yüklenecek tablo
    sirali:       True ise satır sırası da kontrol edilir
    ozet_gerekli: True ise kullanıcıdan 3 cümlelik ürün özeti de istenir

    Akış: önce `anlatim` + `ornek` okunur (öğren), sonra `soru` yazılıp Çalıştır/Kontrol
    edilir (dene). `ornek` hiçbir zaman `soru`nun doğrudan çözümü olmamalı; aynı kalıbı
    farklı bir örnekle göstermelidir.
    """

    id: str
    gun: int
    tur: str
    kavram: str
    anlatim: str
    soru: str
    beklenen: str
    ipucu: str
    cozum: str
    ornek: str = ""
    ornek_dili: str = "python"
    tablo: str = "siparisler"
    sirali: bool = False
    ozet_gerekli: bool = False
    kirlilik: str = ""  # vakada bilinçli veri sorunu; "Veri notu" olarak gizli açılır
    rubrik: str = ""  # 3 cümlelik ürün özeti için değerlendirme ölçütleri (vaka sorularında)


@dataclass(frozen=True)
class Metrik:
    baslik: str
    aciklama: str


@dataclass(frozen=True)
class Ders:
    """Bölümün kısa girişi. Asıl anlatım artık her Soru'nun kendi `anlatim`+`ornek` alanında;
    bu, bölüm sayfasının en üstünde gösterilen 2-4 cümlelik bir özet/giriştir."""

    gun: int
    baslik: str
    anlatim: str
    ornek: str = ""
    ornek_dili: str = "sql"
    metrikler: list[Metrik] = field(default_factory=list)


@dataclass(frozen=True)
class Gun:
    numara: int
    baslik: str
    ders: Ders
    sorular: list[Soru]
