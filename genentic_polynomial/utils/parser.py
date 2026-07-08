import re

def parse_polynomial(poly_str):
    """ Преобразует строку полинома в функцию """
    poly_str = poly_str.strip()

    if not poly_str:
        return lambda x: 0.0
    
    expr = poly_str.replace('^', '**')

    if expr.endswith(('+', '-', '*', '/', '(')):
        return lambda x: float('nan')

    if expr.count('(') != expr.count(')'):
        return lambda x: float('nan')

    if not check_degree(poly_str):
        return lambda x: float('nan')
    

    def func(x):
        try:
            result = eval(expr, {"__builtins__": {}}, {"x": x})
            return float(result) if isinstance(result, (int, float)) else float('nan')
        except Exception:
            return float('nan')
    
    return func


def check_degree(poly_str):
    """ Проверка, что степень полинома не больше 8 """
    matches = re.findall(r'x\^(\d+)', poly_str)
    
    max_degree = 0
    for match in matches:
        degree = int(match)
        if degree > max_degree:
            max_degree = degree
    
    if 'x' in poly_str and max_degree < 1:
        max_degree = 1
    
    return max_degree <= 8