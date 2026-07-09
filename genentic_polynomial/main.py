import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow, apply_styles


def main():
    """
    Главная функция, запускает приложение
    """
    app = QApplication(sys.argv)    # объект приложения
    apply_styles(app)               # применение стилей
    window = MainWindow()           # главное окно
    window.show()
    sys.exit(app.exec_())           # запуск цикла обработки событий


if __name__ == "__main__":
    main()

# -x^2 + 1
# -x^4 + 4*x^3 - 4*x^2