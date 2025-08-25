from sympy import symbols, Function, Eq, solve, lambdify, pretty
from scipy.interpolate import interp1d
from numpy import linspace


def fredholm_f(a, b, n, l_, k, f_):
    l, x, s = symbols('l x s')
    y = symbols(f'y0:{n + 1}')
    f = Function('f')(x)

    k = eval(k)
    f_ = eval(f_)

    data = linspace(a, b, n + 1)

    sim1 = sum(k.subs({s: data[i]}) * y[i] for i in range(1, n) if i % 2 != 0)
    sim2 = sum(k.subs({s: data[i]}) * y[i] for i in range(1, n) if i % 2 == 0)

    simpson = ((b - a) / (3 * n)) * (k.subs({s: data[0]}) * y[0] + 4 * sim1 +
                                     2 * sim2 + k.subs({s: data[-1]}) * y[-1])

    fredholm_s = [Eq(f, y[i] - l * simpson).subs({l: l_, f: f_, x: data[i]}) for i in range(len(y))]

    y_ = solve(fredholm_s, y)
    out = l * simpson + f_
    out = out.subs(l, l_).subs(y_)
    fun = lambdify(x, out, 'numpy')
    x_ = linspace(a, b, 200)

    out = Eq(Function('y')(x), out.subs(l, l_).subs(y_))
    return (data, list(y_.values()), x_, fun(x_), '\n\n'.join([pretty(i).replace('\n', '') for i in fredholm_s]),
            '\n'.join([f'{i[0]}: {i[1]}' for i in list(y_.items())]), pretty(out))


def volterre_f(a, b, n, l_, k, f_):
    l, x, s = symbols('l x s')
    y = symbols(f'y0:{n + 1}')
    f = Function('f')(x)

    k = eval(k)
    f_ = eval(f_)

    data = linspace(a, b, n + 1)

    fredholm_s = []
    for i in range(len(data)):
        sim1, sim2, sim3 = 0, 0, 0
        for j in range(len(data)):
            if 0 < j < len(data) - 1:
                if j % 2 != 0:
                    if j <= i:
                        sim1 = sim1 + k.subs({s: data[j]}) * y[j]
                else:
                    if j <= i:
                        sim2 = sim2 + k.subs({s: data[j]}) * y[j]
        if i >= len(data) - 1:
            sim3 = k.subs({s: data[-1]}) * y[-1]
        simpson = ((b - a) / (3 * n)) * (k.subs({s: data[0]}) * y[0] + 4 * sim1 +
                                         2 * sim2 + sim3)
        fredholm = Eq(f, y[i] - l * simpson).subs({l: l_, f: f_, x: data[i]})
        fredholm_s.append(fredholm)

    y_ = solve(fredholm_s, y)

    x_ = linspace(a, b, 200)
    fun = interp1d(data, list(y_.values()), kind='quadratic')(x_)
    return (data, list(y_.values()), x_, fun, '\n\n'.join([pretty(i).replace('\n', '') for i in fredholm_s]),
            '\n'.join([f'{i[0]}: {i[1]}' for i in list(y_.items())]), '')
