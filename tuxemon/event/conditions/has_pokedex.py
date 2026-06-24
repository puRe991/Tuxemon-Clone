# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2026 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from tuxemon.event.conditions.has_tuxepedia import HasTuxepediaCondition


@dataclass
class HasPokedexCondition(HasTuxepediaCondition):
    """
    Compatibility alias for ``has_tuxepedia`` using the common Pokédex term.

    Script usage:
        .. code-block::

            is has_pokedex <character>,<monster>,<label>
    """

    name: ClassVar[str] = "has_pokedex"
