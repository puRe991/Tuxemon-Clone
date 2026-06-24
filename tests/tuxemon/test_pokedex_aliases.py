# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2026 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
from __future__ import annotations

from tuxemon.event.eventaction import ActionManager
from tuxemon.event.eventcondition import ConditionManager


def test_pokedex_action_aliases_are_registered():
    actions = ActionManager().actions

    assert actions["set_pokedex"].name == "set_pokedex"
    assert actions["clear_pokedex"].name == "clear_pokedex"
    assert actions["open_pokedex"].name == "open_pokedex"


def test_pokedex_condition_aliases_are_registered():
    conditions = ConditionManager().conditions

    assert conditions["has_pokedex"].name == "has_pokedex"
    assert conditions["pokedex"].name == "pokedex"
