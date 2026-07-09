import math

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QSpinBox, QDoubleSpinBox,
    QPushButton, QListWidget, QApplication, QScrollArea
)

from PyQt5.QtCore import QTimer

from ui.widgets import PolynomialInput, IntervalInput
from utils.parser import parse_polynomial, check_degree

from gen_alg import GeneticAlgorithm

class MainWindow(QMainWindow):
    """ Класс окна """
    def __init__(self):
        """ Конструктор окна """
        super().__init__()
        self.setWindowTitle("Задача о поиске максимумов") 
        self.setGeometry(350, 50, 1200, 800)
        
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

        # генетический алгоритм
        self.gen_alg = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer_interval = 100 
        self.selected_maximum = None

        
        self.statusBar().showMessage("Готов к работе. Введите, сгенерируйте или загрузите полином")  # статус бар
        self.update_function_plot()                     # рисовка начального графика
        self.update_fitness_plot()

    def create_left_panel(self):
        """ Создание левой панели """
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(2)  # AlwaysOff
        scroll.setVerticalScrollBarPolicy(1)    # AsNeeded

        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Группа целевая функция
        func_group = QGroupBox("Целевая функция")
        func_layout = QVBoxLayout()
        func_group.setLayout(func_layout)
        
        self.poly_input = PolynomialInput()
        self.poly_input.valueChanged.connect(self.on_params_changed)
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
        self.interval_input.valueChanged.connect(self.on_params_changed)
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

        ga_layout.addWidget(QLabel("Поколений без улучшений"), 5, 0)
        self.max_no_improve = QSpinBox()
        self.max_no_improve.setRange(1, 1000)
        self.max_no_improve.setValue(20)
        ga_layout.addWidget(self.max_no_improve, 5, 1)

        ga_layout.addWidget(QLabel("Ширина штрафа:"), 6, 0)
        self.sigma = QDoubleSpinBox()
        self.sigma.setRange(0.01, 10.0)
        self.sigma.setSingleStep(0.1)
        self.sigma.setValue(0.5)
        ga_layout.addWidget(self.sigma, 6, 1)

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

        self.back_btn = QPushButton("Назад")
        self.back_btn.setObjectName("back_btn")
        self.back_btn.clicked.connect(self.on_back_clicked)

        self.finish_btn = QPushButton("Финиш")
        self.finish_btn.setObjectName("finish_btn")
        self.finish_btn.clicked.connect(self.on_finish_clicked)
        
        row2.addWidget(self.clear_btn)
        row2.addWidget(self.reset_btn)
        row2.addWidget(self.back_btn)
        row2.addWidget(self.finish_btn)
        btn_layout.addLayout(row2)
        
        layout.addWidget(btn_group)

        # Группа найденные максимумы
        maximum_group = QGroupBox("Найденные максимумы")
        maximum_layout = QVBoxLayout()
        maximum_group.setLayout(maximum_layout)
        self.maximum_list = QListWidget()
        self.maximum_list.itemClicked.connect(self.on_maximum_selected)
        maximum_layout.addWidget(self.maximum_list)
        layout.addWidget(maximum_group)

        layout.addStretch()
        scroll.setWidget(panel)
        self.stop_btn.setEnabled(False)
        self.back_btn.setEnabled(False)
        self.finish_btn.setEnabled(False)
        
        return scroll
    
    def create_right_panel(self):
        """ Создаёт правую панель с графиками """
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
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

        toolbar1 = NavigationToolbar(self.canvas1, self)
        layout.addWidget(toolbar1)
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

        toolbar2 = NavigationToolbar(self.canvas2, self)
        layout.addWidget(toolbar2)
        layout.addWidget(self.canvas2)

        self.fig1.tight_layout()
        self.fig2.tight_layout()

        return panel
    
    def on_params_changed(self):
        """ При изменении полинома или интервала сбрасывается Генетический алгоритм """
        self.selected_maximum = None
        self.reset_gen_alg()
        self.update_function_plot()
        self.update_fitness_plot()

    def reset_gen_alg(self):
        self.gen_alg = None
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.step_btn.setEnabled(True)
        self.back_btn.setEnabled(False)
        self.finish_btn.setEnabled(False)
        self.maximum_list.clear()

    def get_gen_alg_params(self):
        poly_str = self.poly_input.get_polynomial()
        func = parse_polynomial(poly_str)
        l, r = self.interval_input.get_interval()
        pop_size = self.pop_size.value()
        generations = self.generations.value()
        mutation = self.mutation_rate.value()
        crossover = self.crossover_rate.value()
        tournament = self.tournament_size.value()
        max_no_improve = self.max_no_improve.value()
        sigma = self.sigma.value()
        return func, l, r, pop_size, generations, mutation, crossover, tournament, max_no_improve, sigma

    def init_gen_alg(self):
        if self.gen_alg is not None:
            return
        try:
            func, l, r, pop_size, generations, mutation, crossover, tournament, max_no_improve, sigma = self.get_gen_alg_params()
            # проверка функции
            test_val = func(0.0)
            if not math.isfinite(test_val):
                self.statusBar().showMessage("Ошибка: неверный полином")
                return None
            self.gen_alg = GeneticAlgorithm(
                func=func, l=l, r=r, pop_size=pop_size,
                generations=generations,
                mutation_rate=mutation, crossover_rate=crossover,
                tournament_size=tournament,
                epsilon=0.01, sigma=sigma, max_no_improve=max_no_improve
            )
            self.back_btn.setEnabled(False)
            self.finish_btn.setEnabled(True)
            return self.gen_alg
        except Exception as e:
            self.statusBar().showMessage(f"Ошибка инициализации: {e}")
            return None

    def update_plots_from_gen_alg(self):
        if self.gen_alg is None:
            return
        state = self.gen_alg.get_current_state()
        self.update_function_plot(population=state['population'], maximum=state['found_maximum'], selected=self.selected_maximum)
        self.update_fitness_plot(history=state['best_fitness_history'])
        # обновляем список максимумов
        self.maximum_list.clear()
        for i, (x, fx) in enumerate(state['found_maximum']):
            self.maximum_list.addItem(f"x={x:.4f}, f={fx:.4f}")
        if state['finished']:
            self.statusBar().showMessage(f"Алгоритм завершён на поколении {state['generation']}")
            self.stop_btn.setEnabled(False)
            self.start_btn.setEnabled(True)
            self.step_btn.setEnabled(True)
            self.timer.stop()
        else:
            self.statusBar().showMessage(f"Поколение {state['generation']}")
    
    def update_function_plot(self, population=None, maximum=None, selected=None):
        """ Обновляет график целевой функции """
        import numpy as np
        import math
        
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
                if math.isnan(val) or math.isinf(val):
                    y.append(float('nan'))
                else:
                    y.append(val)
            except Exception:
                y.append(float('nan'))
        
        y = np.array(y)
        
        if np.all(np.isnan(y)):
            self.ax1.clear()
            self.ax1.text(0.5, 0.5, "Ошибка: неверное выражение", 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax1.transAxes, fontsize=14, color='red')
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

        if population is not None and isinstance(population, (list, tuple)):
            pop_x = []
            pop_y = []
            for xi in population:
                val = func(xi)
                if not math.isnan(val) and math.isfinite(val):
                    pop_x.append(xi)
                    pop_y.append(val)
            if pop_x:
                self.ax1.scatter(pop_x, pop_y, color='#2ecc71', s=30, alpha=0.6, label='Популяция')

        if maximum is not None and isinstance(maximum, (list, tuple)):
            valid_maximum = []
            for m in maximum:
                if isinstance(m, (tuple, list)) and len(m) == 2:
                    try:
                        float(m[0])
                        float(m[1])
                        valid_maximum.append(m)
                    except (TypeError, ValueError):
                        pass
            if valid_maximum:
                mx = [m[0] for m in valid_maximum]
                my = [m[1] for m in valid_maximum]
                self.ax1.scatter(mx, my, color='red', s=100, marker='*', label='Максимумы', zorder=5)

        if selected is not None:
            sx, sy = selected
            self.ax1.scatter([sx], [sy], color='yellow', s=200, marker='o', 
                            edgecolors='black', linewidth=2, label='Выбранный максимум', zorder=10)
            self.ax1.annotate(f'x={sx:.4f}', (sx, sy), xytext=(5, 5), 
                            textcoords='offset points', fontsize=10, color='darkred')

        self.ax1.relim()
        self.ax1.autoscale_view()
        
        y_min, y_max = self.ax1.get_ylim()
        if math.isfinite(y_min) and math.isfinite(y_max) and y_max > y_min:
            y_range = y_max - y_min
            if y_range > 1e6:
                y_range = 1e6
            self.ax1.set_ylim(y_min - 0.15 * y_range, y_max + 0.15 * y_range)

        self.ax1.legend()
        self.canvas1.draw()

    def update_fitness_plot(self, history=None):
        self.ax2.clear()
        self.ax2.set_title("Изменение приспособленности")
        self.ax2.set_xlabel("Поколение")
        self.ax2.set_ylabel("Лучшее f(x)")
        self.ax2.grid(True, alpha=0.3)
        if history and len(history) > 0:
            self.ax2.plot(range(1, len(history)+1), history, color='#e74c3c', linewidth=2)
        self.canvas2.draw()


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
        
        if self.gen_alg is None:
            if self.init_gen_alg() is None:
                return
        if self.gen_alg.finished:
            self.statusBar().showMessage("Алгоритм уже завершён. Нажмите Сброс для нового запуска.")
            return
        
        self.statusBar().showMessage("Запуск алгоритма")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.step_btn.setEnabled(False)
        self.back_btn.setEnabled(False)
        self.finish_btn.setEnabled(False)
        self.timer.start(self.timer_interval)
        
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
        if self.gen_alg:
            self.gen_alg.stop()

        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.step_btn.setEnabled(True)
        self.back_btn.setEnabled(self.gen_alg is not None and self.gen_alg.get_history_length() > 1)
        self.finish_btn.setEnabled(True)
        self.statusBar().showMessage("Алгоритм остановлен")
    
    def on_step_clicked(self):
        """ Один шаг алгоритма """
        if self.gen_alg is None:
            if self.init_gen_alg() is None:
                return
        
        if self.gen_alg.finished:
            self.statusBar().showMessage("Алгоритм уже завершён")
            return
        
        print("Выполнение шага алгоритма")
        self.gen_alg.step()
        self.update_plots_from_gen_alg()
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.step_btn.setEnabled(True)
        self.back_btn.setEnabled(self.gen_alg.get_history_length() > 1)
        self.finish_btn.setEnabled(not self.gen_alg.finished)
        
        if self.gen_alg.finished:
            self.statusBar().showMessage(f"Алгоритм завершён на поколении {self.gen_alg.generation}")
            self.finish_btn.setEnabled(False)
        else:
            self.statusBar().showMessage(f"Выполнен шаг, поколение {self.gen_alg.generation}")
    
    def on_finish_clicked(self):
        """Быстрый прогон всех оставшихся поколений без анимации"""
        if self.gen_alg is None or self.gen_alg.finished:
            return
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.step_btn.setEnabled(False)
        self.back_btn.setEnabled(False)
        self.finish_btn.setEnabled(False)
        
        self.statusBar().showMessage("Быстрый прогон")
        
        self.finish_timer = QTimer()
        self.finish_timer.timeout.connect(self._finish_step)
        self.finish_timer.start(10)

    def _finish_step(self):
        """ Один шаг быстрого прогона """
        if self.gen_alg is None or self.gen_alg.finished or self.gen_alg.stopped:
            self.finish_timer.stop()
            self.update_plots_from_gen_alg()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.step_btn.setEnabled(True)
            self.back_btn.setEnabled(self.gen_alg and self.gen_alg.get_history_length() > 1)
            self.finish_btn.setEnabled(False)
            self.statusBar().showMessage("Финиш выполнен" if not self.gen_alg.stopped else "Остановлено")
            return
        
        self.gen_alg.step()
        if self.gen_alg.generation % 10 == 0:
            self.update_plots_from_gen_alg()
            QApplication.processEvents()


    def on_back_clicked(self):
        if self.gen_alg and self.gen_alg.go_back(1):
            self.update_plots_from_gen_alg()
            self.back_btn.setEnabled(self.gen_alg.get_history_length() > 1)
            self.statusBar().showMessage("Возврат на шаг назад")
            if self.gen_alg.finished:
                self.start_btn.setEnabled(True)
                self.stop_btn.setEnabled(False)
                self.step_btn.setEnabled(True)
                self.finish_btn.setEnabled(False)
        else:
            self.statusBar().showMessage("Нет шагов для возврата")

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
        
        self.maximum_list.clear()
        self.selected_maximum = None
        self.reset_gen_alg()
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
        self.max_no_improve.setValue(20)
        self.sigma.setValue(0.5)
        self.selected_maximum = None
        self.reset_gen_alg()
        self.update_function_plot()
        self.update_fitness_plot()
        self.statusBar().showMessage("Параметры сброшены")

    def on_timer_tick(self):
        if self.gen_alg is None:
            self.timer.stop()
            return
        if self.gen_alg.finished or self.gen_alg.stopped:
            self.timer.stop()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.step_btn.setEnabled(True)
            self.back_btn.setEnabled(self.gen_alg.get_history_length() > 1)
            self.finish_btn.setEnabled(False)
            self.update_plots_from_gen_alg()
            return
        self.gen_alg.step()
        self.update_plots_from_gen_alg()
        self.back_btn.setEnabled(self.gen_alg.get_history_length() > 1)

    def on_maximum_selected(self, item):
        if self.gen_alg is None or not self.gen_alg.found_maximum:
            self.selected_maximum = None
            return

        text = item.text()
        try:
            # Извлекаем x из строки
            parts = text.split(',')
            x_part = parts[0].strip()     
            x_str = x_part.split('=')[1].strip()
            x = float(x_str)

            # Ищем точку в списке найденных максимумов
            eps = 1e-6
            found = None
            for mx, mf in self.gen_alg.found_maximum:
                if abs(mx - x) < eps:
                    found = (mx, mf)
                    break
            if found:
                self.selected_maximum = found
            else:
                self.selected_maximum = None
        except Exception:
            self.selected_maximum = None

        # Обновляем график с выбранной точкой
        state = self.gen_alg.get_current_state()
        self.update_function_plot(
            population=state['population'],
            maximum=state['found_maximum'],
            selected=self.selected_maximum
        )