import random
from lcapy import *
import copy
from sympy import pprint, init_printing, symbols
t = symbols('t', real=True)
circuit = [
    {'type': 'W', 'name': 'W', 'start': '0', 'end': '1', 'value': 0, 'direction': 'up', 'tag': 'F2'},
    {'type': 'W', 'name': 'W', 'start': '1', 'end': '2', 'value': 0, 'direction': 'up', 'tag': 'B'},
    {'type': 'W', 'name': 'W', 'start': '2', 'end': '4', 'value': 0, 'direction': 'right', 'tag': 'F2'},
    {'type': 'W', 'name': 'W', 'start': '4', 'end': '5', 'value': 0, 'direction': 'down', 'tag': 'B'},
    {'type': 'W', 'name': 'W', 'start': '1', 'end': '5', 'value': 0, 'direction': 'right', 'tag': 'F2'},
    {'type': 'W', 'name': 'W', 'start': '5', 'end': '6', 'value': 0, 'direction': 'right', 'tag': None},
    {'type': 'W', 'name': 'W', 'start': '6', 'end': '7', 'value': 0, 'direction': 'up', 'tag': 'B'},
    {'type': 'W', 'name': 'W', 'start': '6', 'end': '8', 'value': 0, 'direction': 'down', 'tag': None},
    {'type': 'W', 'name': 'W', 'start': '8', 'end': '9', 'value': 0, 'direction': 'left', 'tag': 'B'},
    {'type': 'W', 'name': 'W', 'start': '9', 'end': '0', 'value': 0, 'direction': 'left', 'tag': 'F2'},
    {'type': 'V', 'name': 'V1', 'start': '4', 'end': '7', 'value': 0, 'direction': 'right', 'tag': None},

]


def assign_components(order):
    elements = copy.deepcopy(circuit)
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
        line = f"{name} {start} {end}"
        if name == 'SW':
            if value==1:
                line += " no 0"
            else:
                line += " nc 0"
        if direction:
            line += f";{direction}"
        lines.append(line)
    return "\n".join(lines)




if __name__ == "__main__":
  errors = 0
  for i in range(100):
    try:
      elements = assign_components(order=2)
      circuit_str = render_circuit(elements)
      cct = Circuit(circuit_str)
      cct_ivp = cct.convert_IVP(0)
      ss = cct_ivp.ss

      print(f"Circuit {i} - valid")
    except Exception as e:
      errors += 1
      print("-----------------------------------")
      print(f"Circuit {i} - ERROR\n{e}")
      print("----------Circuit------------------")
      print(circuit_str)
      cct = Circuit(circuit_str)
      cct.draw(node_spacing=6)
      print("-----------------------------------")



  print(f"Errors: {errors}")
