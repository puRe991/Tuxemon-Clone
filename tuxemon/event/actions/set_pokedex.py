# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2026 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
from __future__ import annotations

from dataclasses import dataclass
from typing import final

from tuxemon.event.actions.set_tuxepedia import SetTuxepediaAction


@final
@dataclass
class SetPokedexAction(SetTuxepediaAction):
    """
    Compatibility alias for ``set_tuxepedia`` using the common Pokédex term.

    Script usage:
        .. code-block::

            set_pokedex <character>,<monster_slug>,<label>

    Script parameters are identical to ``set_tuxepedia``.
    """

    name = "set_pokedex"
