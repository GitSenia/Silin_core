from lcapy import Circuit
from sympy import pprint, init_printing, symbols
t = symbols('t', real=True)
cct = Circuit("""


V 0 1 ;right
W 1 2 ;down
L 2 3 ;down
W 3 9 ;left
R3 9 4 ;left
W 4 5 ;up
C 5 6 ;up
W 6 0 ;up
SW 5 8  no 0;right=1
R2 8 7 ;up
R1 6 7 ;right
W 7 2 ;right


        """)


# Получаем ток через R1


# Красиво печатаем

cct.draw(node_spacing=6)

