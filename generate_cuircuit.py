from lcapy import Circuit
import random

def check_basic_validity(circuit):
    for e in circuit.elements.values():
        if len(e.nodes) == 2 and e.nodes[0] != e.nodes[1]:
            return True
    return False

def generate_circuit(order=1):
    if order not in (1, 2):
        raise ValueError("Order must be 1 or 2")

    template = """
        W 0 1;up
        W 1 2;up
        W 2 3;right
        W 3 4;right
        W 4 5;down
        W 5 6;down
        W 6 7;left
        W 7 0;left
        W 3 8;down
        W 8 7;down
        SW 5 9 nc 0;right=0.4
        W 6 10;right=0.4
        V1 9 10;down=0.4
    """

    used = set(line.strip().split()[0] for line in template.strip().splitlines())
    reactive_pool = []

    if 'C1' not in used:
        reactive_pool.append('C1')
    if 'L1' not in used:
        reactive_pool.append('L1')

    if order == 1:
        target_reactives = random.sample(reactive_pool, 1)
    else:
        if len(reactive_pool) < 2:
            raise ValueError("Not enough unique reactive components available for second-order circuit.")
        target_reactives = ['C1', 'L1']

    other_components = ['R1', 'R2', 'R3']
    all_components = target_reactives + other_components
    random.shuffle(all_components)

    template_lines = template.strip().splitlines()

    # 1. Приоритетные пары (выбрать одну)
    priority_pairs = ["0 1", "1 2", "2 3", "7 0"]
    chosen_priority = random.choice(priority_pairs)

    # 2. Обязательная пара
    always_pairs = ["5 6"]

    # 3. Один из концов цепи
    ending_pairs = ["3 8", "8 7"]
    chosen_ending = random.choice(ending_pairs)

    # Список пар для обязательной замены
    must_replace_pairs = [chosen_priority, *always_pairs, chosen_ending]

    def find_line_index(pair):
        return next((i for i, line in enumerate(template_lines) if pair in line), None)

    must_indices = set(find_line_index(pair) for pair in must_replace_pairs if find_line_index(pair) is not None)

    if len(must_indices) > len(all_components):
        raise ValueError("Not enough components for required placements.")

    # Допустимые строки для случайной замены (кроме W 6 10)
    w_line_indices = [
        i for i, line in enumerate(template_lines)
        if line.strip().startswith("W")
        and "6 10" not in line
        and i not in must_indices
    ]

    remaining_needed = len(all_components) - len(must_indices)
    selected_random = random.sample(w_line_indices, remaining_needed)
    selected_indices = list(must_indices) + selected_random

    # Заменяем выбранные строки
    new_lines = []
    for i, line in enumerate(template_lines):
        if i in selected_indices:
            comp = all_components.pop()
            new_line = line.replace("W", comp, 1)
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    new_template_str = "\n".join(new_lines)
    circuit = Circuit(new_template_str)

    if not check_basic_validity(circuit):
        return generate_circuit(order)

    return circuit

# Генерация схемы
cct = generate_circuit(order=1)
cct.draw(node_spacing=6)
