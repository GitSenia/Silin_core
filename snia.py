from lcapy import *
from sympy import pprint, symbols, pi, sin, expand_trig

t = symbols('t', real=True)

cct = Circuit(f"""
V1 1 2 {{-8*sin(w0 + pi/2)}}; up
R1 0 1 2; up
SW 2 3 no 0; right
C1 3 5 1e-6; down
W 5 0; left
W 3 4; right
R2 4 6 4; down
W 6 5; left
""")

cct_ivp = cct.convert_IVP(0)
IR1 = cct_ivp.R1.i(t)

pprint(expand_trig(IR1), use_unicode=True)
cct.draw(node_spacing=6)
