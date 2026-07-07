import math


def parse_polynomial(poly_str: str):
    """ Преобразует строку полинома в функцию """
    poly_str = poly_str.strip()

    if not poly_str:
        return lambda x: 0.0
    
    expr = poly_str.replace('^', '**')

    if expr.endswith(('+', '-', '*', '/', '(')):
        return lambda x: float('nan')

    if expr.count('(') != expr.count(')'):
        return lambda x: float('nan')

    mat_dict = {
        'x': 0,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'log10': math.log10,
        'sqrt': math.sqrt,
        'abs': abs,
        'pi': math.pi,
        'e': math.e,
    }
    

    def func(x):
        """ Вычисляет значение полинома в точке x """
        mat_dict['x'] = x
        try:
            result = eval(expr, {"__builtins__": {}}, mat_dict)
            return float(result) if isinstance(result, (int, float)) else float('nan')
        except Exception:
            return float('nan')
    
    return func


def get_variable_name(poly_str: str):
    """ Определяет имя переменной в полиноме """
    import re
    
    letters = re.findall(r'[a-zA-Z]', poly_str)
    function_names = {'sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'abs'}
    for letter in letters:
        if letter not in function_names:
            return letter
    
    return 'x'