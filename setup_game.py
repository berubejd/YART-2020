from __future__ import annotations

import copy
import lzma
import pickle
import random
import traceback
from typing import Optional

import tcod

import color
import entity_factories
import input_handlers
from engine import Engine
from paperdungeon import generate_paper_dungeon
from procgen import generate_dungeon

# Load the background image and remove the alpha channel.
background_image = tcod.image.load("data/menu_background.png")[:, :, :3]


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    max_monsters_per_room = 2
    max_items_per_room = 2

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)

    if random.randrange(100) < 70:
        # Generate a "paper" dungeon most of the time
        print("Generating a paper dungeon...")

        room_min_size = 4
        room_max_size = 7

        min_corridor_length: int = room_min_size + 1
        max_corridor_length: int = room_max_size * 3

        complexity = 10

        engine.gamemap = generate_paper_dungeon(
            complexity=complexity,
            room_min_size=room_min_size,
            room_max_size=room_max_size,
            min_corridor_length=min_corridor_length,
            max_corridor_length=max_corridor_length,
            map_width=map_width,
            map_height=map_height,
            max_monsters_per_room=max_monsters_per_room,
            max_items_per_room=max_items_per_room,
            engine=engine,
        )

    else:
        # Generate an "original" dungeon sometimes
        print("Generating a procgen dungeon...")

        room_min_size = 6
        room_max_size = 10

        max_rooms = 30

        engine.gamemap = generate_dungeon(
            max_rooms=max_rooms,
            room_min_size=room_min_size,
            room_max_size=room_max_size,
            map_width=map_width,
            map_height=map_height,
            max_monsters_per_room=max_monsters_per_room,
            max_items_per_room=max_items_per_room,
            engine=engine,
        )

    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )
    return engine


def load_game(filename: str) -> Engine:
    """Load a saved game from a file and return it as an Engine instance"""
    with lzma.open(filename, "rb") as f:
        engine = pickle.load(f)

    assert isinstance(engine, Engine)

    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "TOMBS OF THE ANCIENT KINGS",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By (Your name here)",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            print(f"Still in here? {event}")
            # A KeyDown event seems to be sent repeatedly from the last time the game was shutdown after restart
            # raise SystemExit(0)
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load!")
            except Exception as exc:
                traceback.print_exc()
                return input_handlers.PopupMessage(
                    self, f"Failed to load savegame:\n{exc}"
                )
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())

        return None
