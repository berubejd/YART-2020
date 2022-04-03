from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional

import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity


class GameMap:
    def __init__(
        self, width: int, height: int, entities: Iterable[Entity] = ()
    ) -> None:
        self.width = width
        self.height = height
        self.entities = set(entities)

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        # Track currently visible and previously visited but no longer visible tiles
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def get_blocking_entity_at_location(self, x: int, y: int) -> Optional[Entity]:
        """
        Return the first entity at x, y that blocks movement
        """
        for entity in self.entities:
            if entity.blocks_movement and entity.x == x and entity.y == y:
                return entity

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of the map"""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map to the console

        If a tile is in the "visible" array, then draw it with the "light" colors
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors
        Otherwise, the default is "SHROUD"
        """
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        for entity in self.entities:
            # Only draw entities that are in the "visible" array
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )
