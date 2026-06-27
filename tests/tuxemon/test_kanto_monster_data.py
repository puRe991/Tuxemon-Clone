from __future__ import annotations

from pathlib import Path

import yaml

from tuxemon.database.runtime import db
from tuxemon.locale.locale import T


KANTO_ABRA_PATH = Path("mods/tuxemon/db/monster/kanto_abra.yaml")
BASE_PO_PATH = Path("mods/tuxemon/l18n/en_US/LC_MESSAGES/base.po")


def test_kanto_abra_uses_existing_battle_sprite() -> None:
    """The Kanto Abra record must not rely on a generated missing sheet."""
    data = yaml.safe_load(KANTO_ABRA_PATH.read_text(encoding="utf-8"))

    assert data["sprites"]["sheet"] == "gfx/sprites/battle/missing"
    assert Path(f"mods/tuxemon/{data['sprites']['sheet']}.png").is_file()


def test_kanto_region_archive_translation_is_available() -> None:
    """Keep both generic and MonsterModel category translation keys present."""
    base_po = BASE_PO_PATH.read_text(encoding="utf-8")

    assert 'msgid "kanto_region_archive"' in base_po
    assert 'msgid "cat_kanto_region_archive"' in base_po

    T.initialize_translations(recompile=True)
    assert T.translate("cat_kanto_region_archive") != "cat_kanto_region_archive"


def test_kanto_abra_validates_with_mod_database() -> None:
    """Regression coverage for startup validation of the Kanto Abra entry."""
    T.initialize_translations(recompile=True)
    db.load()

    model = db.lookup("kanto_abra", table="monster")
    assert model.species == "kanto_region_archive"
    assert model.sprites.sheet == "gfx/sprites/battle/missing"
