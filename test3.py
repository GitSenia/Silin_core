from lcapy import Circuit
from sympy import pprint, init_printing, symbols
t = symbols('t', real=True)
cct = Circuit("""
V 0 1 12;up
R1 1 2 1e3; right
C 2 4 1e-9; down
R2 4 5 500;down 
W 5 0;left
W 2 6;right
W 5 8;right
SW 6 7  nc 0; down
R3 7 8 500;down

; 
""")
cct_ivp = cct.convert_IVP(0)

# Получаем ток через R1
vC = cct_ivp.C.v(t)

# Красиво печатаем
pprint(vC, use_unicode=True)
cct.draw(node_spacing=6)

