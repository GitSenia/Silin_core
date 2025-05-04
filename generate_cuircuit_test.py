from lcapy import Circuit
import random


def check_basic_validity(circuit):
    for e in circuit.elements.values():
        if len(e.nodes) == 2 and e.nodes[0] != e.nodes[1]:
            return True
    return False


def has_transient_conditions(circuit):
    elements = circuit.elements
    has_source = any(e.name.startswith(('V', 'I')) for e in elements.values())
    has_storage = any(e.name.startswith(('C', 'L')) for e in elements.values())
    has_switch = any(e.name.startswith('SW') for e in elements.values())
    return has_source and has_storage and has_switch


def has_short_circuit(circuit):
    try:
        # Упростим схему
        circuit = circuit.simplify()

        # Получим список всех уникальных узлов (кроме заземления "0")
        nodes = [n for e in circuit.elements.values() for n in e.nodes]
        nodes = list(set(n for n in nodes if n != '0'))

        # Получим потенциалы всех узлов
        potentials = [circuit.V(n).expr.simplify() for n in nodes]

        # Если все потенциалы одинаковые, это подозрение на КЗ
        return all(p == potentials[0] for p in potentials)
    except Exception:
        # Если не удалось рассчитать (например, из-за КЗ) — считаем, что КЗ есть
        return True


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
        selected_indices = random.sample(w_line_indices, len(components))

        new_lines = template_lines.copy()
        for idx, comp in zip(selected_indices, components):
            new_lines[idx] = new_lines[idx].replace('W', comp, 1)

        new_template_str = "\n".join(new_lines)
        c = Circuit(new_template_str)

        if check_basic_validity(c) and has_transient_conditions(c) and not has_short_circuit(c):
            return c


# Пример использования
cct = generate_circuit()
cct.draw(node_spacing=6)
