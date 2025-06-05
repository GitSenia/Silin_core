import random



def get_random_circuit(order=1):
    # Проверка допустимого порядка
    if order not in [1, 2]:
        raise ValueError("order должен быть 1 или 2")

    # Индекс класса: 0 для order=1, 1 для order=2
    class_index = order - 1

    # Получаем доступный список схем из нужного класса
    class_circuits = circuit1[class_index]

    # Фильтруем пустые схемы
    available_circuits = [s for s in class_circuits if s and s[0].strip()]

    if not available_circuits:
        raise ValueError(f"Нет схем для order={order}")

    # Выбираем случайную схему из выбранного класса
    chosen_scheme = random.choice(available_circuits)[0]

    return chosen_scheme
