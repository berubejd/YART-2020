import random

import tcod

from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from paperdungeon import generate_paper_dungeon
from procgen import generate_dungeon


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        "data/dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    if random.randrange(100) < 60:
        # Generate a "paper" dungeon most of the time
        print("Generating a paper dungeon...")

        room_min_size = 4
        room_max_size = 7

        min_corridor_length: int = room_min_size + 1
        max_corridor_length: int = room_max_size * 3

        complexity = 10

        game_map = generate_paper_dungeon(
            complexity=complexity,
            room_min_size=room_min_size,
            room_max_size=room_max_size,
            min_corridor_length=min_corridor_length,
            max_corridor_length=max_corridor_length,
            map_width=map_width,
            map_height=map_height,
            player=player,
        )

    else:
        # Generate an "original" dungeon sometimes
        print("Generating a procgen dungeon...")

        room_min_size = 6
        room_max_size = 10

        max_rooms = 30

        game_map = generate_dungeon(
            max_rooms=max_rooms,
            room_min_size=room_min_size,
            room_max_size=room_max_size,
            map_width=map_width,
            map_height=map_height,
            player=player,
        )

    engine = Engine(
        entities=entities, event_handler=event_handler, game_map=game_map, player=player
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
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == "__main__":
    main()
