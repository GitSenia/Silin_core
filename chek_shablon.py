from lcapy import Circuit
from sympy import pprint, init_printing, symbols
t = symbols('t', real=True)
cct = Circuit("""

V1 0 1;up
R1 1 2;right
R2 2 6;down
W 6 3;down
W 3 4;right
SW 4 5 nc 0;up
L 2 5;right
W 3 0;left

        """)


# Получаем ток через R1


# Красиво печатаем

cct.draw(node_spacing=6)
