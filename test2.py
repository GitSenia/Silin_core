from lcapy import Circuit
from sympy import symbols, pprint

circuit = Circuit("""
R1 0 1;up
L 1 2;up
W 2 4 ;right
R2 4 5;down
R4 1 5;right
SW 5 6 no 0;right
R3 6 7;up
W 6 8;down
W 8 9;left
C 9 0;left
V1 4 7;right
""")

print("Converting circuit to IVP")


cct_ivp = circuit.convert_IVP(0)
circuit.draw(node_spacing=6)
print(cct_ivp)