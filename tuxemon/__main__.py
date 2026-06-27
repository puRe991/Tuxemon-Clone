# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2026 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
"""Command-line entry point for launching Tuxemon as a module."""

from __future__ import annotations

from tuxemon.app import launch_game


def main() -> None:
    """Launch Tuxemon using the shared startup routine."""
    launch_game()


if __name__ == "__main__":
    main()
