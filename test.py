import tkinter as tk
from tkinter import simpledialog, messagebox
import math
import json

class ComponentValueInput:
    def __init__(self, master, components, callback):
        self.master = master
        self.components = components
        self.callback = callback
        self.entries = {}
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.master, text="Введите значения компонентов:", font=("Arial", 12, "bold")).pack(pady=10)
        form_frame = tk.Frame(self.master)
        form_frame.pack()

        for i, comp in enumerate(self.components):
            tk.Label(form_frame, text=comp).grid(row=i, column=0, padx=5, pady=2, sticky="e")
            entry = tk.Entry(form_frame, width=15)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[comp] = entry

        submit_btn = tk.Button(self.master, text="Готово", command=self.submit)
        submit_btn.pack(pady=10)

    def submit(self):
        values = {comp: entry.get() for comp, entry in self.entries.items()}
        self.master.destroy()
        self.callback(values)


class CircuitMatrix:
    def __init__(self, master, components, values):
        self.master = master
        self.components = components
        self.values = values
        self.size = len(self.components)
        self.grid_data = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.connections = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.create_matrix()
        self.create_export_button()

    def create_matrix(self):
        for i in range(self.size):
            label_top = tk.Label(self.master, text=self.components[i], font=("Arial", 10), justify="center")
            label_top.grid(row=0, column=i+1, padx=2, pady=2)

            label_side = tk.Label(self.master, text=self.components[i], font=("Arial", 10), justify="left")
            label_side.grid(row=i+1, column=0, padx=2, pady=2)

        for row in range(self.size):
            for col in range(self.size):
                btn = tk.Button(self.master, width=4, height=2,
                                command=lambda r=row, c=col: self.toggle_connection(r, c))
                btn.grid(row=row+1, column=col+1, padx=1, pady=1)
                self.grid_data[row][col] = btn

    def toggle_connection(self, row, col):
        btn = self.grid_data[row][col]
        current_color = btn.cget("bg")
        new_color = "green" if current_color in ("SystemButtonFace", "lightgray") else "lightgray"
        btn.config(bg=new_color)
        self.connections[row][col] = 1 if new_color == "green" else 0

    def create_export_button(self):
        export_btn = tk.Button(self.master, text="Экспортировать в JSON", command=self.export_to_json)
        export_btn.grid(row=self.size + 2, column=0, columnspan=self.size + 1, pady=10)

    def export_to_json(self):
        json_data = []
        for i, comp in enumerate(self.components):
            row_data = {
                "name": comp,
                "value": self.values.get(comp, ""),
                "connections": self.connections[i]
            }
            json_data.append(row_data)

        json_string = json.dumps(json_data, indent=4, ensure_ascii=False)

        # Показать в новом окне
        top = tk.Toplevel(self.master)
        top.title("JSON вывод")
        text = tk.Text(top, wrap="word")
        text.insert("1.0", json_string)
        text.pack(expand=True, fill="both")


def get_component_counts():
    root = tk.Tk()
    root.withdraw()

    try:
        r = simpledialog.askinteger("Резисторы", "Сколько резисторов (R)?", minvalue=0, maxvalue=99)
        c = simpledialog.askinteger("Конденсаторы", "Сколько конденсаторов (C)?", minvalue=0, maxvalue=99)
        l = simpledialog.askinteger("Индуктивности", "Сколько индуктивностей (L)?", minvalue=0, maxvalue=99)
        i = simpledialog.askinteger("Источники тока", "Сколько источников тока (I)?", minvalue=0, maxvalue=99)
        v = simpledialog.askinteger("Источники напряжения", "Сколько источников напряжения (V)?", minvalue=0, maxvalue=99)

        if any(val is None for val in [r, c, l, i, v]):
            return None

        return {"R": r, "C": c, "L": l, "I": i, "V": v}

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные значения")
        return None


def generate_component_list(components):
    result = []
    for prefix, count in components.items():
        for i in range(1, count + 1):
            result.append(f"{prefix}{i}")
    return result


def start_matrix_window(components, values):
    root = tk.Tk()
    root.title("Матрица соединений компонентов")
    app = CircuitMatrix(root, components, values)
    root.mainloop()


if __name__ == "__main__":
    component_counts = get_component_counts()
    if component_counts:
        components = generate_component_list(component_counts)

        value_window = tk.Tk()
        value_window.title("Значения компонентов")
        ComponentValueInput(value_window, components, lambda values: start_matrix_window(components, values))
        value_window.mainloop()