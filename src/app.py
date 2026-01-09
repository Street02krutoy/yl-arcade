"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from pyglet.graphics import Batch
import random

from entity.player import Player

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
        
        self.player_list = arcade.SpriteList[arcade.Sprite]()

        self.player_list.append(self.player)
        self.ms_boost_list = arcade.SpriteList[arcade.Sprite]()
        self.ms_boost_list.append(arcade.Sprite("assets/crystal.png",
                                    scale=0.1))
        for item in self.ms_boost_list:
            item.center_x, item.center_y = (253, 135)  
        
        self.batch = Batch()
        
        self.engine = arcade.PhysicsEngineSimple(
            player_sprite=self.player,
        )

    def reset(self):
        """Reset the game to the initial state."""
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.batch.draw()
        self.player_list.draw()
        self.ms_boost_list.draw()


    def on_update(self, delta_time: float):
        if self.player.hitpoints <= 0: 
            if self.player.dead:
                return
            self.text_info = arcade.Text(f"umer",
                                     16, 16, arcade.color.RED, 14, batch=self.batch)
            self.player.kill()
            return
    
        self.text_info = arcade.Text(f"Current MS: {self.player.movespeed}, Current HP: {self.player.hitpoints}",
                                     16, 16, arcade.color.GREEN, 14, batch=self.batch)
        self.player.update_movement()
        if self.player.center_x <= 0:
            self.player.center_x = WINDOW_WIDTH - 1

        if self.player.center_x >= WINDOW_WIDTH:
            self.player.center_x = 1

        if self.player.center_y <= 0:
            self.player.center_y = WINDOW_HEIGHT - 1

        if self.player.center_y >= WINDOW_HEIGHT:
            self.player.center_y = 1

        for coin in arcade.check_for_collision_with_list(self.player, self.ms_boost_list):
            coin.remove_from_sprite_lists()
            new_boost = arcade.Sprite("assets/crystal.png",
                                    scale=0.1)
            self.ms_boost_list.append(new_boost)
            new_boost.center_x, new_boost.center_y = (random.randrange(100, WINDOW_WIDTH - 100), random.randrange(100, WINDOW_HEIGHT -100))  
            
            self.player.movespeed += 1
            self.player.hitpoints -= 10

        self.engine.update()

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        
        if symbol == arcade.key.A:
            self.player.movement = (-self.player.movespeed, self.player.movement[1])
        if symbol == arcade.key.S:
            self.player.movement = (self.player.movement[0], -self.player.movespeed)
        if symbol == arcade.key.D:
            self.player.movement = (self.player.movespeed, self.player.movement[1])
        if symbol == arcade.key.W:
            self.player.movement = (self.player.movement[0], self.player.movespeed)


    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A:
            self.player.movement = (0, self.player.movement[1])
        if symbol == arcade.key.S:
            self.player.movement = (self.player.movement[0], 0)
        if symbol == arcade.key.D:
            self.player.movement = (0, self.player.movement[1])
        if symbol == arcade.key.W:
            self.player.movement = (self.player.movement[0], 0)

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