import os
import random
import arcade


class DatasetGenerator(arcade.Window):
    def __init__(self,
                 width: int,
                 height: int,
                 output_folder: str,
                 sprite_folder: str,
                 train_volume: int,
                 val_volume: int,
                 test_volume: int,
                 max_objects: int):
        super().__init__(width, height, "Dataset Generator")
        self.width = width
        self.height = height
        self.output_folder = output_folder
        self.train_volume = train_volume
        self.val_volume = val_volume
        self.test_volume = test_volume
        self.max_objects = max_objects
        self.sprite_folder = sprite_folder
        arcade.set_background_color(arcade.color.AMAZON)
        os.makedirs(self.output_folder, exist_ok=True)
        for d in ["train/images", "train/labels", "val/images", "val/labels", "test/images", "test/labels"]:
            os.makedirs(f"{self.output_folder}/{d}", exist_ok=True)
        self.img_counter = 0

        self.game_objects = {}
        self.class_dict = {}
        class_id = 0
        for f in os.listdir(self.sprite_folder):
            self.class_dict[class_id] = f.split('.')[0]
            self.game_objects[class_id] = arcade.SpriteList()
            class_id += 1
        self.create_config()

    def create_config(self):
        with open(f"{self.output_folder}/dataset.yaml", 'w') as f:
            f.write(f"path: {self.output_folder}\n")
            f.write("train: train/images\n")
            f.write("val: val/images\n\n")
            f.write("names:\n")
            for k, v in self.class_dict.items():
                f.write(f"  {k}: {v}\n")

    def setup_random_scene(self):
        for k in self.game_objects.keys():
            self.game_objects[k].clear()

            for _ in range(random.randint(0, self.max_objects)):
                sprt = arcade.Sprite(f"{self.sprite_folder}/{self.class_dict[k]}.png", scale=0.5)
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
        folder = 'train'
        if self.train_volume <= self.img_counter < self.train_volume + self.val_volume:
            folder = 'val'
        elif self.img_counter >= self.train_volume + self.val_volume:
            folder = 'test'
        image.save(f"dataset/{folder}/images/{img_name}.png")

        yolo_lines = []

        for k, v in self.game_objects.items():
            for sprt in v:
                line = self.convert_to_yolo(class_id=k, sprite=sprt)
                yolo_lines.append(line)

        if yolo_lines:
            with open(f"dataset/{folder}/labels/{img_name}.txt", "w") as f:
                f.write("\n".join(yolo_lines))

        self.img_counter += 1

        if self.img_counter >= self.val_volume + self.train_volume + self.test_volume:
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
    window = DatasetGenerator(width=500, height=500,
                              output_folder='C:\\Data\\Slavon\\petprojects\\neurowooll\\dataset',
                              sprite_folder='C:\\Data\\Slavon\\petprojects\\neurowooll\\sprites',
                              train_volume=5000,
                              val_volume=500,
                              test_volume=100,
                              max_objects=3)
    arcade.run()

