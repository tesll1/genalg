from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QLabel, QDoubleSpinBox, 
    QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
)
from PyQt5.QtCore import pyqtSignal
import random

class PolynomialInput(QWidget):
    """ Виджет для ввода полинома """
    valueChanged = pyqtSignal(str)      # сигнал, отправляемый при изменении текста
    
    def __init__(self, parent=None):
        """ Конструктор виджета """
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
       
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Например: x^5 - 3*x^2 + 4")
        self.line_edit.setText("x^5 - 3*x^2 + 4")
        self.line_edit.returnPressed.connect(self.on_enter_pressed)     # подключение сигнала
        layout.addWidget(self.line_edit)
    
        btn_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("Загрузить")
        self.load_btn.setFixedHeight(32)
        self.load_btn.clicked.connect(self.load_from_file)
        btn_layout.addWidget(self.load_btn)
        
        self.random_btn = QPushButton("Случайный")
        self.random_btn.setFixedHeight(32)
        self.random_btn.clicked.connect(self.generate_random)
        btn_layout.addWidget(self.random_btn)
        
        layout.addLayout(btn_layout)

    def get_polynomial(self) -> str:
        """ Возвращает текущий текст полинома """
        return self.line_edit.text()
    
    def set_polynomial(self, text: str):
        """ Устанавливает текст полинома """
        self.line_edit.setText(text)
        self.valueChanged.emit(text)
    
    def on_enter_pressed(self):
        """ Обработка текста после нажатия Enter """
        text = self.line_edit.text().strip()
        if text:
            self.valueChanged.emit(text)

    def load_from_file(self):
        """ Загружает полином из текстового файла """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл с полиномом",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            if not lines:
                self.line_edit.setPlaceholderText("Файл пуст!")
                return
            
            polynomial = lines[0]
            self.set_polynomial(polynomial)
            
        except Exception as e:
            self.line_edit.setPlaceholderText(f"Ошибка: {str(e)}")
    
    def generate_random(self):
        """ Генерирует случайный полином """
        degree = random.randint(0, 8)

        coefficients = []
        for i in range(degree + 1):
            coef = 0
            while coef == 0:
                coef = random.randint(-10, 10)
            coefficients.append(coef)
        
        terms = []
        for i, coef in enumerate(coefficients):
            if coef == 0:
                continue
            
            if i == 0:
                terms.append(str(coef))
            elif i == 1:
                if coef == 1:
                    terms.append("x")
                elif coef == -1:
                    terms.append("-x")
                else:
                    terms.append(f"{coef}*x")
            else:
                if coef == 1:
                    terms.append(f"x^{i}")
                elif coef == -1:
                    terms.append(f"-x^{i}")
                else:
                    terms.append(f"{coef}*x^{i}")
        
        if not terms:
            polynomial = "0"
        else:
            polynomial = " + ".join(terms)
            polynomial = polynomial.replace("+ -", "- ")
        
        self.set_polynomial(polynomial)


class IntervalInput(QWidget):
    """ Виджет для ввода интервала [l, r] """
    valueChanged = pyqtSignal(float, float) # сигнал с двумя числами с плавающей точкой
    
    def __init__(self, parent=None):
        """ Конструктор виджета ввода интервала """
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        layout.addWidget(QLabel("["))
        self.l_spin = QDoubleSpinBox()
        self.l_spin.setRange(-50, 50)
        self.l_spin.setValue(-10)
        
        self.l_spin.valueChanged.connect(self.emit_value) # подключение сигнала

        layout.addWidget(self.l_spin)
        layout.addWidget(QLabel("    ,"))

        self.r_spin = QDoubleSpinBox()
        self.r_spin.setRange(-50, 50)
        self.r_spin.setValue(10)
        self.r_spin.valueChanged.connect(self.emit_value)
        layout.addWidget(self.r_spin)
        layout.addWidget(QLabel("     ]"))
    
    def get_interval(self):
        """ Возвращает текущие значения интервала """
        return self.l_spin.value(), self.r_spin.value()
    
    def set_interval(self, l: float, r: float):
        """ Устанавливает интервал """
        self.l_spin.setValue(l)
        self.r_spin.setValue(r)
    
    def emit_value(self):
        """ Отправляет сигнал """
        self.valueChanged.emit(self.l_spin.value(), self.r_spin.value())