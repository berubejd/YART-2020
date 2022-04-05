import copy
import random

import tcod

import color
import entity_factories
from engine import Engine
from paperdungeon import generate_paper_dungeon
from procgen import generate_dungeon


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    max_monters_per_room = 2

    # TCOD tileset
    # tileset = tcod.tileset.load_tilesheet(
    #     "data/dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    # )

    # Ascii tileset
    tileset = tcod.tileset.load_tilesheet(
        "data/16x16_sb_ascii.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    # Truetype font tileset
    # tileset = tcod.tileset.load_truetype_font(
    #     "data/Example.ttf",
    #     tile_width=16,
    #     tile_height=16,
    # )

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
            max_monsters_per_room=max_monters_per_room,
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
            max_monsters_per_room=max_monters_per_room,
            engine=engine,
        )

    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")

        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)

            engine.event_handler.handle_events(context)


if __name__ == "__main__":
    main()
