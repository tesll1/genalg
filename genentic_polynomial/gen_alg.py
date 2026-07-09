import random
import math
import copy

class GeneticAlgorithm:
    def __init__(self, func, l, r, pop_size, generations,
                 mutation_rate, crossover_rate, tournament_size,
                 epsilon=0.01, sigma=0.5, max_no_improve=20):
        """
        :param func: функция f(x) (исходный полином)
        :param l, r: интервал
        :param pop_size: размер популяции
        :param generations: максимальное число поколений
        :param mutation_rate: вероятность мутации
        :param crossover_rate: вероятность скрещивания
        :param tournament_size: размер турнира
        :param epsilon: шаг мутации
        :param sigma: ширина значения для штрафа
        :param max_no_improve: сколько поколений без новых максимумов для остановки
        """
        self.func = func
        self.l = l
        self.r = r
        self.pop_size = pop_size
        self.max_generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        self.epsilon = epsilon
        self.sigma = sigma
        self.max_no_improve = max_no_improve

        # состояние
        self.generation = 0
        self.population = self._init_population()
        self.history_populations = []   # для возврата назад
        self.found_maximum = []          # список (x, f(x))
        self.best_fitness_history = []  # для графика
        self.stopped = False
        self.finished = False

        # сохраняем начальное состояние
        self._save_state()

    def _init_population(self):
        """ Создаёт начальную популяцию равномерно на интервале """
        l, r, n = self.l, self.r, self.pop_size
        length = r - l
        step = length / (n + 1)
        return [l + step * (i + 1) for i in range(n)]

    def _fitness(self, x):
        """ Штрафная функция: f(x) - сумма штрафов"""
        f_val = self.func(x)
        summa = 0.0
        for (mx, mf) in self.found_maximum:
            summa += abs(mf) * math.exp(-((x - mx) ** 2) / (2 * self.sigma ** 2))
        return f_val - summa

    def _find_local_maximum(self, points):
        """ Находит локальные максимумы среди списка точек """
        maximum = []
        # сортируем точки
        sorted_points = sorted(points)
        eps = self.epsilon
        for i, x in enumerate(sorted_points):
            # проверяем близость к уже найденным
            if any(abs(x - mx) < eps for mx, _ in self.found_maximum):
                continue
            # проверяем соседние точки
            left_ok = True
            right_ok = True
            if i > 0:
                left_ok = self.func(x) >= self.func(sorted_points[i-1]) - 1e-9
            if i < len(sorted_points)-1:
                right_ok = self.func(x) >= self.func(sorted_points[i+1]) - 1e-9
            if left_ok and right_ok:
                if self.func(x) >= self.func(x - eps) and self.func(x) >= self.func(x + eps):
                    maximum.append(x)
        return maximum

    def _update_maximum(self):
        """ Обновляет список найденных максимумов"""
        all_points = set()
        for pop in self.history_populations:
            all_points.update(pop[0])
        all_points.update(self.population)

        new_maximum = self._find_local_maximum(list(all_points))
        for x in new_maximum:
            # проверяем, не добавлен ли уже
            if not any(abs(x - mx) < self.epsilon for mx, _ in self.found_maximum):
                self.found_maximum.append((x, self.func(x)))

    def _step(self):
        if self.stopped or self.finished:
            return

        fitness_vals = [self._fitness(x) for x in self.population]

        best_idx = max(range(len(self.population)), key=lambda i: fitness_vals[i])
        new_pop = [self.population[best_idx]]

        while len(new_pop) < self.pop_size:
            idx1 = random.sample(range(self.pop_size), self.tournament_size)
            idx2 = random.sample(range(self.pop_size), self.tournament_size)
            parent1 = self.population[max(idx1, key=lambda i: fitness_vals[i])]
            parent2 = self.population[max(idx2, key=lambda i: fitness_vals[i])]

            # скрещивание
            if random.random() < self.crossover_rate:
                alpha = random.random()
                child = random.choice([
                    parent1 - alpha * abs(parent2 - parent1),
                    parent2 + alpha * abs(parent2 - parent1)
                ])
            else:
                child = random.choice([parent1, parent2])

            # мутация
            if random.random() < self.mutation_rate:
                child += self.epsilon * random.uniform(-1, 1)
                child = max(self.l, min(self.r, child))

            new_pop.append(child)

        self.population = new_pop
        self.generation += 1

        self._update_maximum()

        best_x = max(self.population, key=lambda x: self.func(x))
        self.best_fitness_history.append(self.func(best_x))

        self._save_state()

        # проверка критерия остановки
        if self.generation >= self.max_generations:
            self.finished = True
            return

        if len(self.history_populations) > self.max_no_improve:
            recent = self.history_populations[-self.max_no_improve:]
            first_maximum = recent[0][1]
            last_maximum = recent[-1][1]
            if len(first_maximum) == len(last_maximum):
                if all(abs(a[0] - b[0]) < 1e-6 for a, b in zip(first_maximum, last_maximum)):
                    self.finished = True
                    return

    def _save_state(self):
        """ Сохраняет текущее состояние """
        state = (
            copy.deepcopy(self.population),
            copy.deepcopy(self.found_maximum),
            self.generation,
            copy.deepcopy(self.best_fitness_history)
        )
        self.history_populations.append(state)

    def step(self):
        """Выполняет один шаг, если алгоритм не завершён"""
        if not self.finished and not self.stopped:
            self._step()
        return self.get_current_state()

    def run(self, callback=None):
        """ Запускает алгоритм до завершения """
        while not self.finished and not self.stopped:
            self._step()
            if callback:
                callback(self.get_current_state())

    def stop(self):
        self.stopped = True

    def get_current_state(self):
        """ Возвращает текущие """
        return {
            'population': self.population,
            'found_maximum': self.found_maximum,
            'generation': self.generation,
            'best_fitness_history': self.best_fitness_history,
            'finished': self.finished
        }

    def go_back(self, steps=1):
        """ Откатывает состояние на steps шагов назад """
        if len(self.history_populations) <= steps + 1:
            return False
        # удаляем последние steps состояний
        for _ in range(steps):
            self.history_populations.pop()
        # восстанавливаем последнее сохранённое состояние
        pop, maximum, gen, hist = self.history_populations[-1]
        self.population = copy.deepcopy(pop)
        self.found_maximum = copy.deepcopy(maximum)
        self.generation = gen
        self.best_fitness_history = copy.deepcopy(hist)
        self.finished = False
        self.stopped = False
        return True

    def get_history_length(self):
        return len(self.history_populations)