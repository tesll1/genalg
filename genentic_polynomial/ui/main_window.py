import math

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QSpinBox, QDoubleSpinBox,
    QPushButton
)

from ui.widgets import PolynomialInput, IntervalInput
from utils.parser import parse_polynomial, check_degree


class MainWindow(QMainWindow):
    """ Класс окна """
    def __init__(self):
        """ Конструктор окна """
        super().__init__()
        self.setWindowTitle("Задача о поиске максимумов") 
        self.setGeometry(350, 150, 1200, 800)
        
        # центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout()
        central.setLayout(main_layout)
        
        # левая панель
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # правая панель
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
        
        self.statusBar().showMessage("Готов к работе. Введите, сгенерируйте или загрузите полином")  # статус бар
        self.update_function_plot()                     # рисовка начального графика
    
    def create_left_panel(self):
        """ Создание левой панели """
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Группа целевая функция
        func_group = QGroupBox("Целевая функция")
        func_layout = QVBoxLayout()
        func_group.setLayout(func_layout)
        
        self.poly_input = PolynomialInput()
        self.poly_input.valueChanged.connect(self.update_function_plot)
        func_layout.addWidget(self.poly_input)
        
        hint = QLabel("Введите полином и нажмите Enter")
        hint.setStyleSheet("font-size: 15px; color: gray;")
        func_layout.addWidget(hint)

        layout.addWidget(func_group)
        
        # Группа интервал
        interval_group = QGroupBox("Интервал поиска")
        interval_layout = QVBoxLayout()
        interval_group.setLayout(interval_layout)
        
        self.interval_input = IntervalInput()
        self.interval_input.valueChanged.connect(self.update_function_plot)
        interval_layout.addWidget(self.interval_input)
        
        layout.addWidget(interval_group)
        
        # Группа параметры ГА
        ga_group = QGroupBox("Параметры ГА")
        ga_layout = QGridLayout()
        ga_group.setLayout(ga_layout)
        
        ga_layout.addWidget(QLabel("Размер популяции:"), 0, 0)
        self.pop_size = QSpinBox()
        self.pop_size.setRange(10, 1000)
        self.pop_size.setValue(100)
        ga_layout.addWidget(self.pop_size, 0, 1)
        
        ga_layout.addWidget(QLabel("Кол-во поколений:"), 1, 0)
        self.generations = QSpinBox()
        self.generations.setRange(1, 10000)
        self.generations.setValue(100)
        ga_layout.addWidget(self.generations, 1, 1)
        
        ga_layout.addWidget(QLabel("Вероятность мутации:"), 2, 0)
        self.mutation_rate = QDoubleSpinBox()
        self.mutation_rate.setRange(0.0, 1.0)
        self.mutation_rate.setSingleStep(0.01)
        self.mutation_rate.setValue(0.1)
        ga_layout.addWidget(self.mutation_rate, 2, 1)
        
        ga_layout.addWidget(QLabel("Вероятность скрещивания:"), 3, 0)
        self.crossover_rate = QDoubleSpinBox()
        self.crossover_rate.setRange(0.0, 1.0)
        self.crossover_rate.setSingleStep(0.01)
        self.crossover_rate.setValue(0.8)
        ga_layout.addWidget(self.crossover_rate, 3, 1)
        
        ga_layout.addWidget(QLabel("Размер турнира:"), 4, 0)
        self.tournament_size = QSpinBox()
        self.tournament_size.setRange(2, 100)
        self.tournament_size.setValue(10)
        ga_layout.addWidget(self.tournament_size, 4, 1)
        
        layout.addWidget(ga_group)
        
        # Группа управление
        btn_group = QGroupBox("Управление")
        btn_layout = QVBoxLayout()
        btn_group.setLayout(btn_layout)
        
        row1 = QHBoxLayout()
        self.start_btn = QPushButton("Запустить")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self.on_start_clicked)
        
        self.stop_btn = QPushButton("Стоп")
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.clicked.connect(self.on_stop_clicked)
        
        self.step_btn = QPushButton("Шаг")
        self.step_btn.clicked.connect(self.on_step_clicked)
        
        row1.addWidget(self.start_btn)
        row1.addWidget(self.stop_btn)
        row1.addWidget(self.step_btn)
        btn_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.clicked.connect(self.on_clear_clicked)
        self.reset_btn = QPushButton("Сброс")
        self.reset_btn.setObjectName("reset_btn")
        self.reset_btn.clicked.connect(self.on_reset_clicked)
        
        row2.addWidget(self.clear_btn)
        row2.addWidget(self.reset_btn)
        btn_layout.addLayout(row2)
        
        layout.addWidget(btn_group)
        layout.addStretch()
        
        return panel
    
    def create_right_panel(self):
        """ Создаёт правую панель с графиками """
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure
        
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # целевая функция + популяция
        self.fig1 = Figure(figsize=(6, 4), dpi=100)
        self.fig1.patch.set_facecolor('#ffe4e4')
        self.canvas1 = FigureCanvas(self.fig1)
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_facecolor('#ffe4e4')
        self.ax1.set_title("Целевая функция и популяция")
        self.ax1.set_xlabel("x")
        self.ax1.set_ylabel("f(x)")
        self.ax1.grid(True, alpha=0.3)
        layout.addWidget(self.canvas1)
        
        # изменение приспособленности
        self.fig2 = Figure(figsize=(6, 2), dpi=100)
        self.fig2.patch.set_facecolor('#ffe4e4') 
        self.canvas2 = FigureCanvas(self.fig2)
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_facecolor('#ffe4e4')
        self.ax2.set_title("Изменение приспособленности")
        self.ax2.set_xlabel("Поколение")
        self.ax2.set_ylabel("Приспособленность")
        self.ax2.grid(True, alpha=0.3)
        layout.addWidget(self.canvas2)
        
        self.fig1.tight_layout()
        self.fig2.tight_layout()

        return panel
    
    def update_function_plot(self):
        """ Обновляет график целевой функции """
        import numpy as np
        
        l, r = self.interval_input.get_interval()
        if l >= r:
            return
        
        poly_str = self.poly_input.get_polynomial()
        if not poly_str.strip():
            self.ax1.clear()
            self.ax1.text(0.5, 0.5, "Введите полином\nи нажмите Enter, загрузите или сгенерируйте", 
                         horizontalalignment='center', verticalalignment='center',
                         transform=self.ax1.transAxes, fontsize=14, color='gray')
            self.ax1.set_title("Целевая функция и популяция")
            self.ax1.set_xlabel("x")
            self.ax1.set_ylabel("f(x)")
            self.canvas1.draw()
            return
        
        if not check_degree(poly_str):
            self.ax1.clear()
            self.ax1.text(0.5, 0.5, "Ошибка: степень больше 8", 
                         horizontalalignment='center', verticalalignment='center',
                         transform=self.ax1.transAxes, fontsize=14, color='red')
            self.ax1.set_title("Целевая функция и популяция")
            self.ax1.set_xlabel("x")
            self.ax1.set_ylabel("f(x)")
            self.canvas1.draw()
            self.statusBar().showMessage("Ошибка: степень полинома не должна быть больше 8")
            return
        
        func = parse_polynomial(poly_str)

        x = np.linspace(l, r, 1000)
        y = []
        for i in x:
            try:
                val = func(i)
                y.append(val)
            except Exception:
                y.append(float('nan'))
        
        y = np.array(y)
        
        if np.all(np.isnan(y)):
            self.ax1.clear()
            self.ax1.text(0.5, 0.5, "Ошибка: неверное выражение", 
                         horizontalalignment='center', verticalalignment='center',
                         transform=self.ax1.transAxes, fontsize=14, color='#7cb8df')
            self.ax1.set_title("Целевая функция и популяция")
            self.ax1.set_xlabel("x")
            self.ax1.set_ylabel("f(x)")
            self.canvas1.draw()
            self.statusBar().showMessage("Ошибка: неверное выражение")
            return
        
        self.ax1.clear()
        self.ax1.plot(x, y, color='#7cb8df', linewidth=2, label='f(x)')
        self.ax1.set_title("Целевая функция и популяция")
        self.ax1.set_xlabel("x")
        self.ax1.set_ylabel("f(x)")
        self.ax1.grid(True, alpha=0.3)
        self.ax1.legend()
        self.canvas1.draw()


    # Обработка событий
    def on_start_clicked(self):
        """ Запуск алгоритма """
        poly_str = self.poly_input.get_polynomial()
        func = parse_polynomial(poly_str)
        try:
            test_val = func(0.0)
            if not math.isfinite(test_val):
                self.statusBar().showMessage("Ошибка: неверный полином")
                return
        except Exception:
            self.statusBar().showMessage("Ошибка: неверный полином")
            return
        
        self.statusBar().showMessage("Запуск алгоритма")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        print("Запуск генетического алгоритма")
        print(f"Полином: {self.poly_input.get_polynomial()}")
        print(f"Интервал: {self.interval_input.get_interval()}")
        print(f"Популяция: {self.pop_size.value()}")
        print(f"Поколений: {self.generations.value()}")
        print(f"Мутация: {self.mutation_rate.value()}")
        print(f"Скрещивание: {self.crossover_rate.value()}")
        print(f"Турнир: {self.tournament_size.value()}")
        
        self.statusBar().showMessage("Алгоритм запущен")
    

    def on_stop_clicked(self):
        """ Остановка алгоритма """
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        print("Остановка алгоритма")
        self.statusBar().showMessage("Алгоритм остановлен")
    

    def on_step_clicked(self):
        """ Один шаг алгоритма """
        print("Выполнение шага алгоритма")
        self.statusBar().showMessage("Выполнен шаг алгоритма")
    

    def on_clear_clicked(self):
        """ Очистка графиков """
        self.ax1.clear()
        self.ax1.set_title("Целевая функция и популяция")
        self.ax1.set_xlabel("x")
        self.ax1.set_ylabel("f(x)")
        self.ax1.grid(True, alpha=0.3)
        self.canvas1.draw()
        
        self.ax2.clear()
        self.ax2.set_title("Изменение приспособленности")
        self.ax2.set_xlabel("Поколение")
        self.ax2.set_ylabel("Приспособленность")
        self.ax2.grid(True, alpha=0.3)
        self.canvas2.draw()
        
        self.statusBar().showMessage("Результаты очищены")
    

    def on_reset_clicked(self):
        """ Сброс параметров """
        self.poly_input.set_polynomial("x^5 - 3*x^2 + 4")
        self.interval_input.set_interval(-10, 10)
        self.pop_size.setValue(100)
        self.generations.setValue(100)
        self.mutation_rate.setValue(0.1)
        self.crossover_rate.setValue(0.8)
        self.tournament_size.setValue(10)
        self.update_function_plot()
        self.statusBar().showMessage("Параметры сброшены")