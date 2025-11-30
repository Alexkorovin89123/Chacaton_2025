import cv2
import os


def extract_frames(video_path, output_folder):
    """
    Извлекает кадры из видео и сохраняет их в указанную папку

    Args:
        video_path (str): Путь к видеофайлу
        output_folder (str): Папка для сохранения кадров
    """

    # Создаем папку для кадров, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Открываем видеофайл
    cap = cv2.VideoCapture(video_path)

    # Проверяем, открылось ли видео
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видеофайл")
        return

    # Получаем информацию о видео
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    print(f"Видео информация:")
    print(f" - FPS: {fps}")
    print(f" - Всего кадров: {total_frames}")
    print(f" - Длительность: {duration:.3f} секунд")

    frame_count = 0
    saved_count = 0

    print("Начинаем извлечение кадров...")

    while True:
        # Читаем следующий кадр
        ret, frame = cap.read()

        # Если кадр не прочитан, выходим из цикла
        if not ret:
            break

        # Сохраняем каждый кадр
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:06d}.jpg")
        cv2.imwrite(frame_filename, frame)
        saved_count += 1

        # Выводим прогресс каждые 100 кадров
        if frame_count % 100 == 0:
            print(f"Обработано кадров: {frame_count}/{total_frames}")

        frame_count += 1

    # Освобождаем ресурсы
    cap.release()

    print(f"Готово! Извлечено {saved_count} кадров в папку '{output_folder}'")


def extract_frames_with_interval(video_path, output_folder, interval=1):
    """
    Извлекает кадры с определенным интервалом

    Args:
        video_path (str): Путь к видеофайлу
        output_folder (str): Папка для сохранения кадров
        interval (int): Интервал между сохраняемыми кадрами (в кадрах)
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видеофайл")
        return

    frame_count = 0
    saved_count = 0

    print(f"Извлечение кадров с интервалом {interval}...")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Сохраняем только каждый N-ый кадр
        if frame_count % interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_count:06d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1

            if saved_count % 50 == 0:
                print(f"Сохранено кадров: {saved_count}")

        frame_count += 1

    cap.release()
    print(f"Готово! Сохранено {saved_count} кадров с интервалом {interval}")


# Основная функция
if __name__ == "__main__":
    # Укажите путь к вашему видеофайлу
    video_file = "remont_30.mp4"  # Замените на путь к вашему видео

    # Папка для сохранения кадров
    output_dir = "extracted_frames"

    # Проверяем существование видеофайла
    if not os.path.exists(video_file):
        print(f"Ошибка: Файл '{video_file}' не найден")
        print("Пожалуйста, укажите правильный путь к видеофайлу")
    else:
        # Вариант 1: Извлечь все кадры
        extract_frames(video_file, output_dir)

        # Вариант 2: Извлечь кадры с интервалом (раскомментируйте для использования)
        # extract_frames_with_interval(video_file, output_dir + "_interval", interval=10)