# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2026 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
from __future__ import annotations

from dataclasses import dataclass
from typing import final

from tuxemon.event.actions.open_journal import OpenJournalAction


@final
@dataclass
class OpenPokedexAction(OpenJournalAction):
    """
    Compatibility alias for ``open_journal`` using the common Pokédex term.

    Script usage:
        .. code-block::

            open_pokedex <monster_slug>
    """

    name = "open_pokedex"
