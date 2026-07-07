from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QLabel, QDoubleSpinBox, 
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import pyqtSignal


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
    
    def get_polynomial(self) -> str:
        """ Возвращает текущий текст полинома """
        return self.line_edit.text()
    
    def set_polynomial(self, text: str):
        """ Устанавливает текст полинома """
        self.line_edit.setText(text)
    
    def on_enter_pressed(self):
        """ Обработка текста после нажатия Enter """
        text = self.line_edit.text().strip()
        if text:
            self.valueChanged.emit(text)


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
        self.l_spin.setRange(-1000, 1000)
        self.l_spin.setValue(-10)
        
        self.l_spin.valueChanged.connect(self.emit_value) # подключение сигнала

        layout.addWidget(self.l_spin)
        layout.addWidget(QLabel("    ,"))

        self.r_spin = QDoubleSpinBox()
        self.r_spin.setRange(-1000, 1000)
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