from functools import reduce


class ErrorCalculator:
    error_list = [0]

    def __init__(self, error_min=0, error_max=4):
        self.min = error_min
        self.max = error_max
        self.renew()

    def renew(self):
        self.error_list = [0]

    def append(self, value):
        self.error_list.append(value)

    def last_n_average_percent(self, n):
        return round((reduce(lambda x, y: x + y, self.error_list[-n:]) / n) / (self.max - self.min) * 100, 2)

    def last_n_total_value(self, n):
        return round(reduce(lambda x, y: x + y, self.error_list[-n:]), 2)

    def last_n_average_value(self, n):
        return round(reduce(lambda x, y: x + y, self.error_list[-n:]) / n, 2)

    def first_n_average_percent(self, n):
        return round((reduce(lambda x, y: x + y, self.error_list[:n]) / n) / (self.max - self.min) * 100, 2)

    def first_n_total_value(self, n):
        return round(reduce(lambda x, y: x + y, self.error_list[:n]), 2)

    def first_n_average_value(self, n):
        return round(reduce(lambda x, y: x + y, self.error_list[:n]) / n, 2)

    @property
    def total_value(self):
        return reduce(lambda x, y: x + y, self.error_list)

    @property
    def total_count(self):
        return len(self.error_list)

    @property
    def average_value(self):
        return round(reduce(lambda x, y: x + y, self.error_list) / len(self.error_list), 2)

    @property
    def average_percent(self):
        return round((reduce(lambda x, y: x + y, self.error_list) / len(self.error_list)) /
                     (self.max - self.min) * 100, 2)
