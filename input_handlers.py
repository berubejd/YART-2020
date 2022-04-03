from typing import Optional

import tcod.event

from actions import Action, BumpAction, EscapeAction


class EventHandler(tcod.event.EventDispatch[Action]):
    """Capture and forward events based on event type"""

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        """Quit the game"""

        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """Handle keypresses"""

        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = BumpAction(dx=1, dy=0)

        # Using the escape key causes the game to exit immediately on subsequent starts

        # elif key == tcod.event.K_ESCAPE:
        #     action = EscapeAction()

        # No valid key was pressed
        return action
