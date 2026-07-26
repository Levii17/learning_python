"""
Resistor Color Code Tool
========================

Two-way resistor color band calculator for 4-band and 5-band resistors:

  * Colors -> Value   : pick the bands, get resistance + tolerance
  * Value -> Colors   : type a resistance, get the band sequence

Standard EIA color code used throughout (digit / multiplier / tolerance
tables below). This covers the common 4-band and 5-band cases; 6-band
resistors add a temperature-coefficient band which isn't modeled here.

The band math (`bands_to_resistance`, `value_to_bands`) has no tkinter
dependency, so it can be imported and reused on its own, e.g. as a quiz-
answer checker in the EE interview prep app.
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox

# ================= EIA Color Code Tables =================
# Digit bands: color -> digit value (index position doubles as the value)
DIGIT_COLORS = ["black", "brown", "red", "orange", "yellow",
                "green", "blue", "violet", "grey", "white"]

# Multiplier band: color -> power-of-ten exponent
MULTIPLIER_COLORS = {
    "silver": -2, "gold": -1, "black": 0, "brown": 1, "red": 2,
    "orange": 3, "yellow": 4, "green": 5, "blue": 6,
    "violet": 7, "grey": 8, "white": 9,
}
EXPONENT_TO_COLOR = {v: k for k, v in MULTIPLIER_COLORS.items()}

# Tolerance band: color -> +/- percent
TOLERANCE_COLORS = {
    "grey": 0.05, "violet": 0.1, "blue": 0.25, "green": 0.5,
    "brown": 1, "red": 2, "gold": 5, "silver": 10,
}
PERCENT_TO_TOLERANCE_COLOR = {v: k for k, v in TOLERANCE_COLORS.items()}

COLOR_HEX = {
    "black": "#1a1a1a", "brown": "#8B4513", "red": "#e60000",
    "orange": "#ff8c00", "yellow": "#ffd400", "green": "#0a8a0a",
    "blue": "#1560d4", "violet": "#8a2be2", "grey": "#8c8c8c",
    "white": "#f5f5f5", "gold": "#d4af37", "silver": "#c0c0c0",
}

UNIT_MULTIPLIERS = {"Ω": 1, "kΩ": 1e3, "MΩ": 1e6, "GΩ": 1e9}


# ================= Pure calculation logic (no GUI) =================
def bands_to_resistance(digit_colors, multiplier_color, tolerance_color):
    """digit_colors: list of 2 or 3 color names (most significant first)."""
    digits = [DIGIT_COLORS.index(c) for c in digit_colors]
    value = int("".join(str(d) for d in digits)) * (10 ** MULTIPLIER_COLORS[multiplier_color])
    tolerance_pct = TOLERANCE_COLORS[tolerance_color]
    return value, tolerance_pct


def value_to_bands(value_ohms, digit_count):
    """
    Reduces value_ohms to `digit_count` significant digits plus a power-of-
    ten multiplier. Returns (digits, multiplier_exponent, achieved_value,
    clamped) where achieved_value is what the resulting bands actually
    represent (may differ slightly from the input if it wasn't an exact
    fit), and clamped is True if the required multiplier fell outside the
    standard silver..white range (10^-2 to 10^9).
    """
    if value_ohms <= 0:
        raise ValueError("Resistance must be greater than zero.")

    exponent = math.floor(math.log10(value_ohms)) - (digit_count - 1)
    mantissa = round(value_ohms / (10 ** exponent))

    # Rounding can occasionally push the mantissa one digit either side
    # of the intended range (e.g. 999.6 -> 1000) -- renormalize if so.
    if mantissa >= 10 ** digit_count:
        mantissa //= 10
        exponent += 1
    elif mantissa < 10 ** (digit_count - 1):
        mantissa *= 10
        exponent -= 1

    clamped = False
    if exponent < -2:
        exponent, clamped = -2, True
    elif exponent > 9:
        exponent, clamped = 9, True

    digits = [int(ch) for ch in str(mantissa).zfill(digit_count)]
    achieved_value = mantissa * (10 ** exponent)
    return digits, exponent, achieved_value, clamped


def format_ohms(value):
    if value >= 1e9:
        return f"{value / 1e9:g} GΩ"
    if value >= 1e6:
        return f"{value / 1e6:g} MΩ"
    if value >= 1e3:
        return f"{value / 1e3:g} kΩ"
    return f"{value:g} Ω"


# ================= GUI =================
class ResistorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resistor Color Code Tool")
        self.root.geometry("760x640")
        self.root.configure(bg="#2c3e50")

        title = tk.Label(self.root, text="Resistor Color Code Tool", bd=12, relief=tk.GROOVE,
                          bg="#1abc9c", fg="white", font=("times new roman", 22, "bold"), pady=2)
        title.pack(fill=tk.X)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.forward_tab = tk.Frame(notebook, bg="#2c3e50")
        self.reverse_tab = tk.Frame(notebook, bg="#2c3e50")
        notebook.add(self.forward_tab, text="Colors -> Value")
        notebook.add(self.reverse_tab, text="Value -> Colors")

        self._build_forward_tab()
        self._build_reverse_tab()

        tk.Button(self.root, text="Exit", command=self.on_exit, bg="#e74c3c", fg="white",
                  font=("arial", 11, "bold"), width=12).pack(pady=(0, 10))

    # ---------------- Colors -> Value tab ----------------
    def _build_forward_tab(self):
        frame = self.forward_tab

        F1 = tk.LabelFrame(frame, text="Bands", font=("times new roman", 12, "bold"),
                            fg="gold", bg="#2c3e50", padx=10, pady=10)
        F1.pack(fill=tk.X, padx=10, pady=8)

        self.band_count = tk.IntVar(value=4)
        bc_frame = tk.Frame(F1, bg="#2c3e50")
        bc_frame.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))
        tk.Radiobutton(bc_frame, text="4-band", variable=self.band_count, value=4,
                       command=self._toggle_third_digit, bg="#2c3e50", fg="white",
                       selectcolor="#34495e", font=("arial", 10)).pack(side=tk.LEFT, padx=(0, 12))
        tk.Radiobutton(bc_frame, text="5-band", variable=self.band_count, value=5,
                       command=self._toggle_third_digit, bg="#2c3e50", fg="white",
                       selectcolor="#34495e", font=("arial", 10)).pack(side=tk.LEFT)

        self.digit1 = tk.StringVar(value="brown")
        self.digit2 = tk.StringVar(value="black")
        self.digit3 = tk.StringVar(value="black")
        self.multiplier_fwd = tk.StringVar(value="red")
        self.tolerance_fwd = tk.StringVar(value="gold")

        multiplier_order = ["silver", "gold"] + [c for c in DIGIT_COLORS]
        tolerance_order = sorted(TOLERANCE_COLORS, key=TOLERANCE_COLORS.get)

        tk.Label(F1, text="Band 1 (digit):", bg="#2c3e50", fg="white", font=("arial", 10)).grid(row=1, column=0, sticky="w", pady=4)
        ttk.Combobox(F1, textvariable=self.digit1, values=DIGIT_COLORS, state="readonly", width=10).grid(row=1, column=1, padx=6)

        tk.Label(F1, text="Band 2 (digit):", bg="#2c3e50", fg="white", font=("arial", 10)).grid(row=1, column=2, sticky="w", pady=4)
        ttk.Combobox(F1, textvariable=self.digit2, values=DIGIT_COLORS, state="readonly", width=10).grid(row=1, column=3, padx=6)

        self.digit3_label = tk.Label(F1, text="Band 3 (digit):", bg="#2c3e50", fg="white", font=("arial", 10))
        self.digit3_combo = ttk.Combobox(F1, textvariable=self.digit3, values=DIGIT_COLORS, state="readonly", width=10)
        self.digit3_label.grid(row=2, column=0, sticky="w", pady=4)
        self.digit3_combo.grid(row=2, column=1, padx=6)
        self._toggle_third_digit()

        tk.Label(F1, text="Multiplier:", bg="#2c3e50", fg="white", font=("arial", 10)).grid(row=3, column=0, sticky="w", pady=4)
        ttk.Combobox(F1, textvariable=self.multiplier_fwd, values=multiplier_order, state="readonly", width=10).grid(row=3, column=1, padx=6)

        tk.Label(F1, text="Tolerance:", bg="#2c3e50", fg="white", font=("arial", 10)).grid(row=3, column=2, sticky="w", pady=4)
        ttk.Combobox(F1, textvariable=self.tolerance_fwd, values=tolerance_order, state="readonly", width=10).grid(row=3, column=3, padx=6)

        btns = tk.Frame(frame, bg="#2c3e50")
        btns.pack(pady=6)
        tk.Button(btns, text="Calculate Resistance", command=self.on_calculate_forward,
                  bg="#3498db", fg="white", font=("arial", 11, "bold")).grid(row=0, column=0, padx=10)
        tk.Button(btns, text="Clear", command=self.on_clear_forward,
                  bg="#e67e22", fg="white", font=("arial", 11, "bold")).grid(row=0, column=1, padx=10)

        self.canvas_fwd = tk.Canvas(frame, width=600, height=200, bg="#ecf0f1", highlightthickness=0)
        self.canvas_fwd.pack(pady=10)

        self.result_fwd = tk.Label(frame, text="", bg="#2c3e50", fg="lightgreen",
                                    font=("courier new", 14, "bold"))
        self.result_fwd.pack()

        self._draw_resistor(self.canvas_fwd, ["brown", "black"], "red", "gold")
        self.on_calculate_forward()

    def _toggle_third_digit(self):
        if self.band_count.get() == 5:
            self.digit3_label.grid()
            self.digit3_combo.grid()
        else:
            self.digit3_label.grid_remove()
            self.digit3_combo.grid_remove()

    def on_calculate_forward(self):
        digit_colors = [self.digit1.get(), self.digit2.get()]
        if self.band_count.get() == 5:
            digit_colors.append(self.digit3.get())

        value, tolerance_pct = bands_to_resistance(digit_colors, self.multiplier_fwd.get(), self.tolerance_fwd.get())
        self.result_fwd.config(text=f"{format_ohms(value)}  ±{tolerance_pct:g}%   ({value:g} Ω)")
        self._draw_resistor(self.canvas_fwd, digit_colors + [self.multiplier_fwd.get()], self.tolerance_fwd.get())

    def on_clear_forward(self):
        self.digit1.set("brown")
        self.digit2.set("black")
        self.digit3.set("black")
        self.multiplier_fwd.set("red")
        self.tolerance_fwd.set("gold")
        self.band_count.set(4)
        self._toggle_third_digit()
        self.on_calculate_forward()

    # ---------------- Value -> Colors tab ----------------
    def _build_reverse_tab(self):
        frame = self.reverse_tab

        F1 = tk.LabelFrame(frame, text="Target Value", font=("times new roman", 12, "bold"),
                            fg="gold", bg="#2c3e50", padx=10, pady=10)
        F1.pack(fill=tk.X, padx=10, pady=8)

        self.band_count_rev = tk.IntVar(value=4)
        bc_frame = tk.Frame(F1, bg="#2c3e50")
        bc_frame.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))
        tk.Radiobutton(bc_frame, text="4-band", variable=self.band_count_rev, value=4,
                       bg="#2c3e50", fg="white", selectcolor="#34495e", font=("arial", 10)).pack(side=tk.LEFT, padx=(0, 12))
        tk.Radiobutton(bc_frame, text="5-band", variable=self.band_count_rev, value=5,
                       bg="#2c3e50", fg="white", selectcolor="#34495e", font=("arial", 10)).pack(side=tk.LEFT)

        self.value_entry = tk.StringVar(value="4.7")
        self.unit = tk.StringVar(value="kΩ")
        self.tolerance_rev = tk.StringVar(value="5")

        vcmd_amount = (self.root.register(self._validate_amount), "%P")

        tk.Label(F1, text="Resistance:", bg="#2c3e50", fg="white", font=("arial", 10)).grid(row=1, column=0, sticky="w", pady=4)
        tk.Entry(F1, textvariable=self.value_entry, width=10, font="arial 11",
                 validate="key", validatecommand=vcmd_amount).grid(row=1, column=1, padx=6)
        ttk.Combobox(F1, textvariable=self.unit, values=list(UNIT_MULTIPLIERS.keys()),
                     state="readonly", width=6).grid(row=1, column=2, padx=6)

        tolerance_values = [str(v) for v in sorted(TOLERANCE_COLORS.values())]
        tk.Label(F1, text="Tolerance (%):", bg="#2c3e50", fg="white", font=("arial", 10)).grid(row=1, column=3, sticky="w", pady=4)
        ttk.Combobox(F1, textvariable=self.tolerance_rev, values=tolerance_values,
                     state="readonly", width=6).grid(row=1, column=4, padx=6)

        btns = tk.Frame(frame, bg="#2c3e50")
        btns.pack(pady=6)
        tk.Button(btns, text="Calculate Bands", command=self.on_calculate_reverse,
                  bg="#3498db", fg="white", font=("arial", 11, "bold")).grid(row=0, column=0, padx=10)
        tk.Button(btns, text="Clear", command=self.on_clear_reverse,
                  bg="#e67e22", fg="white", font=("arial", 11, "bold")).grid(row=0, column=1, padx=10)

        self.canvas_rev = tk.Canvas(frame, width=600, height=200, bg="#ecf0f1", highlightthickness=0)
        self.canvas_rev.pack(pady=10)

        self.result_rev = tk.Label(frame, text="", bg="#2c3e50", fg="lightgreen",
                                    font=("courier new", 12, "bold"), justify=tk.LEFT)
        self.result_rev.pack()

        self.on_calculate_reverse()

    def _validate_amount(self, proposed):
        if proposed == "":
            return True
        if proposed.count(".") > 1:
            return False
        return all(ch.isdigit() or ch == "." for ch in proposed)

    def on_calculate_reverse(self):
        raw = self.value_entry.get()
        if raw in ("", "."):
            messagebox.showerror("Missing value", "Please enter a resistance value.")
            return

        ohms = float(raw) * UNIT_MULTIPLIERS[self.unit.get()]
        digit_count = 2 if self.band_count_rev.get() == 4 else 3

        try:
            digits, exponent, achieved, clamped = value_to_bands(ohms, digit_count)
        except ValueError as e:
            messagebox.showerror("Invalid value", str(e))
            return

        digit_colors = [DIGIT_COLORS[d] for d in digits]
        multiplier_color = EXPONENT_TO_COLOR[exponent]
        tolerance_pct = float(self.tolerance_rev.get())
        tolerance_color = PERCENT_TO_TOLERANCE_COLOR[tolerance_pct]

        band_names = digit_colors + [multiplier_color, tolerance_color]
        band_labels = " - ".join(c.capitalize() for c in band_names)

        lines = [f"Bands: {band_labels}"]
        if abs(achieved - ohms) > 1e-9:
            lines.append(f"(closest standard-representable value: {format_ohms(achieved)}, "
                          f"you entered {format_ohms(ohms)})")
        if clamped:
            lines.append("Note: exact multiplier is outside the standard silver..white range; clamped.")
        self.result_rev.config(text="\n".join(lines))

        self._draw_resistor(self.canvas_rev, digit_colors + [multiplier_color], tolerance_color)

    def on_clear_reverse(self):
        self.value_entry.set("")
        self.unit.set("kΩ")
        self.tolerance_rev.set("5")
        self.band_count_rev.set(4)
        self.result_rev.config(text="")
        self.canvas_rev.delete("all")

    def on_exit(self):
        if messagebox.askyesno("Exit", "Close the tool?"):
            self.root.destroy()

    # ---------------- Shared drawing helper ----------------
    def _draw_resistor(self, canvas, value_band_colors, tolerance_color):
        """value_band_colors: digit color(s) + multiplier color, in order."""
        canvas.delete("all")
        body_left, body_right, body_top, body_bottom = 100, 500, 60, 140

        # leads
        canvas.create_line(10, 100, body_left, 100, width=5, fill="#7f8c8d")
        canvas.create_line(body_right, 100, 590, 100, width=5, fill="#7f8c8d")
        # body
        canvas.create_rectangle(body_left, body_top, body_right, body_bottom,
                                 fill="#e8d5a8", outline="#333333", width=2)

        # value bands, evenly spaced with a bit of room before the tolerance gap
        band_width = 20
        spacing = 32
        x = body_left + 30
        for color in value_band_colors:
            canvas.create_rectangle(x, body_top, x + band_width, body_bottom,
                                     fill=COLOR_HEX[color], outline="#111111")
            x += spacing

        # tolerance band, separated by a visible gap near the right lead
        tol_x = body_right - 45
        canvas.create_rectangle(tol_x, body_top, tol_x + band_width, body_bottom,
                                 fill=COLOR_HEX[tolerance_color], outline="#111111")


if __name__ == "__main__":
    root = tk.Tk()
    app = ResistorApp(root)
    root.mainloop()