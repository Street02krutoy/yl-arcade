import arcade
from arcade import gui
from typing import Callable
import json
import os

# Constants for menu
MENU_WIDTH = 1280
MENU_HEIGHT = 720
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60

class FinishMenu(arcade.View):
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.ui.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.ui.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.ui.on_mouse_motion(x, y, dx, dy)
    def __init__(self, killed_enemies: int, won: bool, on_restart: Callable, on_menu: Callable):
        super().__init__()
        self.killed_enemies = killed_enemies
        self.won = won
        self.on_restart = on_restart
        self.on_menu = on_menu
        self.ui = gui.UIManager()
        
        button_y = MENU_HEIGHT // 2 - 100
        
        restart_button = gui.UIFlatButton(
            x=MENU_WIDTH // 2 - BUTTON_WIDTH // 2,
            y=button_y,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            text="Перезапустить"
        )
        restart_button.on_click = lambda event: on_restart()
        self.ui.add(restart_button)
        
        menu_button = gui.UIFlatButton(
            x=MENU_WIDTH // 2 - BUTTON_WIDTH // 2,
            y=button_y - BUTTON_HEIGHT - 20,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            text="Меню"
        )
        menu_button.on_click = lambda event: on_menu()
        self.ui.add(menu_button)

    def on_draw(self):
        """Render the finish menu"""
        self.clear((20, 20, 40))
        
        arcade.draw_lbwh_rectangle_filled(
            0,
            MENU_WIDTH,
            MENU_HEIGHT,
            0,
            (30, 30, 50)
        )
        
        title = "Победа!" if self.won else "Игра проиграна!"
        title_color = arcade.color.GREEN if self.won else arcade.color.RED
        
        arcade.draw_text(
            title,
            MENU_WIDTH // 2,
            MENU_HEIGHT - 150,
            title_color,
            font_size=80,
            anchor_x="center",
            bold=True
        )
        
        arcade.draw_text(
            f"Enemies Killed: {self.killed_enemies}",
            MENU_WIDTH // 2,
            MENU_HEIGHT // 2 + 80,
            arcade.color.WHITE,
            font_size=36,
            anchor_x="center"
        )
        
        self.ui.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle key presses"""
        if symbol == arcade.key.ESCAPE:
            self.on_menu()