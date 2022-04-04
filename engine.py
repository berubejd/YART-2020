from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

from input_handlers import MainGameEventHandler

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler


class Engine:
    """Manage game responsibilities such as drawing the screen, handling events, etc."""

    gamemap: GameMap

    def __init__(
        self,
        player: Actor,
    ) -> None:
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.gamemap.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        """Recompute the field of view of the player"""
        self.gamemap.visible[:] = compute_fov(
            self.gamemap.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )

        # Add visible tiles to the explored tile list
        self.gamemap.explored |= self.gamemap.visible

    def render(self, console: Console, context: Context) -> None:
        self.gamemap.render(console=console)

        console.print(
            x=1,
            y=47,
            string=f"HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}",
        )

        context.present(console)
        console.clear()
