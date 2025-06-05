import copy

from lcapy import Circuit
import config
import random
from sympy import pprint, init_printing, symbols
t = symbols('t', real=True)

def get_random_circuit(order):
    if order == 1:
        circuits = copy.deepcopy(config.circuit_test)
    elif order == 2:
        circuits = copy.deepcopy(config.circuit_test)
    else:
        raise ValueError("Порядок цепи должен быть 1 или 2")

    if not circuits:
        raise ValueError(f"В config нет схем для порядка {order}")

    return random.choice(circuits)



def assign_components(order):
    elements = get_random_circuit(order)
    resistor_counter = 1

    def next_resistor_name():
        nonlocal resistor_counter
        name = f"R{resistor_counter}"
        resistor_counter += 1
        return name

    # --- Этап 1: установка ключа SW ---
    indices = list(range(len(elements)))
    random.shuffle(indices)

    sw_set = False
    for i in indices:
        el = elements[i]
        if el['type'] == 'W' and el['tag'] in ['F0', 'F1','F2']:
            el['type'] = 'SW'
            el['name'] = 'SW'
            if el['tag'] == 'F0':
                el['value'] = 0
            elif el['tag'] == 'F1':
                el['value'] = 1
            elif el['tag'] == 'F2':
                el['value'] = random.randint(0, 1)
            el['tag'] = None
            sw_set = True
            break

    if not sw_set:
        raise ValueError("Не найден элемент с tag=F0 или F1 для установки ключа SW")

    # --- Этап 2: подсчёт уже установленных реактивных компонентов ---
    def count_reactives():
        has_C = any(el['type'] == 'C' for el in elements)
        has_L = any(el['type'] == 'L' for el in elements)
        return has_C, has_L

    has_C, has_L = count_reactives()

    # --- Этап 3: установка нужных реактивных компонентов ---
    required_reactives = []
    if order == 2:
        if not has_C:
            required_reactives.append('C')
        if not has_L:
            required_reactives.append('L')
    elif order == 1:
        if not has_C and not has_L:
            required_reactives.append(random.choice(['C', 'L']))

    random.shuffle(indices)
    for comp in required_reactives:
        for i in indices:
            el = elements[i]
            if el['type'] == 'W' and el.get('tag') in ['L', 'F0', 'F1','F2']:
                el['type'] = comp
                el['name'] = comp
                el['value'] = 0
                el['tag'] = None
                break  # ставим только один элемент этого типа

    # --- Этап 4: установка резисторов и случайные замены ---
    for i in indices:
        el = elements[i]

        if el['type'] != 'W':
            continue

        tag = el.get('tag')

        # уже учтены C и L выше
        if tag == 'B':
            el['type'] = 'R'
            el['name'] = next_resistor_name()
            el['value'] = 0
            el['tag'] = None

        elif tag == 'L':
            if el['name'] in ['C', 'L']:
                continue
            if random.random() < 0.2:
                el['type'] = 'R'
                el['name'] = next_resistor_name()
                el['value'] = 0
                el['tag'] = None

        elif tag in ['F0', 'F1']:
            if el['name'] in ['C', 'L']:
                continue  # сюда мог попасть реактивный, если остался второй F0/F1


    return elements



def render_circuit(elements):
    lines = []
    for el in elements:
        name = el['name']
        start = el['start']
        end = el['end']
        direction = el.get('direction')
        value = el.get('value')


        # Строим строку
        line = f"{name} {start} {end} "
        if name == 'SW':
            if value==1:
                line += " no 0"
            else:
                line += " nc 0"
        if direction:
            if isinstance(value, (int, float)) and value != 0:
                line += f";{direction}={value}"
            else:
                line += f";{direction}"
        lines.append(line)
    return "\n".join(lines)

assigned = assign_components( order=1)
t=render_circuit(assigned)
print(t)
cct=Circuit(t)
cct.draw(node_spacing=6)
cct_ivp = cct.convert_IVP(0)
ss = cct_ivp.ss
print(ss)
for el in assigned:
    print(el)



