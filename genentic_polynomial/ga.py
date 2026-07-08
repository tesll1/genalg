import random

def slice_gap(l, r, n):
    result = []
    lenght = r - l
    piece = lenght / (n+1)
    x = l + piece
    while x < r:
        result.append(x)
        x += piece
    return result

def fit_func(sp, x):
    a0, a1, a2, a3, a4, a5, a6, a7, a8 = sp
    return a8*(x**8) + a7*(x**7) + a6*(x**6) + a5*(x**5) + a4*(x**4) + a3*(x**3) + a2*(x**2) + a1*x +a0

def start():
    l, r = map(float, input("Введите левую и правую границу промежутка: ").split())
    population_size = int(input("Введите размер первоначальной популяции: "))
    population = slice_gap(l, r, population_size)
    print(f"\nТочки на промежутке: {population}\n")
    print("Введите коэффициенты полинома 8 степени от младшего к старшему, ")
    a0, a1, a2, a3, a4, a5, a6, a7, a8 = map(float, input("ставить 0, если нет одночлена соответствующей степени: ").split())
    polinom = [a0, a1, a2, a3, a4, a5, a6, a7, a8]
    fit_func_of_x = [fit_func(polinom, x) for x in population]
    print(f"\nЗначения функции в точках: {fit_func_of_x}")

    generations = int(input("Введите количество поколений: "))
    tournament_size = int(input("Введите размер турнира: "))

    crossover_prob = float(input("Введите вероятность скрещивания: "))
    mutation_prob = float(input("Введите вероятность мутации: "))
    epsilon = 0.01

    best_x = max(population, key=lambda x: fit_func(polinom, x))
    best_f = fit_func(polinom, best_x)

    history = set(population)

    for _ in range(generations):
        fit_func_of_x = [fit_func(polinom, x) for x in population]
        
        new_pop = []
        best_idx = max(range(len(population)), key=lambda i: fit_func_of_x[i])
        new_pop.append(population[best_idx])
        while len(new_pop) < population_size:
            idx1 = random.sample(range(population_size), tournament_size)
            idx2 = random.sample(range(population_size), tournament_size)
            parent1 = population[max(idx1, key=lambda i: fit_func_of_x[i])]
            parent2 = population[max(idx2, key=lambda i: fit_func_of_x[i])]
            
            # скрещивание
            if random.random() < crossover_prob:
                alpha = random.random()
                child = random.choice([parent1 - alpha*abs(parent2 - parent1), parent2 + alpha*abs(parent2 - parent1)])
            else:
                child = random.choice([parent1, parent2])
            
            # мутация
            if random.random() < mutation_prob:
                child += epsilon
                child = max(l, min(r, child))

            new_pop.append(child)

        population = new_pop
        for x in population:
            history.add(x)
        current_best = max(population, key=lambda x: fit_func(polinom, x))
        if fit_func(polinom, current_best) > best_f:
            best_x = current_best
            best_f = fit_func(polinom, best_x)

    local_max = []
    sorted_points = sorted(history, key=lambda x: fit_func(polinom, x), reverse=True)
    for x in sorted_points:
        if any(abs(x - y) < epsilon for y in local_max):
            continue
        is_max = True
        for y in history:
            if abs(x - y) < epsilon and y != x:
                if fit_func(polinom, y) > fit_func(polinom, x):
                    is_max = False
                    break
        if is_max:
            local_max.append(x)

    for b in (l, r):
        if not any(abs(b - y) < epsilon for y in local_max):
            if b == l:
                if fit_func(polinom, l) >= fit_func(polinom, l + epsilon):
                    local_max.append(l)
            else:
                if fit_func(polinom, r) >= fit_func(polinom, r - epsilon):
                    local_max.append(r)

    print("\nНайденные локальные максимумы:")
    for x in sorted(local_max):
        fx = fit_func(polinom, x)
        print(f"x = {x:.8f}, f(x) = {fx:.8f}")
    print(f"\nГлобальный максимум: x = {best_x:.8f}, f(x) = {best_f:.8f}")

start()
