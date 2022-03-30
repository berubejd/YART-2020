from typing import Any, Iterable, Set

from tcod.console import Console
from tcod.context import Context

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    """Manage game responsibilities such as drawing the screen, handling events, etc."""

    def __init__(
        self,
        entities: Set[Entity],
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ) -> None:
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(engine=self, entity=self.player)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console=console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)
        console.clear()
