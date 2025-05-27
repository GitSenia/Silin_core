from lcapy import Circuit, s
import sympy


def calculate_characteristic_poly(circuit: Circuit):
    """
    Вычисляет характеристический полином для заданной цепи.

    Аргументы:
        circuit (Circuit): Объект цепи lcapy.

    Возвращает:
        tuple: Кортеж, содержащий:
               - characteristic_poly (lcapy Expression): Символьное характеристическое уравнение.
               - roots (list): Список sympy выражений для корней.
               - discriminant (sympy Expression): Символьное выражение для дискриминанта (b^2 - 4ac).
                 Возвращает None, если полином не квадратный.
    """
    ss = circuit.ss

    characteristic_poly = ss.P
    roots = ss.eigenvalues

    # Убедимся, что roots - это список
    if not isinstance(roots, list):
        try:
            roots = list(roots)
        except TypeError:
            if hasattr(roots, 'keys'):
                roots = list(roots.keys())
            else:
                roots = [roots]

    # Вычисляем дискриминант
    discriminant = None
    try:
        # Получаем числитель полинома как выражение sympy
        poly_expr = characteristic_poly.expr
        numerator, _ = sympy.fraction(sympy.simplify(poly_expr))

        # Создаем объект полинома sympy от переменной 's'
        poly = sympy.Poly(numerator, s)

        coeffs = poly.all_coeffs()

        if len(coeffs) == 3:
            a, b, c = coeffs
            discriminant = sympy.simplify(b ** 2 - 4 * a * c)
        elif len(coeffs) == 2:  # Случай ax^2 + c
            a, c = coeffs
            b = 0
            discriminant = sympy.simplify(b ** 2 - 4 * a * c)
        elif len(coeffs) == 1:  # Случай ax^2
            a = coeffs[0]
            b = 0
            c = 0
            discriminant = sympy.simplify(b ** 2 - 4 * a * c)

    except (sympy.PolynomialError, AttributeError) as e:
        print(f"Предупреждение: Не удалось вычислить дискриминант ({e})")
        pass

    return characteristic_poly, roots, discriminant


cct = Circuit("""
L 0 1;up
V1 1 2;up
R2 2 4;right
C 4 5;down
R3 1 5;right
W 5 6;right
R1 6 7;up
W 6 8;down
SW 8 9 nc 0;left=1
R4 9 0;left
R5 4 7;right
        """)

print("Converting circuit to IVP")

cct_ivp = cct.convert_IVP(0)
calculate_characteristic_poly(cct_ivp)
print(cct_ivp)