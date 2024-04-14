# Импортиурем бибилиотеку для работы с системой
import sys
# Из PyQt6.QtWidgets импортируем необходимые виджеты
from PyQt6.QtWidgets import QPushButton, QMainWindow, QApplication, QFileDialog, QLabel, QVBoxLayout, QWidget
# Из PyQt6.QtGui импортиурем PixMap для работы с изображением
from PyQt6.QtGui import QPixmap, QImage
# Из api.py импортиурем функцию для получения результатов нашего api
from api import send_car_number

# Создаем класс, унаследованный от QMainWindow из PyQt6.QtWidgets
class GetImage(QMainWindow):
    # Создаем элементы, которые будут отображаться в нашем приложение
    def __init__(self):
        super().__init__()
        # Передаем название нашего окна
        self.setWindowTitle('Определение номера автомобиля')
        # Создаем слой для эелементов
        layout = QVBoxLayout()
        # Создаем виджет
        widget = QWidget()
        # Ставим виджету слой из переменной layout
        widget.setLayout(layout)
        # В перемнную сохраняем элемент QLabel, в котором будет отображаться загруженное фото
        self.image = QLabel()
        # В переменную сохраняем элемент QLabel, в котором будет отображаться текст с номера авто, а начальное значение элемента задаем сами
        self.label = QLabel('Выберите изображение, чтобы отобразить номер')
        # В переменную сохраняем элемент QPushButton, с текстом на кнопке "Добавить файл"
        button = QPushButton('Выбрать файл')
        # подключаем к кнопке функцию нажатия
        button.clicked.connect(self.clicked_to_use_API)
        # Добавляем в наш слой все добавленные элементы по порядку
        layout.addWidget(self.image)
        layout.addWidget(self.label)
        layout.addWidget(button)
        # Ставим отображение перменной widget в центре 
        self.setCentralWidget(widget)
    # Создаем функцию, которая будет отправлять фото в наше API
    def clicked_to_use_API(self):
        # Добавляем виджет, чтобы наша кнопка могла работать как добавление файлов
        file = QFileDialog.getOpenFileName(self, 'Выберите файл', '/Users/Server/Desktop', 'JPG File(*.jpg)')
        # Сохраняем в переменную путь до переданного файла
        image_path = file[0]
        # Проверяем условие, что путь до картинки существует
        if not(image_path):
            # Если пути нет, то выводим, что картинка не выбрана
            self.label.setText("Изображение не выбрано.")
        else:
            # Сохраняем в переменную работу нашего API, которое возвращает текст номера
            result = send_car_number(image_path)
            # Отображаем на экране текст из нашего API
            self.label.setText(f'Предпологаемый номер изображенный на изображение: {result[0][-1][-1]}')
            # Выводим изображение с box-ом:
            # Передаем в переменную нашу картинку с box-ом
            self.n_image = result[1]
            # конвертируем ее под формат QImage
            self.convert = QImage(self.n_image, self.n_image.shape[1], self.n_image.shape[0], QImage.Format.Format_BGR888)
            # Отображаем ее на экране
            self.image.setPixmap(QPixmap.fromImage(self.convert).scaled(1200, 800))

# Создаем наше приложение, а после запускаем его
app = QApplication(sys.argv)
window = GetImage()
window.show()
app.exec()
