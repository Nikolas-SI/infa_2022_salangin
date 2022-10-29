def overline_x(x):
    sum_x = 0
    for i in x:
        sum_x += float(i)
    return sum_x / len(x)


def sigma_random(x):
    sr_x = overline_x(x)
    a = 0
    for i in x:
        a += (sr_x - float(i)) ** 2
    return (a / (len(x) * (len(x) - 1))) ** 0.5

sigma_sys = 1

def sigabs(x):
    return (sigma_random(x) ** 2 + sigma_sys ** 2) ** 0.5
    print((sigma_random(x) ** 2 + sigma_sys ** 2) ** 0.5)


class Var():
    def __init__(self, value, sigma):
        self.value = value
        self.sigma = sigma

    def __add__(x, y):
        return (Var(x.value + y.value, (x.sigma ** 2 + y.sigma ** 2) ** 0.5))

    def __sub__(x, y):
        return (Var(x.value - y.value, (x.sigma ** 2 + y.sigma ** 2) ** 0.5))

    def __mul__(x, y):
        return (
            Var(x.value * y.value, ((x.sigma / x.value) ** 2 + (y.sigma / y.value) ** 2) ** 0.5 * (x.value * y.value)))

    def __truediv__(x, y):
        return (
            Var(x.value / y.value, ((x.sigma / x.value) ** 2 + (y.sigma / y.value) ** 2) ** 0.5 * (x.value / y.value)))

    def write(self):
        print(self.value, self.sigma)
