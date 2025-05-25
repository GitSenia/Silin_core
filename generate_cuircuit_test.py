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

    template_lines = template.strip().splitlines()

    # Подготовка списков компонентов
    reactive_pool = []
    if 'C1' not in template:
        reactive_pool.append('C1')
    if 'L1' not in template:
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

    # Сначала обрабатываем участок 5 6 — строго C1 или R
    allowed_for_5_6 = [c for c in all_components if c == 'C1' or c.startswith('R')]
    if not allowed_for_5_6:
        return generate_circuit(order)  # перегенерация, если нет подходящих компонентов

    comp_5_6 = random.choice(allowed_for_5_6)
    all_components.remove(comp_5_6)

    # Заменяем строку с 5 6
    for i, line in enumerate(template_lines):
        if "5 6" in line:
            template_lines[i] = line.replace("W", comp_5_6, 1)
            break

    # Остальные обязательные пары
    priority_pairs = ["0 1", "1 2", "2 3", "7 0"]
    chosen_priority = random.choice(priority_pairs)
    ending_pairs = ["3 8", "8 7"]
    chosen_ending = random.choice(ending_pairs)

    must_replace_pairs = [chosen_priority, chosen_ending]

    def find_line_index(pair):
        return next((i for i, line in enumerate(template_lines) if pair in line), None)

    must_indices = set(find_line_index(pair) for pair in must_replace_pairs if find_line_index(pair) is not None)

    # Допустимые строки для случайной замены (исключая 6 10 и уже заменённую 5 6)
    used_indices = must_indices | {i for i, line in enumerate(template_lines) if "5 6" in line or "6 10" in line}
    w_line_indices = [
        i for i, line in enumerate(template_lines)
        if line.strip().startswith("W") and i not in used_indices
    ]

    remaining_needed = len(all_components) - len(must_indices)
    if remaining_needed > len(w_line_indices):
        return generate_circuit(order)

    selected_random = random.sample(w_line_indices, remaining_needed)
    selected_indices = list(must_indices) + selected_random

    # Заменяем остальные строки
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
cct = generate_circuit(order=2)
cct.draw(node_spacing=6)
print(cct)