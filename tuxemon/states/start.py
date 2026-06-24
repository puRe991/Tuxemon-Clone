# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2026 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
"""This module contains the Start state."""

from __future__ import annotations

import logging
from collections.abc import Callable
from functools import partial
from typing import TYPE_CHECKING, Any, ClassVar

from pygame.surface import Surface
from pygame_menu.locals import ALIGN_CENTER, POSITION_EAST
from pygame_menu.menu import Menu
from pygame_menu.widgets.core.widget import Widget

from tuxemon.database.runtime import db
from tuxemon.entity.npc import NPC
from tuxemon.launcher import GameLauncher
from tuxemon.locale.locale import T
from tuxemon.menu.menu import PygameMenuState
from tuxemon.platform.const.graphics import BG_START_SCREEN, BLACK_COLOR
from tuxemon.platform.const.sizes import PLAYER_NPC
from tuxemon.save_system.save import get_index_of_latest_save
from tuxemon.save_system.save_manager import SaveManager
from tuxemon.session import local_session
from tuxemon.state.state import State
from tuxemon.tools import open_dialog

if TYPE_CHECKING:
    from tuxemon.base_client import BaseClient

logger = logging.getLogger(__name__)


class BackgroundState(State):
    """
    Background state is used to prevent other states from
    being required to track dirty screen areas. For example,
    in the start state, there is a menu on a blank background,
    since menus do not clean up dirty areas, the blank,
    "Background state" will do that. The alternative is creating
    a system for states to clean up their dirty screen areas.

    Eventually the need for this will be phased out.
    """

    name: ClassVar[str] = "BackgroundState"

    def __init__(self, client: BaseClient, *args: Any, **kwargs: Any):
        super().__init__(client, *args, **kwargs)

    def draw(self, surface: Surface) -> None:
        surface.fill(BLACK_COLOR)


class StartState(PygameMenuState):
    """The state responsible for the start menu."""

    name: ClassVar[str] = "StartState"

    def _add_button(
        self,
        menu: Menu,
        *,
        title_key: str,
        action: Callable[[], None],
        button_id: str,
    ) -> Widget:
        """Add a consistently styled start-menu button."""
        return menu.add.button(
            title=T.translate(title_key),
            action=action,
            font_size=self.font_type.big,
            button_id=button_id,
        )

    def _add_header(self, menu: Menu) -> None:
        """Add a short call-to-action that frames starting the journey."""
        menu.add.label(
            T.translate("menu_start_title"),
            font_size=self.font_type.bigger,
        )
        menu.add.label(
            T.translate("menu_start_subtitle"),
            font_size=self.font_type.small,
        )
        menu.add.vertical_margin(self.client.context.scaling.scale_int(8))

    def _unsubscribe_afk(self) -> None:
        self.unsubscribe("afk.threshold_reached", self._on_afk_threshold)

    def add_menu_items(
        self,
        menu: Menu,
    ) -> None:
        # If there is a save, keep the continuation path at the top.
        index = get_index_of_latest_save()

        def new_game() -> None:
            self._unsubscribe_afk()
            if not self.client.config.mods:
                logger.error("Cannot start a new game without an active mod.")
                open_dialog(self.client, [T.translate("menu_no_mods")])
                return

            launcher = GameLauncher(self.client)
            launcher.launch(
                session=local_session,
                meta=db.mod_metadata.get_mod_metadata(
                    self.client.config.mods[0]
                ),
                remove_states=["StartState"],
            )

        def change_state(
            state: State | str, **kwargs: Any
        ) -> Callable[[], None]:
            def _change() -> None:
                self._unsubscribe_afk()
                self.client.push_state(state, **kwargs)

            return _change

        def load_autosave() -> None:
            self._unsubscribe_afk()
            self.client.event_engine.execute_action(
                "load_game", [0, True], True
            )

        def exit_game() -> None:
            self._unsubscribe_afk()
            self.client.quit()

        self._add_header(menu)

        if index is not None:
            self._add_button(
                menu,
                title_key="menu_continue_journey",
                action=change_state("LoadMenuState"),
                button_id="menu_load",
            )

            if SaveManager.has_autosave():
                self._add_button(
                    menu,
                    title_key="menu_autosave",
                    action=load_autosave,
                    button_id="menu_autosave",
                )

        if len(self.client.config.mods) == 1:
            self._add_button(
                menu,
                title_key="menu_begin_journey",
                action=new_game,
                button_id="menu_new_game",
            )
        else:
            self._add_button(
                menu,
                title_key="menu_begin_journey",
                action=change_state(
                    "ModsChoice", mods=self.client.config.mods
                ),
                button_id="menu_mod_choice",
            )
        self._add_button(
            menu,
            title_key="menu_battle",
            action=change_state(
                "DifficultyPickState", on_pick=self.start_battle
            ),
            button_id="menu_battle",
        )
        self._add_button(
            menu,
            title_key="menu_minigame",
            action=change_state(
                "DifficultyPickState",
                on_pick=self.start_minigame,
                difficulties=["easy", "normal", "hard"],
            ),
            button_id="menu_minigame",
        )
        self._add_button(
            menu,
            title_key="menu_options",
            action=change_state("ControlState", main_menu=True),
            button_id="menu_options",
        )
        self._add_button(
            menu,
            title_key="exit",
            action=exit_game,
            button_id="exit",
        )

    def __init__(self, client: BaseClient, **kwargs: Any) -> None:
        width, height = client.context.resolution

        super().__init__(client=client, height=height, width=width, **kwargs)

        theme = self._setup_theme(BG_START_SCREEN)
        theme.scrollarea_position = POSITION_EAST
        theme.widget_alignment = ALIGN_CENTER
        self._menu_config["theme"] = theme

        self.escape_key_exits = False
        self.client.afk_manager.add_threshold("IntroState", 15.0)
        self.event_bus.subscribe(
            "afk.threshold_reached", self._on_afk_threshold, priority=10
        )

        self.add_menu_items(self.menu)
        self.reset_theme()

    def _on_afk_threshold(self, level: str) -> None:
        if level == "IntroState":
            self.client.replace_state("IntroState")

    def shutdown(self) -> None:
        self.unsubscribe("afk.threshold_reached", self._on_afk_threshold)
        super().shutdown()

    def start_battle(self, difficulty: str) -> None:
        NPC.create_player(local_session, slug=PLAYER_NPC)
        self.client.push_state(
            "WorldState", session=local_session, map_name=None
        )
        self.client.event_engine.execute_action(
            "set_variable", [f"difficulty:{difficulty}"]
        )
        self.client.event_engine.execute_action("load_yaml", ["battle_menu"])

    def start_minigame(self, difficulty: str) -> None:
        self.client.push_state(
            "MinigameState",
            difficulty=difficulty,
            streak=0,
            score=0,
        )


class ModsChoice(PygameMenuState):
    """The state responsible for the mods menu."""

    name: ClassVar[str] = "ModsChoice"

    def add_menu_items(
        self,
        menu: Menu,
    ) -> None:

        def new_game(mod_name: str) -> None:
            launcher = GameLauncher(self.client)
            launcher.launch(
                session=local_session,
                meta=db.mod_metadata.get_mod_metadata(mod_name),
                remove_states=["StartState", "ModsChoice"],
            )

        for mod_name in self.mods:
            menu.add.button(
                title=T.translate(f"{mod_name}_campaign"),
                action=partial(new_game, mod_name),
                font_size=self.font_type.big,
                button_id=mod_name,
            )

    def __init__(
        self, client: BaseClient, mods: list[str], **kwargs: Any
    ) -> None:
        self.mods = mods
        width, height = client.context.resolution

        super().__init__(client=client, height=height, width=width, **kwargs)

        theme = self._setup_theme(BG_START_SCREEN)
        theme.scrollarea_position = POSITION_EAST
        theme.widget_alignment = ALIGN_CENTER
        self._menu_config["theme"] = theme

        self.add_menu_items(self.menu)
        self.reset_theme()
