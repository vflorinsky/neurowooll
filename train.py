import shutil
from pathlib import Path
from ultralytics import YOLO


def main():
    # Инициализация модели
    model = YOLO("yolov8n.pt")

    # Запускаем обучение на вашем датасете
    results = model.train(
        data="C:\\Data\\Slavon\\petprojects\\neurowooll\\dataset\\dataset.yaml",
        epochs=100,           # Количество эпох обучения
        imgsz=500,            # Ваше разрешение изображений (например, 500x500)
        workers=8,            # Количество потоков загрузки данных
        batch=16,             # Размер батча
        device=0,             # Обучение на GPU (Nvidia)
        save=True             # Сохранять чекпоинты
    )


if __name__ == '__main__':
    main()
    train_index = []
    for item in Path('runs/detect').iterdir():
        if item.is_dir():
            try:
                train_index.append(int(item.name.split('-')[-1]))
            except ValueError:
                pass
    train_index = "" if len(train_index) == 0 else f"-{max(train_index)}"
    weights_path = f"runs/detect/train{train_index}/weights"

    model = YOLO(f"{weights_path}/best.pt")
    model.export(format="onnx", imgsz=500, half=True)

    shutil.copy(f"{weights_path}/best.onnx", 'best.onnx')


