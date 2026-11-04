import os
import random
import arcade


class DatasetGenerator(arcade.Window):
    def __init__(self,
                 width: int,
                 height: int,
                 sprite_folder: str,
                 volume: int,
                 max_objects: int):
        super().__init__(width, height, "Dataset Generator")
        self.width = width
        self.height = height
        self.volume = volume
        self.max_objects = max_objects
        self.sprite_folder = sprite_folder
        arcade.set_background_color(arcade.color.AMAZON)
        os.makedirs("dataset/images", exist_ok=True)
        os.makedirs("dataset/labels", exist_ok=True)
        self.img_counter = 0

        self.game_objects = {}
        for f in os.listdir(self.sprite_folder):
            self.game_objects[f.split('.')[0]] = arcade.SpriteList()

    def setup_random_scene(self):
        for k in self.game_objects.keys():
            self.game_objects[k].clear()

            for _ in range(random.randint(0, self.max_objects)):
                sprt = arcade.Sprite(f"{self.sprite_folder}/{k}.png", scale=0.5)
                sprt.center_x = random.randint(10, self.width - 10)
                sprt.center_y = random.randint(10, self.height - 10)
                self.game_objects[k].append(sprt)

    def on_draw(self):
        self.clear()
        for _, v in self.game_objects.items():
            v.draw()

    def on_update(self, delta_time):
        self.setup_random_scene()
        self.on_draw()

        image = arcade.get_image(0, 0, self.width, self.height)
        img_name = f"frame_{self.img_counter}"
        image.save(f"dataset/images/{img_name}.png")

        yolo_lines = []

        for k, v in self.game_objects.items():
            for sprt in v:
                line = self.convert_to_yolo(class_id=k, sprite=sprt)
                yolo_lines.append(line)

        if yolo_lines:
            with open(f"dataset/labels/{img_name}.txt", "w") as f:
                f.write("\n".join(yolo_lines))

        self.img_counter += 1

        if self.img_counter >= self.volume:
            print("Датасет готов!")
            arcade.close_window()

    def convert_to_yolo(self, class_id, sprite):
        # Координаты центра (инвертируем Y, так как в arcade 0 внизу, а в YOLO вверху)
        x_center = sprite.center_x / self.width
        y_center = (self.height - sprite.center_y) / self.height

        width = sprite.width / self.width
        height = sprite.height / self.height

        x_center = max(0.0, min(1.0, x_center))
        y_center = max(0.0, min(1.0, y_center))
        width = max(0.0, min(1.0, width))
        height = max(0.0, min(1.0, height))

        return f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"


if __name__ == "__main__":
    window = DatasetGenerator(width=500, height=500, sprite_folder='sprites', volume=5, max_objects=3)
    arcade.run()

