from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import (
    render_bar,
    render_bar_classic,
    render_names_at_mouse_location,
)

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
        self.message_log = MessageLog()
        self.mouse_location: tuple[int, int] = (0, 0)
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

    def render(self, console: Console) -> None:
        self.gamemap.render(console=console)

        self.message_log.render(console=console, x=21, y=44, width=40, height=5)

        render_bar_classic(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=14,
        )

        render_names_at_mouse_location(console=console, x=1, y=1, engine=self)
