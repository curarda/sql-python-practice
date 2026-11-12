"""7 günlük müfredat. Her gün kendi dosyasında (gunN.py) tanımlıdır.

Yeni soru eklemek için ilgili günün dosyasındaki SORULAR listesine bir Soru ekleyin.
Soru id'leri benzersiz olmalıdır; testler bunu kontrol eder.
"""

from curriculum import (
    gun1, gun2, gun3, gun4, gun5, gun6, gun7, gun8, gun9, gun10,
    gun11, gun12, gun13, gun14, gun15, gun16, gun17, gun18, gun19, gun20,
)
from curriculum.models import Ders, Gun, Metrik, Soru

_GUN_MODULLERI = [
    gun1, gun2, gun3, gun4, gun5, gun6, gun7, gun8, gun9, gun10,
    gun11, gun12, gun13, gun14, gun15, gun16, gun17, gun18, gun19, gun20,
]

GUNLER: list[Gun] = [
    Gun(numara=m.DERS.gun, baslik=m.DERS.baslik, ders=m.DERS, sorular=m.SORULAR)
    for m in _GUN_MODULLERI
]

TUM_SORULAR: dict[str, Soru] = {s.id: s for g in GUNLER for s in g.sorular}


def gun_bul(numara: int) -> Gun:
    for gun in GUNLER:
        if gun.numara == numara:
            return gun
    raise KeyError(f"Gün bulunamadı: {numara}")


__all__ = ["GUNLER", "TUM_SORULAR", "gun_bul", "Ders", "Gun", "Metrik", "Soru"]
