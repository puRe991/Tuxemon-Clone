# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2026 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
from __future__ import annotations

from dataclasses import dataclass
from typing import final

from tuxemon.event.actions.clear_tuxepedia import ClearTuxepediaAction


@final
@dataclass
class ClearPokedexAction(ClearTuxepediaAction):
    """
    Compatibility alias for ``clear_tuxepedia`` using the common Pokédex term.

    Script usage:
        .. code-block::

            clear_pokedex [monster_slug]
    """

    name = "clear_pokedex"
