# -*- coding: utf-8 -*-
"""
Simulador interactivo de calorimetría
Interfaz educativa con visualización del equilibrio térmico.
Requiere: matplotlib (pip install matplotlib)
"""

import tkinter as tk
from tkinter import ttk, messagebox

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    Figure = None
    FigureCanvasTkAgg = None


# ----------------------------- PALETA ---------------------------------
BG = "#F3F6FB"
CARD = "#FFFFFF"
NAVY = "#172554"
NAVY_2 = "#1E3A5F"
BLUE = "#3B82F6"
TEAL = "#0F9D8A"
CORAL = "#F9736B"
GOLD = "#F4B942"
TEXT = "#243047"
MUTED = "#68758A"
BORDER = "#DCE4EF"
SOFT_BLUE = "#E8F1FF"
SOFT_TEAL = "#E2F7F2"
SOFT_CORAL = "#FFF0ED"


def parse_number(entry, label):
    raw = entry.get().strip().replace(",", ".")
    if not raw:
        raise ValueError(f"Completa el campo: {label}.")
    try:
        return float(raw)
    except ValueError:
        raise ValueError(f"El valor de «{label}» debe ser numérico.")


class CalorimetriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TermoLab | Simulador de calorimetría")
        self.root.geometry("1180x820")
        self.root.minsize(980, 700)
        self.root.configure(bg=BG)

        self.last_result = None
        self._setup_styles()
        self._build_header()
        self._build_layout()
        self._set_defaults()
        self.root.bind("<Return>", lambda _event: self.calculate())
        self.calculate()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox", padding=7, fieldbackground="#FFFFFF",
            background="#FFFFFF", foreground=TEXT, arrowcolor=NAVY
        )

    def _build_header(self):
        header = tk.Frame(self.root, bg=NAVY, height=118)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=NAVY)
        left.pack(side="left", fill="both", expand=True, padx=30, pady=18)

        tk.Label(
            left, text="TERMOLAB  /  LABORATORIO VIRTUAL",
            bg=NAVY, fg="#8DE2D2", font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")
        tk.Label(
            left, text="Explora el equilibrio térmico",
            bg=NAVY, fg="#FFFFFF", font=("Segoe UI", 23, "bold")
        ).pack(anchor="w", pady=(4, 1))
        tk.Label(
            left, text="Cambia los datos, observa el intercambio de energía y entiende el resultado.",
            bg=NAVY, fg="#D4DEEF", font=("Segoe UI", 10)
        ).pack(anchor="w")

        badge = tk.Label(
            header, text="c agua = 4186 J/(kg·°C)",
            bg="#25416F", fg="#FFFFFF", font=("Segoe UI", 10, "bold"),
            padx=15, pady=10
        )
        badge.pack(side="right", padx=30)

    def _build_layout(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=24, pady=20)

        main.grid_columnconfigure(0, weight=0, minsize=330)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        self.left_panel = tk.Frame(main, bg=BG, width=330)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        self.left_panel.grid_propagate(False)

        self.right_panel = tk.Frame(main, bg=BG)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self._build_inputs()
        self._build_result_cards()
        self._build_visualization()
        self._build_explanation()

    def _card(self, parent, title, subtitle=None):
        outer = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        top = tk.Frame(outer, bg=CARD)
        top.pack(fill="x", padx=18, pady=(16, 8))
        tk.Label(top, text=title, bg=CARD, fg=NAVY, font=("Segoe UI", 12, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(
                top, text=subtitle, bg=CARD, fg=MUTED,
                font=("Segoe UI", 9), wraplength=285, justify="left"
            ).pack(anchor="w", pady=(3, 0))
        return outer

    def _build_inputs(self):
        card = self._card(
            self.left_panel, "Configura el experimento",
            "Usa las masas y temperaturas de tu práctica. El agua mantiene su calor específico fijo."
        )
        card.pack(fill="x")

        form = tk.Frame(card, bg=CARD)
        form.pack(fill="x", padx=18, pady=(0, 10))
        self.entries = {}

        fields = [
            ("mw", "Masa del agua", "g", "100"),
            ("mx", "Masa de la muestra", "g", "150"),
            ("tw", "Temperatura inicial del agua", "°C", "22"),
            ("tx", "Temperatura inicial de la muestra", "°C", "80"),
            ("tf", "Temperatura final de equilibrio", "°C", "35"),
        ]

        for row, (key, label, unit, default) in enumerate(fields):
            tk.Label(
                form, text=label, bg=CARD, fg=TEXT,
                font=("Segoe UI", 9, "bold")
            ).grid(row=row * 2, column=0, sticky="w", pady=(8, 3))
            line = tk.Frame(form, bg=CARD)
            line.grid(row=row * 2 + 1, column=0, sticky="ew")
            line.grid_columnconfigure(0, weight=1)
            entry = tk.Entry(
                line, bg="#F8FAFD", fg=TEXT, insertbackground=TEXT,
                relief="flat", highlightthickness=1, highlightbackground=BORDER,
                highlightcolor=BLUE, font=("Segoe UI", 11), width=16
            )
            entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
            tk.Label(
                line, text=unit, bg=SOFT_BLUE, fg=NAVY_2,
                font=("Segoe UI", 9, "bold"), padx=9, pady=7
            ).pack(side="right")
            self.entries[key] = entry

        tk.Label(
            form, text="Calor específico del agua", bg=CARD, fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).grid(row=10, column=0, sticky="w", pady=(12, 4))
        tk.Label(
            form, text="4186 J/(kg·°C)  ·  valor fijo",
            bg=SOFT_TEAL, fg="#087565", font=("Segoe UI", 10, "bold"),
            padx=10, pady=9, anchor="w"
        ).grid(row=11, column=0, sticky="ew")

        buttons = tk.Frame(card, bg=CARD)
        buttons.pack(fill="x", padx=18, pady=(10, 18))
        tk.Button(
            buttons, text="▶  SIMULAR", command=self.calculate,
            bg=TEAL, fg="white", activebackground="#0B8475",
            activeforeground="white", relief="flat", cursor="hand2",
            font=("Segoe UI", 10, "bold"), padx=12, pady=11
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Button(
            buttons, text="↺  Reiniciar", command=self.reset,
            bg="#E9EEF6", fg=NAVY, activebackground="#DCE5F1",
            relief="flat", cursor="hand2", font=("Segoe UI", 10, "bold"),
            padx=12, pady=11
        ).pack(side="left", fill="x", expand=True, padx=(6, 0))

        note = tk.Frame(self.left_panel, bg=SOFT_BLUE)
        note.pack(fill="x", pady=(14, 0))
        tk.Label(
            note, text="IDEA CLAVE", bg=SOFT_BLUE, fg=BLUE,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=15, pady=(12, 3))
        tk.Label(
            note,
            text="El calor que pierde el cuerpo caliente es, idealmente, igual al que gana el cuerpo frío.",
            bg=SOFT_BLUE, fg=NAVY_2, font=("Segoe UI", 10),
            wraplength=285, justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 12))

    def _build_result_cards(self):
        self.metrics = tk.Frame(self.right_panel, bg=BG)
        self.metrics.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        for col in range(3):
            self.metrics.grid_columnconfigure(col, weight=1)

        self.metric_values = {}
        specs = [
            ("cx", "CALOR ESPECÍFICO DE LA MUESTRA", "—", BLUE, SOFT_BLUE),
            ("qwater", "CALOR DEL AGUA", "—", TEAL, SOFT_TEAL),
            ("status", "LECTURA DEL EXPERIMENTO", "En espera", CORAL, SOFT_CORAL),
        ]
        for col, (key, title, initial, accent, soft) in enumerate(specs):
            box = tk.Frame(self.metrics, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
            box.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 6, 0 if col == 2 else 6))
            tk.Frame(box, bg=accent, height=4).pack(fill="x")
            tk.Label(
                box, text=title, bg=CARD, fg=MUTED,
                font=("Segoe UI", 8, "bold"), wraplength=190, justify="left"
            ).pack(anchor="w", padx=13, pady=(12, 5))
            value = tk.Label(
                box, text=initial, bg=CARD, fg=accent,
                font=("Segoe UI", 15 if key != "status" else 11, "bold"),
                wraplength=190, justify="left"
            )
            value.pack(anchor="w", padx=13, pady=(0, 13))
            self.metric_values[key] = value

    def _build_visualization(self):
        card = self._card(
            self.right_panel, "Dentro del calorímetro",
            "El gráfico compara las temperaturas iniciales y la temperatura final que ingresaste."
        )
        card.grid(row=1, column=0, sticky="nsew")
        self.chart_area = tk.Frame(card, bg=CARD)
        self.chart_area.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        if Figure is None:
            tk.Label(
                self.chart_area,
                text="Para ver el gráfico instala matplotlib:\npython -m pip install matplotlib",
                bg=CARD, fg=CORAL, font=("Segoe UI", 11, "bold"), pady=40
            ).pack()
            self.canvas = None
        else:
            self.fig = Figure(figsize=(7.2, 3.6), dpi=100, facecolor=CARD)
            self.ax = self.fig.add_subplot(111)
            self.fig.subplots_adjust(left=0.12, right=0.97, top=0.86, bottom=0.18)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_area)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _build_explanation(self):
        self.explain_card = self._card(
            self.right_panel, "¿Qué está pasando?",
            "La explicación se actualiza cada vez que ejecutas la simulación."
        )
        self.explain_card.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        self.explanation = tk.Label(
            self.explain_card,
            text="Modifica los valores y pulsa Simular para interpretar el experimento.",
            bg=CARD, fg=TEXT, font=("Segoe UI", 10),
            justify="left", anchor="w", wraplength=740
        )
        self.explanation.pack(fill="x", padx=18, pady=(0, 16))

    def _set_defaults(self):
        defaults = {"mw": "100", "mx": "150", "tw": "22", "tx": "80", "tf": "35"}
        for key, value in defaults.items():
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)

    def reset(self):
        self._set_defaults()
        self.calculate()

    def calculate(self):
        try:
            mw = parse_number(self.entries["mw"], "masa del agua")
            mx = parse_number(self.entries["mx"], "masa de la muestra")
            tw = parse_number(self.entries["tw"], "temperatura inicial del agua")
            tx = parse_number(self.entries["tx"], "temperatura inicial de la muestra")
            tf = parse_number(self.entries["tf"], "temperatura final")

            if mw <= 0 or mx <= 0:
                raise ValueError("Las dos masas deben ser mayores que cero.")
            if abs(tx - tf) < 1e-12:
                raise ValueError("La temperatura de la muestra no puede ser igual a la temperatura final: habría división entre cero.")
            if abs(tf - tw) < 1e-12:
                messagebox.showwarning(
                    "Sin cambio de temperatura",
                    "El agua no cambió de temperatura. El resultado será cero y conviene revisar los datos."
                )

            # Convertir masas a kg para que las unidades sean coherentes con cw.
            mw_kg = mw / 1000.0
            mx_kg = mx / 1000.0
            cw = 4186.0  # J/(kg·°C)
            delta_water = tf - tw
            delta_sample = tx - tf
            cx = (cw * mw_kg * delta_water) / (mx_kg * delta_sample)
            q_water = cw * mw_kg * delta_water

            if not all(map(lambda value: abs(value) < float("inf"), [cx, q_water])):
                raise ValueError("Los datos generan un resultado no válido. Revisa los valores.")

            self.last_result = (mw, mx, tw, tx, tf, cx, q_water)
            self.metric_values["cx"].config(text=f"{cx:,.1f} J/(kg·°C)")
            self.metric_values["qwater"].config(text=f"{q_water:,.1f} J")
            if tx > tw:
                status = "La muestra empezó más caliente" if tx > tw else "Temperaturas similares"
            elif tw > tx:
                status = "El agua empezó más caliente"
            else:
                status = "Misma temperatura inicial"
            self.metric_values["status"].config(text=status)

            self._draw_chart(tw, tx, tf)
            self._write_explanation(mw, mx, tw, tx, tf, cx, q_water)
        except ValueError as error:
            messagebox.showerror("Revisa los datos", str(error))

    def _draw_chart(self, tw, tx, tf):
        if self.canvas is None:
            return
        self.ax.clear()
        labels = ["Agua\n(inicial)", "Muestra\n(inicial)", "Equilibrio\n(final)"]
        values = [tw, tx, tf]
        bars = self.ax.bar(
            labels, values, width=0.56,
            color=[TEAL, CORAL, BLUE], edgecolor="white", linewidth=1.5
        )
        self.ax.set_title("Temperaturas del experimento", color=NAVY, fontsize=12, fontweight="bold", pad=12)
        self.ax.set_ylabel("Temperatura (°C)", color=MUTED, fontsize=9)
        self.ax.set_ylim(min(0, min(values) - 8), max(values) + max(8, abs(max(values)) * 0.12))
        self.ax.grid(axis="y", linestyle="--", alpha=0.22)
        self.ax.set_axisbelow(True)
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_color(BORDER)
        self.ax.spines["bottom"].set_color(BORDER)
        self.ax.tick_params(colors=MUTED, labelsize=9)
        for bar, value in zip(bars, values):
            self.ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (max(values) - min(values) + 1) * 0.025,
                f"{value:g} °C", ha="center", va="bottom",
                color=TEXT, fontsize=9, fontweight="bold"
            )
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def _write_explanation(self, mw, mx, tw, tx, tf, cx, q_water):
        if tx > tw:
            direction = "La muestra comenzó a mayor temperatura que el agua, por lo que el escenario típico es que la muestra ceda energía y el agua la reciba."
        elif tw > tx:
            direction = "El agua comenzó a mayor temperatura que la muestra, así que el escenario típico es que el agua ceda energía y la muestra la reciba."
        else:
            direction = "Ambos materiales comenzaron a la misma temperatura; no hay una diferencia térmica inicial entre ellos."

        if tf > tw:
            water_change = f"El agua sube de {tw:g} °C a {tf:g} °C: su cambio de temperatura es positivo."
        elif tf < tw:
            water_change = f"El agua baja de {tw:g} °C a {tf:g} °C: su cambio de temperatura es negativo."
        else:
            water_change = "El agua no cambia de temperatura con los datos ingresados."

        if cx < 0:
            interpretation = "El resultado salió negativo. Eso suele indicar que las temperaturas o el orden de los cuerpos no son coherentes con la convención de signos de esta fórmula; revisa los datos del experimento."
        else:
            interpretation = f"Con la fórmula del simulador, la muestra tiene un calor específico calculado de {cx:,.2f} J/(kg·°C). Cuanto mayor sea este valor, más energía necesita por kilogramo para cambiar un grado Celsius."

        text = (
            f"{direction}\n\n"
            f"{water_change} El calor calculado para el agua es Qw = {q_water:,.2f} J. "
            f"El signo indica si el agua gana o pierde energía según la convención usada.\n\n"
            f"{interpretation}\n\n"
            "Modelo ideal: se supone que no hay pérdidas de energía al ambiente ni absorción apreciable de calor por el recipiente."
        )
        self.explanation.config(text=text)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalorimetriaApp(root)
    root.mainloop()
