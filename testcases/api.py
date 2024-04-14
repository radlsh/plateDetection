# Импортиурем библиотеку opencv для работы с изображением
import cv2
# Импортиурем библиотеку для распознования текста
import easyocr
# импортируем модуль YOLO для использования модели обучения из бибилиотеку ultralytics
from ultralytics import YOLO

# Загружаем лучшие веса, полученные при обучение в переменную model
model = YOLO(r'C:\TTTT\lessonsplatedetection\main\runs\detect\yolo\weights\best.pt')
# Создаем функцию для детекции номера и определение текста на нем
def detect_plate(image_path):
    # Загружаем в переменную фото по переданному пути
    image = cv2.imread(image_path)
    # Предиктим bouding box для картинки
    prediction = model(image)
    # если на картинки обнаружен номер, то продолжаем, если нет, то возвращается текст, что номер не обнаружен
    if prediction:
        # Достаем координаты bouding box-a и преобразуем их в целочисленный формат
        x_min, y_min, x_max, y_max = map(int, prediction[0].boxes.xyxy[0])
        # Обрезаем изображение по полученному bouding box-y
        section_image = image[y_min:y_max, x_min:x_max]
        # Увеличиваем размер нашего изображение
        resized_image = cv2.resize(section_image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        # Применяем к изображению фильтр Гауса, чтобы убрать шумы
        blurred_image = cv2.GaussianBlur(resized_image, (5, 5), 0)
        # Изменяем контрастность и яркость нашего изображения
        final_image = cv2.convertScaleAbs(blurred_image, alpha=1.5, beta=0)
        # Параметры easyocr
        reader = easyocr.Reader(['en'], gpu=False)
        # Распознаем номер на обрезанной картинке с помощью ранее созданного экземляра объекта reader
        car_number = reader.readtext(
                image=final_image,
                allowlist='ABCEHKMOPTXY0123456789', # Даем список символов которые должна стремится распознать модель исключая все остальные символы
                paragraph=True) # Выводим результаты детекции в удобочитаемом виде
        # Выделяем обнаруженный номер красный box-ом 
        image_box = cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color=(0, 0, 255), thickness=2)
        # Добавляем распознанный текст
        text_box = cv2.putText(image_box, car_number[-1][-1], (x_min, y_min-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(0, 0, 255), thickness=2)
        # Возвращаем номер, и картинку с box-om
        return car_number, image_box
    else:
        return 
# Создаем функцию для отправки из функции detect_car_number данных в интерфейс
def send_car_number(image_path):   
    # Возвращаем полученные данные
    return detect_plate(image_path)
