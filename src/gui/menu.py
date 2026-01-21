
import arcade
from typing import Callable
import json
import os

# Константы для меню
MENU_WIDTH = 1280
MENU_HEIGHT = 720
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60


class GameSettings:
    """Класс для управления настройками игры"""

    def __init__(self):
        self.settings_file = "game_settings.json"
        self.default_settings = {
            "selected_character": "warrior",
            "sound_volume": 1.0,
            "music_volume": 0.5,
            "brightness": 1.0,
            "fullscreen": False,
            "difficulty": "normal"
        }
        self.settings = self.load_settings()

    def load_settings(self) -> dict:
        """Загрузка настроек из файла"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    # Объединяем с дефолтными, если каких-то ключей нет
                    for key, value in self.default_settings.items():
                        if key not in loaded:
                            loaded[key] = value
                    return loaded
        except:
            pass

        return self.default_settings.copy()

    def save_settings(self):
        """Сохранение настроек в файл"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except:
            return False

    def get(self, key: str, default=None):
        """Получить значение настройки"""
        return self.settings.get(key, default)

    def set(self, key: str, value):
        """Установить значение настройки"""
        self.settings[key] = value


class CharacterSelectView(arcade.View):
    """Экран выбора персонажа"""

    def __init__(self, menu_view, selected_character: str):
        super().__init__()
        self.menu_view = menu_view
        self.selected_character = selected_character
        self.background_color = arcade.color.DARK_SLATE_GRAY

        # Кнопки выбора персонажа
        self.character_buttons = []
        self.create_character_buttons()

        # Кнопка возврата
        self.back_button = arcade.gui.UIFlatButton(
            text="Назад",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            style={"font_size": 20}
        )
        self.back_button.on_click = self.go_back
        self.back_button.center_x = MENU_WIDTH // 2
        self.back_button.center_y = 100

    def create_character_buttons(self):
        """Создание кнопок выбора персонажа"""
        characters = [
            ("Воин", "warrior", arcade.color.RED, MENU_WIDTH // 4, MENU_HEIGHT // 2 + 50),
            ("Маг", "mage", arcade.color.BLUE, MENU_WIDTH // 2, MENU_HEIGHT // 2 + 50),
            ("Лучник", "archer", arcade.color.GREEN, 3 * MENU_WIDTH // 4, MENU_HEIGHT // 2 + 50)
        ]

        for name, char_type, color, x, y in characters:
            button = arcade.gui.UIFlatButton(
                text=name,
                width=200,
                height=80,
                style={
                    "font_size": 18,
                    "bg_color": color if self.selected_character == char_type else arcade.color.GRAY
                }
            )
            button.on_click = lambda event, ct=char_type: self.select_character(ct)
            button.center_x = x
            button.center_y = y
            self.character_buttons.append(button)

    def select_character(self, character_type: str):
        """Выбор персонажа"""
        if self.menu_view.select_sound:
            arcade.play_sound(self.menu_view.select_sound)

        self.selected_character = character_type
        self.menu_view.selected_character = character_type

        # Обновляем стиль кнопок
        for button in self.character_buttons:
            if button.text.lower() == character_type:
                button.style["bg_color"] = arcade.color.GOLD
            else:
                button.style["bg_color"] = arcade.color.GRAY

    def go_back(self, event=None):
        """Возврат в главное меню"""
        if self.menu_view.click_sound:
            arcade.play_sound(self.menu_view.click_sound)
        self.window.show_view(self.menu_view)

    def on_draw(self):
        """Отрисовка экрана выбора персонажа"""
        self.clear()

        # Фон
        arcade.draw_lrwh_rectangle_textured(
            0, 0, MENU_WIDTH, MENU_HEIGHT,
            arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")
        )

        # Заголовок
        arcade.draw_text(
            "ВЫБОР ПЕРСОНАЖА",
            MENU_WIDTH // 2,
            MENU_HEIGHT - 100,
            arcade.color.WHITE,
            48,
            anchor_x="center",
            bold=True
        )

        # Описание выбранного персонажа
        character = self.menu_view.characters[self.selected_character]
        arcade.draw_text(
            f"Здоровье: {character['health']} | Урон: {character['damage']} | Скорость: {character['speed']}",
            MENU_WIDTH // 2,
            200,
            arcade.color.LIGHT_YELLOW,
            24,
            anchor_x="center"
        )

        # Кнопки
        for button in self.character_buttons:
            button.draw()
        self.back_button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка нажатия мыши"""
        for ui_button in self.character_buttons + [self.back_button]:
            if ui_button.collides_with_point((x, y)):
                ui_button.on_click(None)

    def on_key_press(self, symbol, modifiers):
        """Обработка нажатия клавиш"""
        if symbol == arcade.key.ESCAPE:
            self.go_back()
        elif symbol == arcade.key.LEFT:
            chars = list(self.menu_view.characters.keys())
            idx = chars.index(self.selected_character)
            self.select_character(chars[(idx - 1) % len(chars)])
        elif symbol == arcade.key.RIGHT:
            chars = list(self.menu_view.characters.keys())
            idx = chars.index(self.selected_character)
            self.select_character(chars[(idx + 1) % len(chars)])


class SettingsView(arcade.View):
    """Экран настроек"""

    def __init__(self, menu_view, settings: dict):
        super().__init__()
        self.menu_view = menu_view
        self.settings = settings
        self.background_color = arcade.color.DARK_GREEN

        # Ползунки настроек
        self.sound_slider = arcade.gui.UIInputText(
            width=200,
            height=40,
            text=str(int(self.settings.get("sound_volume", 1.0) * 100))
        )

        self.music_slider = arcade.gui.UIInputText(
            width=200,
            height=40,
            text=str(int(self.settings.get("music_volume", 0.5) * 100))
        )

        self.brightness_slider = arcade.gui.UIInputText(
            width=200,
            height=40,
            text=str(int(self.settings.get("brightness", 1.0) * 100))
        )

        # Кнопки
        self.back_button = arcade.gui.UIFlatButton(
            text="Назад",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT
        )
        self.back_button.on_click = self.go_back

        self.save_button = arcade.gui.UIFlatButton(
            text="Сохранить",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT
        )
        self.save_button.on_click = self.save_settings

        # Позиционирование
        center_x = MENU_WIDTH // 2
        self.sound_slider.center_x = center_x + 150
        self.sound_slider.center_y = MENU_HEIGHT - 200

        self.music_slider.center_x = center_x + 150
        self.music_slider.center_y = MENU_HEIGHT - 280

        self.brightness_slider.center_x = center_x + 150
        self.brightness_slider.center_y = MENU_HEIGHT - 360

        self.back_button.center_x = center_x - 100
        self.back_button.center_y = 100

        self.save_button.center_x = center_x + 100
        self.save_button.center_y = 100

    def save_settings(self, event=None):
        """Сохранение настроек"""
        try:
            # Обновляем настройки
            self.settings["sound_volume"] = int(self.sound_slider.text) / 100
            self.settings["music_volume"] = int(self.music_slider.text) / 100
            self.settings["brightness"] = int(self.brightness_slider.text) / 100

            # Обновляем яркость в главном меню
            self.menu_view.brightness = self.settings["brightness"]

            # Сохраняем в файл
            self.menu_view.settings_manager.save_settings()

            if self.menu_view.click_sound:
                arcade.play_sound(self.menu_view.click_sound)

            self.go_back()

        except ValueError:
            pass

    def go_back(self, event=None):
        """Возврат в главное меню"""
        if self.menu_view.click_sound:
            arcade.play_sound(self.menu_view.click_sound)
        self.window.show_view(self.menu_view)

    def on_draw(self):
        """Отрисовка экрана настроек"""
        self.clear()

        # Фон
        arcade.draw_lrwh_rectangle_textured(
            0, 0, MENU_WIDTH, MENU_HEIGHT,
            arcade.load_texture(":resources:images/backgrounds/abstract_3.jpg")
        )

        # Заголовок
        arcade.draw_text(
            "НАСТРОЙКИ",
            MENU_WIDTH // 2,
            MENU_HEIGHT - 100,
            arcade.color.WHITE,
            48,
            anchor_x="center",
            bold=True
        )

        # Надписи настроек
        arcade.draw_text(
            "Громкость звуков:",
            MENU_WIDTH // 2 - 200,
            MENU_HEIGHT - 190,
            arcade.color.WHITE,
            24
        )

        arcade.draw_text(
            "Громкость музыки:",
            MENU_WIDTH // 2 - 200,
            MENU_HEIGHT - 270,
            arcade.color.WHITE,
            24
        )

        arcade.draw_text(
            "Яркость:",
            MENU_WIDTH // 2 - 200,
            MENU_HEIGHT - 350,
            arcade.color.WHITE,
            24
        )

        # Ползунки
        self.sound_slider.draw()
        self.music_slider.draw()
        self.brightness_slider.draw()

        # Кнопки
        self.back_button.draw()
        self.save_button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка нажатия мыши"""
        for ui_element in [self.sound_slider, self.music_slider, self.brightness_slider,
                           self.back_button, self.save_button]:
            if ui_element.collides_with_point((x, y)):
                if hasattr(ui_element, 'on_click'):
                    ui_element.on_click(None)
                return

    def on_key_press(self, symbol, modifiers):
        """Обработка нажатия клавиш"""
        if symbol == arcade.key.ESCAPE:
            self.go_back()
        elif symbol == arcade.key.ENTER:
            self.save_settings()


class MenuView(arcade.View):
    """Главное меню игры"""

    def __init__(self, on_start_game: Callable):
        super().__init__()
        self.on_start_game = on_start_game
        self.background_color = arcade.color.DARK_BLUE_GRAY

        # Загрузка настроек
        self.settings_manager = GameSettings()
        self.settings = self.settings_manager.settings

        # Звуки из встроенной библиотеки Arcade
        self.click_sound = arcade.load_sound(":resources:sounds/coin2.wav")  # Короткий клик
        self.select_sound = arcade.load_sound(":resources:sounds/coin4.wav")  # Выбор
        self.death_sound = arcade.load_sound(":resources:sounds/gameover3.wav")  # Смерть
        self.hit_sound = arcade.load_sound(":resources:sounds/hit3.wav")  # Удар
        self.level_up_sound = arcade.load_sound(":resources:sounds/upgrade4.wav")  # Уровень

        # Выбранный персонаж
        self.selected_character = self.settings.get("selected_character", "warrior")
        self.characters = {
            "warrior": {
                "name": "Воин",
                "damage": 15,
                "health": 120,
                "speed": 1.0,
                "description": "Сильный и выносливый боец"
            },
            "mage": {
                "name": "Маг",
                "damage": 25,
                "health": 80,
                "speed": 1.1,
                "description": "Мощные заклинания, но мало здоровья"
            },
            "archer": {
                "name": "Лучник",
                "damage": 20,
                "health": 90,
                "speed": 1.2,
                "description": "Быстрый и меткий стрелок"
            }
        }

        # Создание кнопок
        self.button_list = []
        self.create_buttons()

        # Текущая яркость
        self.brightness = self.settings.get("brightness", 1.0)

    def create_buttons(self):
        """Создание кнопок меню"""
        center_x = MENU_WIDTH // 2
        start_y = MENU_HEIGHT // 2 + 100

        buttons = [
            ("Начать игру", self.start_game, center_x, start_y),
            ("Выбор персонажа", self.open_character_select, center_x, start_y - 80),
            ("Настройки", self.open_settings, center_x, start_y - 160),
            ("Выйти", self.exit_game, center_x, start_y - 240)
        ]

        for text, callback, x, y in buttons:
            button = arcade.gui.UIFlatButton(
                text=text,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                style={
                    "font_size": 20,
                    "bg_color": arcade.color.BLUE_GRAY,
                    "font_color": arcade.color.WHITE,
                    "border_color": arcade.color.GOLD,
                    "border_width": 2
                }
            )
            button.on_click = lambda event, cb=callback: cb()
            button.center_x = x
            button.center_y = y
            self.button_list.append(button)

    def start_game(self):
        """Запуск игры"""
        arcade.play_sound(self.click_sound)

        # Сохраняем выбранного персонажа в настройки
        self.settings["selected_character"] = self.selected_character
        self.settings["brightness"] = self.brightness
        self.settings_manager.save_settings()

        # Запускаем игру с выбранным персонажем
        self.on_start_game(self.selected_character, self.characters[self.selected_character])

    def open_character_select(self):
        """Открыть экран выбора персонажа"""
        arcade.play_sound(self.click_sound)
        character_view = CharacterSelectView(self, self.selected_character)
        self.window.show_view(character_view)

    def open_settings(self):
        """Открыть настройки"""
        arcade.play_sound(self.click_sound)
        settings_view = SettingsView(self, self.settings)
        self.window.show_view(settings_view)

    def exit_game(self):
        """Выход из игры"""
        arcade.play_sound(self.click_sound)
        arcade.exit()

    def on_draw(self):
        """Отрисовка меню"""
        self.clear()

        # Фоновое изображение
        arcade.draw_lrwh_rectangle_textured(
            0, 0, MENU_WIDTH, MENU_HEIGHT,
            arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")
        )

        # Затемнение для лучшей читаемости текста
        arcade.draw_rectangle_filled(
            MENU_WIDTH // 2, MENU_HEIGHT // 2,
            MENU_WIDTH, MENU_HEIGHT,
            (0, 0, 0, int(200 * (1 - self.brightness)))
        )

        # Заголовок с тенью
        arcade.draw_text(
            "ГЛАВНОЕ МЕНЮ",
            MENU_WIDTH // 2 + 3,
            MENU_HEIGHT - 103,
            arcade.color.BLACK,
            48,
            anchor_x="center",
            bold=True
        )
        arcade.draw_text(
            "ГЛАВНОЕ МЕНЮ",
            MENU_WIDTH // 2,
            MENU_HEIGHT - 100,
            arcade.color.GOLD,
            48,
            anchor_x="center",
            bold=True
        )

        # Информация о выбранном персонаже
        character = self.characters[self.selected_character]
        arcade.draw_text(
            f"Выбранный персонаж: {character['name']}",
            MENU_WIDTH // 2,
            180,
            arcade.color.LIGHT_BLUE,
            28,
            anchor_x="center"
        )

        arcade.draw_text(
            character['description'],
            MENU_WIDTH // 2,
            130,
            arcade.color.LIGHT_YELLOW,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Управление: ← → для выбора, ENTER - начать, ESC - выход",
            MENU_WIDTH // 2,
            50,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center"
        )

        # Кнопки
        for button in self.button_list:
            button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка нажатия мыши"""
        for ui_button in self.button_list:
            if ui_button.collides_with_point((x, y)):
                ui_button.on_click(None)

    def on_key_press(self, symbol, modifiers):
        """Обработка нажатия клавиш"""
        if symbol == arcade.key.ENTER:
            self.start_game()
        elif symbol == arcade.key.ESCAPE:
            self.exit_game()
        elif symbol == arcade.key.C:
            # Быстрый доступ к выбору персонажа
            self.open_character_select()
        elif symbol == arcade.key.S:
            # Быстрый доступ к настройкам
            self.open_settings()


# Дополнительные классы для использования в игре
class GameSoundManager:
    """Менеджер звуков для игры"""

    def __init__(self):
        # Загружаем все звуки из встроенной библиотеки
        self.sounds = {
            'click': arcade.load_sound(":resources:sounds/coin2.wav"),
            'select': arcade.load_sound(":resources:sounds/coin4.wav"),
            'death': arcade.load_sound(":resources:sounds/gameover3.wav"),
            'hit': arcade.load_sound(":resources:sounds/hit3.wav"),
            'level_up': arcade.load_sound(":resources:sounds/upgrade4.wav"),
            'jump': arcade.load_sound(":resources:sounds/jump3.wav"),
            'laser': arcade.load_sound(":resources:sounds/laser2.wav"),
            'explosion': arcade.load_sound(":resources:sounds/explosion2.wav"),
            'powerup': arcade.load_sound(":resources:sounds/upgrade1.wav"),
            'error': arcade.load_sound(":resources:sounds/error2.wav")
        }

        # Громкость по умолчанию
        self.volume = 1.0

    def play(self, sound_name: str, volume: float = None):
        """Воспроизвести звук"""
        if sound_name in self.sounds:
            vol = volume if volume is not None else self.volume
            arcade.play_sound(self.sounds[sound_name], volume=vol)

    def set_volume(self, volume: float):
        """Установить громкость"""
        self.volume = max(0.0, min(1.0, volume))

    def get_volume(self) -> float:
        """Получить текущую громкость"""
        return self.volume


# Экспортируемые классы для удобства использования из других модулей
__all__ = [
    'MenuView',
    'CharacterSelectView',
    'SettingsView',
    'GameSettings',
    'GameSoundManager'

]
