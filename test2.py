from lcapy import Circuit
from sympy import symbols, pprint

# Создание схемы
cct = Circuit("""
V1 0 6 10; down
R1 0 1 100; right
SW 8 1 2; up
R2 2 3 200; right
""")

# Отрисовка схемы
cct.draw()
