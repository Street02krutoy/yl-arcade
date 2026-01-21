"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from arcade import gui
from pyglet.graphics import Batch
import random

from entity.enemies.base_enemy import BaseEnemy
from entity.player import Player
from entity.weapons.base_weapon import BaseWeapon
from entity.weapons.circular_rotating_weapon import CircularRotatingWeapon
from gui.level_up import LevelUpLayout
from inventory.inventory import Inventory
from inventory.item import InventoryWeapon
from level.level import GameLevel

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"


class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.GRAY_BLUE
        self.player = Player()
        self.inventory = Inventory()
        self.camera = arcade.Camera2D()
        self.keys = set[int]()
        self.player_list = arcade.SpriteList[Player]()
        self.level = GameLevel()

        self.player_list.append(self.player)
        self.ms_boost_list = arcade.SpriteList[arcade.Sprite]()
        self.ms_boost_list.append(arcade.Sprite("assets/green crystal.png",
                                    scale=1))
        self.weapons_list = arcade.SpriteList[BaseWeapon]()
        self.inventory.add(InventoryWeapon("Пила", CircularRotatingWeapon("assets/linuh.png", 2, 200)))
        for item in self.ms_boost_list:
            item.center_x, item.center_y = (253, 135)  
        self.enemy_list = arcade.SpriteList[BaseEnemy]()
        self.batch = Batch()
        self.ui = gui.UIManager()
        self.level_up_layout = LevelUpLayout(self.player, (WINDOW_WIDTH, WINDOW_HEIGHT), self.inventory)
        self.ui.add(self.level_up_layout)
        
        
        self.engine = arcade.PhysicsEngineSimple(
            player_sprite=self.player,
        )

    def reset(self, level: GameLevel):
        self.player.reset()
        self.enemy_list.clear()
        self.level = level


    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        
        with self.camera.activate():
            self.ms_boost_list.draw()
            self.weapons_list.draw()

            self.enemy_list.draw()
            self.player_list.draw()

            for enemy in self.enemy_list:

                enemy.draw_health_bar()
        
        if self.ui._enabled:
            self.ui.draw()
        
        arcade.draw_lbwh_rectangle_filled(
            10, self.height-30, self.width-20, 20, arcade.color.BLACK
        )
        arcade.draw_lbwh_rectangle_filled(
            10, self.height-30, (self.width-20)*self.player.hitpoints/100, 20, arcade.color.ROSE_RED
        )
        
        self.batch.draw()
        
    def format_time_mm_ss(self, total_seconds: int) -> str:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"


    def on_update(self, delta_time: float):
        self.camera.position = self.player.position
        if self.player.unspent_score != 0:
            if not self.ui._enabled:
                self.level_up_layout.update_items()
                self.ui.enable()
            return
        for item in self.inventory.get():
            if not item.weapon in self.weapons_list:
                self.weapons_list.append(item.weapon)
        if self.ui._enabled:
                self.ui.disable()
        if self.player.hitpoints <= 0: 
            if self.player.dead:
                return
            self.text_info = arcade.Text(f"umer",
                                     16, 16, arcade.color.RED, 14, batch=self.batch)
            return
        self.level.update(delta_time, self.player, self.enemy_list)
        self.weapons_list.update(delta_time, self.enemy_list, self.player) # type: ignore
        self.enemy_list.update(delta_time, self.enemy_list) # type: ignore
        self.text_info = arcade.Text(f"Current MS: {self.player.movespeed}, Current HP: {self.player.hitpoints}, Position: {self.player.position}, Time: {self.format_time_mm_ss(int(self.level.timer))}, Spawn: {round(self.level.spawn_timer, 2)}, XP: {self.player.xp}/{self.player.xp_to_next_lvl}({self.player.level})",
                                     16, 16, arcade.color.GREEN, 14, batch=self.batch)
        self.player.update_movespeed_with_keys(self.keys)
        self.player.update_movement(delta_time)



        for coin in arcade.check_for_collision_with_list(self.player, self.ms_boost_list):
            coin.remove_from_sprite_lists()
            new_boost = arcade.Sprite("assets/green crystal.png",
                                    scale=1)
            self.ms_boost_list.append(new_boost)
            new_boost.center_x, new_boost.center_y = (random.randrange(100, WINDOW_WIDTH - 100), random.randrange(100, WINDOW_HEIGHT -100))  
            
            self.player.movespeed += 1

        self.engine.update()
        
    def on_key_press(self, symbol: int, modifiers: int):
        self.keys.add(symbol)
        if symbol == arcade.key.R:
            self.reset(GameLevel())


    def on_key_release(self, symbol: int, modifiers: int):
        self.keys.discard(symbol)


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        pass

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        pass


def main():
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    game = GameView()

    window.show_view(game)

    arcade.run()



if __name__ == "__main__":
    main()