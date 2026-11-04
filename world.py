import arcade

# Размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Моя Первая Игра"


class MyGame(arcade.Window):
    def __init__(self):
        # Инициализируем окно
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Задаем цвет фона
        arcade.set_background_color(arcade.color.AMAZON)

        # Здесь объявляем переменные (игрока, врагов, счет)
        self.player_x = 100
        self.player_y = 100

        # Создаем список
        self.player_list = arcade.SpriteList()

        # Создаем спрайт игрока из картинки, задаем масштаб (scale) и координаты
        self.player_sprite = arcade.Sprite("sprites/sheep.png", scale=0.5)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 300

        # Добавляем в список
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """Этот метод вызывается автоматически для отрисовки графики"""
        self.clear()  # Очищаем экран перед каждым новым кадром

        self.player_list.draw()

    # def on_update(self, delta_time):
    #     """Этот метод вызывается ~60 раз в секунду для логики и физики"""
    #     # Двигаем круг вправо на каждом кадре
    #     self.player_x += 2
    #
    #     # Если круг улетел за экран, возвращаем его назад
    #     if self.player_x > SCREEN_WIDTH:
    #         self.player_x = 0


def main():
    window = MyGame()
    arcade.run()  # Запускаем игровой цикл


if __name__ == "__main__":
    main()
