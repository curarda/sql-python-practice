"""7 günlük müfredat. Her gün kendi dosyasında (gunN.py) tanımlıdır.

Yeni soru eklemek için ilgili günün dosyasındaki SORULAR listesine bir Soru ekleyin.
Soru id'leri benzersiz olmalıdır; testler bunu kontrol eder.
"""

from curriculum import (
    gun1, gun2, gun3, gun4, gun5, gun6, gun7, gun8, gun9, gun10,
    gun11, gun12, gun13, gun14, gun15, gun16, gun17, gun18, gun19, gun20,
    gun21, gun22,
)
from curriculum.models import Ders, Gun, Metrik, Soru

_GUN_MODULLERI = [
    gun1, gun2, gun3, gun4, gun5, gun6, gun7, gun8, gun9, gun10,
    gun11, gun12, gun13, gun14, gun15, gun16, gun17, gun18, gun19, gun20,
    gun21, gun22,
]

# İki üst düzey parkur: "sql" bölümleri burada listelenenler, geri kalan her şey "python".
# SQL parkurundaki görünüm sırası, bölüm numarasından bağımsız olarak burada verilir
# (21/22 yeni eklendi, 15 kitapçıktaki sırada kaldı ama parkur içinde en sona gelir).
_SQL_SIRASI = {21: 1, 22: 2, 15: 3}

GUNLER: list[Gun] = [
    Gun(
        numara=m.DERS.gun,
        baslik=m.DERS.baslik,
        ders=m.DERS,
        sorular=m.SORULAR,
        parkur="sql" if m.DERS.gun in _SQL_SIRASI else "python",
    )
    for m in _GUN_MODULLERI
]

TUM_SORULAR: dict[str, Soru] = {s.id: s for g in GUNLER for s in g.sorular}


def gun_bul(numara: int) -> Gun:
    for gun in GUNLER:
        if gun.numara == numara:
            return gun
    raise KeyError(f"Gün bulunamadı: {numara}")


def parkur_gunleri(parkur: str) -> list[Gun]:
    """Bir parkurdaki (python/sql) bölümleri, o parkurun kendi gösterim sırasına göre döner."""
    gunler = [g for g in GUNLER if g.parkur == parkur]
    if parkur == "sql":
        gunler.sort(key=lambda g: _SQL_SIRASI.get(g.numara, g.numara))
    else:
        gunler.sort(key=lambda g: g.numara)
    return gunler


__all__ = ["GUNLER", "TUM_SORULAR", "gun_bul", "parkur_gunleri", "Ders", "Gun", "Metrik", "Soru"]
