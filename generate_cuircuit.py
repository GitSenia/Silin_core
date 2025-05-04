from lcapy import Circuit
import random

def check_basic_validity(circuit):
    for e in circuit.elements.values():
        if len(e.nodes) == 2 and e.nodes[0] != e.nodes[1]:
            return True
    return False

def generate_circuit():
    template = """
        W 1 2;up
        W 2 3;up
        W 3 4;right
        W 4 5;right
        W 5 6;down
        W 6 7;down
        W 7 8;left
        W 8 1;left
        W 4 9;down
        W 9 8;down
    """

    template_lines = template.strip().split("\n")
    w_line_indices = [i for i, line in enumerate(template_lines) if line.strip().startswith("W")]

    while True:
        components = ['R1', 'R2', 'R3', 'V1', 'C1', 'SW']
        selected_indices = random.sample(w_line_indices, len(components))  # случайные строки для замены

        new_lines = []
        for i, line in enumerate(template_lines):
            if i in selected_indices:
                comp = components.pop()
                new_line = line.replace('W', comp, 1)
                new_lines.append(new_line)
            else:
                new_lines.append(line)

        new_template_str = "\n".join(new_lines)
        c = Circuit(new_template_str)

        if check_basic_validity(c):
            return c

# Пример использования
cct = generate_circuit()
cct.draw(node_spacing=6)
