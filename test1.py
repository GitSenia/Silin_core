from lcapy import Circuit
import matplotlib.pyplot as plt

# Описываем схему по условию
cct = Circuit("""
V 1 0 12; right
R1 1 2 1e3; right
W 2 3; down
C 2 4 1e-9; down
R2 4 0 500; down
SW 3 5 nc 0; right
R3 5 0 500; down
; draw_nodes=connections
""")

cct_ivp = cct.convert_IVP(0)

