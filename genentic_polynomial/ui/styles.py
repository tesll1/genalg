COLORS = {
    'blue': "#7cb8df",      # кнопки, акценты
    'green': "#85dca9",     # кнопка запуска
    'red': "#ff6a6a",       # кнопка стопа
    'orange': "#ffc76c",    # кнопка сброса
    'gray': "#99a3a4",      # нпс элементы
    'dark': "#520000",      # фон статусбаров, зоголовков
    'pink': "#fcc4c4",      # фон окна
    'white': "#ffe4e4",     # фон групп
    'border': "#360101",    # рамки
    'text': "#000000",      # текст
}


STYLES = f"""
/* Основное окно */
QMainWindow {{
    background-color: {COLORS['pink']};    /* фон */
}}


/* Группы */
QGroupBox {{
    font-weight: bold;                      /* жирный шрифт для заголовка */
    border: 2px solid {COLORS['border']};   /* рамка */
    border-radius: 8px;                     /* скругленные углы */
    margin-top: 12px;                       /* отступ сверху для заголовка */
    padding-top: 12px;                      /* внутренний отступ сверху */
    background-color: {COLORS['white']};    /* фон внутри группы */
}}

/* заголовок группы */
QGroupBox::title {{
    left: 10px;                             /* отступ слева для заголовка */
    padding: 0 10px;                        /* отступы вокруг текста заголовка */
    color: {COLORS['dark']};                /* цвет текста заголовка */
}}


/* Поля ввода */
QLineEdit, QSpinBox, QDoubleSpinBox {{
    padding: 6px 8px;                       /* внутренние отступы */
    border: 1px solid #bdc3c7;              /* рамка */
    border-radius: 4px;                     /* углы */
    background-color: {COLORS['white']};    /* фон */
}}

/* поле в фокусе: */
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {COLORS['blue']};     /* рамка становится толще */
}}


/* Кнопки */
QPushButton {{
    padding: 8px 16px;                      /* внутренние отступы */
    border: none;
    border-radius: 5px;                     /* углы */
    font-weight: bold;                      /* жирный шрифт */
    color: {COLORS['white']};               /* текст */
    background-color: {COLORS['blue']};     /* фон */
}}

/* наведение мыши: */
QPushButton:hover {{
    background-color: #2980b9;           /* темнееет */
}}

/* кнопка выкл: */
QPushButton:disabled {{
    background-color: #bdc3c7;           /* фон */
    color: #7f8c8d;                      /* текст */
}}

/* Кнопки базовые */
/* запустить: */
QPushButton#start_btn {{
    background-color: {COLORS['green']};
}}
QPushButton#start_btn:hover {{
    background-color: #27ae60;           /* темнеет при наведении */
}}

/* стоп: */
QPushButton#stop_btn {{
    background-color: {COLORS['red']};
}}
QPushButton#stop_btn:hover {{
    background-color: #c0392b;
}}

/* сброс: */
QPushButton#reset_btn {{
    background-color: {COLORS['orange']};
}}
QPushButton#reset_btn:hover {{
    background-color: #e67e22;
}}

/* назад */
QPushButton#back_btn {{
    background-color: #f39c12;
}}
QPushButton#back_btn:hover {{
    background-color: #d68910;
}}

/* финиш */
QPushButton#finish_btn {{
    background-color: #8e44ad;
}}
QPushButton#finish_btn:hover {{
    background-color: #732d91;
}}


/* Статус-бар: */
QStatusBar {{
    background-color: {COLORS['dark']};     /* фон */
    color: {COLORS['pink']};               /* текст */
    padding: 4px 8px;                       /* внутренние отступы */
}}

/* Таблица результатов */
QTableWidget {{
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    background-color: {COLORS['white']};
}}

QTableWidget::item:selected {{
    background-color: {COLORS['blue']};
    color: {COLORS['white']};
}}

QHeaderView::section {{
    background-color: {COLORS['dark']};
    color: {COLORS['pink']};
    padding: 6px;
    border: none;
}}
"""


def apply_styles(app):
    """Применяет стили к приложению"""
    app.setStyleSheet(STYLES)