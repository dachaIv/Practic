import sympy as sp
from sympy.printing.latex import latex
import webbrowser

def get_user_input():
    # Ввод количества уравнений
    n = int(input("Введите количество дифференциальных уравнений: "))

    # Определение символов
    t = sp.symbols('t')
    x = sp.symbols(f'x1:{n + 1}', real=True)
    u = sp.symbols('u', real=True)
    T = sp.symbols('T', real=True)
    beta, a = sp.symbols('beta a', real=True)
    h = sp.symbols('h', real=True)  # Шаг интегрирования

    local_dict = {f'x{i + 1}': x[i] for i in range(n)}
    local_dict.update({'u': u, 'T': T, 'beta': beta, 'a': a, 'abs': sp.Abs})

    # Ввод правых частей уравнений
    x_dot = []
    for i in range(n):
        eq_str = input(f"Введите правую часть уравнения для x{i + 1} : ")
        x_dot.append(sp.sympify(eq_str, locals=local_dict))

    # Ввод функции Psi
    psi_str = input("Введите функцию Psi : ")
    psi = sp.sympify(psi_str, locals=local_dict)

    # Вычисление производной Psi
    # Убираем sign из производной
    psi_dot = sum(sp.diff(psi, x[i]) * x_dot[i] for i in range(n)).subs({sp.sign(xi): sp.Abs(xi)/xi for xi in x})

    # Уравнение управления
    res = sp.Eq(T * psi_dot + psi, 0)

    # Решение уравнения для u
    solutions = sp.solve(res, u)

    # Если решение есть, упрощаем
    if solutions:
        final_solution = sp.simplify(solutions[0])
    else:
        print("Решение не найдено.")
        return

    # Применение одношагового метода (Метод Эйлера)
    x_next = []
    for i in range(n):
        x_next.append(x[i] + h * x_dot[i])

    x_next_latex = [latex(sp.simplify(expr)) for expr in x_next]

    # Форматирование в LaTeX
    psi_latex = latex(psi)
    psi_dot_latex = latex(psi_dot)
    res_latex = latex(res)
    u_solution_latex = latex(final_solution)

    # Генерация HTML-отчета
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Отчет о решении</title>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    </head>
    <body>
        <h1>Отчет о решении</h1>
        <h2>Входные дифференциальные уравнения</h2>
    """
    for i in range(n):
        x_dot_latex = latex(x_dot[i])
        html_content += f"<p>\\( \\dot{{x}}_{i + 1} = {x_dot_latex} \\)</p>\n"
    html_content += f"""
        <h2>Функция Psi</h2>
        <p>\\( \\psi = {psi_latex} \\)</p>

        <h2>Производная Psi</h2>
        <p>\\( \\dot{{\\psi}} = {psi_dot_latex} \\)</p>
        <h2>Уравнение</h2>
        <p>\\( {res_latex} \\)</p>
        <h2>Решение для u</h2>
        <p>\\( u = {u_solution_latex} \\)</p>
    """


    html_content += """
    </body>
    </html>
    """

    # Запись HTML-контента в файл
    with open("solution.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("Решение записано в файл solution.html")

    # Открываем файл в браузере
    webbrowser.open("solution.html")

get_user_input()
