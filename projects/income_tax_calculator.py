"""
PAYE / Income Tax Calculator (South Africa)
============================================

Uses the official SARS individual tax tables for the 2025/2026 and 2026/2027
years of assessment (rates, rebates, thresholds and medical tax credits as
published in the National Budget). This is a planning/estimation tool, not
tax advice -- always check the current SARS tables before relying on a figure.

Python-vs-spreadsheet note (the reason this is a fun companion to the Excel
budget template): in a spreadsheet, computing progressive tax usually means
building a small helper table with a hardcoded "cumulative tax at the start
of each bracket" column, then a single lookup/IF formula against it -- because
spreadsheets don't loop naturally. `gross_tax()` below does the same
cumulative-bracket math but as a straightforward loop, so the "helper table"
never has to be hand-maintained or re-derived when a bracket changes -- only
the (threshold, rate) pairs in TAX_TABLES do. The `IMPORTANT: SARS also
publishes ready-made rounded 2025/2026 and 2026/2027 tax deduction tables --
this script is doing that calculation from tax deducting rules rather than
looking one up.

This module's core function (`gross_tax`) has no GUI dependency, so it can be
imported and reused directly in a script or notebook if you don't want the
tkinter front end:

    from paye_calculator import gross_tax, TAX_TABLES
    tax = gross_tax(450000, TAX_TABLES["2026/2027"]["brackets"])
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ================= SARS Tax Tables =================
# Brackets: list of (upper_bound_of_bracket, rate), ascending, last bound = inf.
# Source: SARS Budget 2025 (2025/2026 year of assessment) and Budget 2026
# (2026/2027 year of assessment).
TAX_TABLES = {
    "2025/2026 (1 Mar 2025 - 28 Feb 2026)": {
        "brackets": [
            (237_100, 0.18),
            (370_500, 0.26),
            (512_800, 0.31),
            (673_000, 0.36),
            (857_900, 0.39),
            (1_817_000, 0.41),
            (float("inf"), 0.45),
        ],
        "rebates": {"primary": 17_235, "secondary": 9_444, "tertiary": 3_145},
        "thresholds": {"under65": 95_750, "65to74": 148_217, "75plus": 165_689},
        "medical_credit": {"main": 364, "dependant": 364, "additional": 246},
    },
    "2026/2027 (1 Mar 2026 - 28 Feb 2027)": {
        "brackets": [
            (245_100, 0.18),
            (383_100, 0.26),
            (530_200, 0.31),
            (695_800, 0.36),
            (887_000, 0.39),
            (1_878_600, 0.41),
            (float("inf"), 0.45),
        ],
        "rebates": {"primary": 17_820, "secondary": 9_765, "tertiary": 3_249},
        "thresholds": {"under65": 99_000, "65to74": 153_250, "75plus": 171_300},
        "medical_credit": {"main": 376, "dependant": 376, "additional": 254},
    },
}

# UIF: 1% of remuneration, capped at a monthly earnings ceiling. The ceiling
# has held at R17,712/month (max R177.12 employee contribution) for several
# tax years running, so the same figure is used for both years above.
UIF_RATE = 0.01
UIF_MONTHLY_CEILING = 17_712

AGE_LABELS = {
    "under65": "Under 65",
    "65to74": "65 to 74",
    "75plus": "75 and older",
}


# ================= Pure calculation logic (no GUI) =================
def gross_tax(taxable_income, brackets):
    """Progressive tax before rebates, for a given annual taxable income."""
    tax = 0.0
    lower = 0
    for upper, rate in brackets:
        if taxable_income > lower:
            slice_amount = min(taxable_income, upper) - lower
            tax += slice_amount * rate
        lower = upper
        if taxable_income <= upper:
            break
    return tax


def bracket_breakdown(taxable_income, brackets):
    """Per-bracket (rate, taxed_amount, tax_on_slice) rows, for display."""
    rows = []
    lower = 0
    for upper, rate in brackets:
        if taxable_income > lower:
            slice_amount = min(taxable_income, upper) - lower
            rows.append((lower, min(taxable_income, upper), rate, slice_amount * rate))
        lower = upper
        if taxable_income <= upper:
            break
    return rows


def marginal_rate(taxable_income, brackets):
    for upper, rate in brackets:
        if taxable_income <= upper:
            return rate
    return brackets[-1][1]


def medical_credit_annual(table, dependants):
    """dependants = number of people on the scheme excluding the main member."""
    mc = table["medical_credit"]
    monthly = mc["main"]
    if dependants >= 1:
        monthly += mc["dependant"]
        monthly += mc["additional"] * (dependants - 1)
    return monthly * 12


def rebate_total(table, age_group):
    rebates = table["rebates"]
    total = rebates["primary"]
    if age_group in ("65to74", "75plus"):
        total += rebates["secondary"]
    if age_group == "75plus":
        total += rebates["tertiary"]
    return total


def calculate(taxable_income_annual, tax_year, age_group, has_medical_aid, dependants, apply_uif):
    """Runs the full calculation and returns a dict of results."""
    table = TAX_TABLES[tax_year]
    brackets = table["brackets"]

    gross = gross_tax(taxable_income_annual, brackets)
    rebate = rebate_total(table, age_group)
    after_rebate = max(gross - rebate, 0)

    med_credit = medical_credit_annual(table, dependants) if has_medical_aid else 0
    net_annual_tax = max(after_rebate - med_credit, 0)

    monthly_gross = taxable_income_annual / 12
    monthly_paye = net_annual_tax / 12
    uif_monthly = min(monthly_gross, UIF_MONTHLY_CEILING) * UIF_RATE if apply_uif else 0
    net_monthly_pay = monthly_gross - monthly_paye - uif_monthly

    return {
        "table": table,
        "breakdown": bracket_breakdown(taxable_income_annual, brackets),
        "gross_tax": gross,
        "rebate": rebate,
        "medical_credit": med_credit,
        "net_annual_tax": net_annual_tax,
        "monthly_gross": monthly_gross,
        "monthly_paye": monthly_paye,
        "uif_monthly": uif_monthly,
        "net_monthly_pay": net_monthly_pay,
        "effective_rate": (net_annual_tax / taxable_income_annual * 100) if taxable_income_annual else 0,
        "marginal_rate": marginal_rate(taxable_income_annual, brackets) * 100,
    }


# ================= GUI =================
class PAYEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PAYE / Income Tax Calculator (South Africa)")
        self.root.geometry("820x680")
        self.root.configure(bg="#2c3e50")

        # ---- Variables ----
        self.tax_year = tk.StringVar(value=list(TAX_TABLES.keys())[-1])
        self.age_group = tk.StringVar(value="under65")
        self.frequency = tk.StringVar(value="annual")
        self.salary = tk.StringVar(value="")
        self.has_medical_aid = tk.BooleanVar(value=False)
        self.dependants = tk.StringVar(value="0")
        self.apply_uif = tk.BooleanVar(value=True)

        # Validators: digits (+ one optional decimal point) for money, digits only for counts
        self.vcmd_amount = (self.root.register(self._validate_amount), "%P")
        self.vcmd_int = (self.root.register(self._validate_int), "%P")

        title = tk.Label(self.root, text="PAYE / Income Tax Calculator", bd=12, relief=tk.GROOVE,
                          bg="#1abc9c", fg="white", font=("times new roman", 22, "bold"), pady=2)
        title.pack(fill=tk.X)

        # ---- Inputs frame ----
        F1 = tk.LabelFrame(self.root, text="Your Details", font=("times new roman", 12, "bold"),
                            fg="gold", bg="#2c3e50", padx=10, pady=10)
        F1.pack(fill=tk.X, padx=10, pady=8)

        tk.Label(F1, text="Tax year:", bg="#2c3e50", fg="white", font=("arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=4)
        ttk.Combobox(F1, textvariable=self.tax_year, values=list(TAX_TABLES.keys()),
                     state="readonly", width=32).grid(row=0, column=1, columnspan=3, sticky="w", pady=4)

        tk.Label(F1, text="Age:", bg="#2c3e50", fg="white", font=("arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=4)
        age_frame = tk.Frame(F1, bg="#2c3e50")
        age_frame.grid(row=1, column=1, columnspan=3, sticky="w")
        for key, label in AGE_LABELS.items():
            tk.Radiobutton(age_frame, text=label, variable=self.age_group, value=key,
                           bg="#2c3e50", fg="white", selectcolor="#34495e",
                           font=("arial", 10)).pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(F1, text="Salary is:", bg="#2c3e50", fg="white", font=("arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=4)
        freq_frame = tk.Frame(F1, bg="#2c3e50")
        freq_frame.grid(row=2, column=1, columnspan=3, sticky="w")
        tk.Radiobutton(freq_frame, text="Annual (taxable income)", variable=self.frequency, value="annual",
                       bg="#2c3e50", fg="white", selectcolor="#34495e", font=("arial", 10)).pack(side=tk.LEFT, padx=(0, 12))
        tk.Radiobutton(freq_frame, text="Monthly (before tax)", variable=self.frequency, value="monthly",
                       bg="#2c3e50", fg="white", selectcolor="#34495e", font=("arial", 10)).pack(side=tk.LEFT)

        tk.Label(F1, text="Amount (R):", bg="#2c3e50", fg="white", font=("arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=4)
        tk.Entry(F1, textvariable=self.salary, width=18, font="arial 11",
                 validate="key", validatecommand=self.vcmd_amount).grid(row=3, column=1, sticky="w", pady=4)
        tk.Label(F1, text="(enter income after retirement/pension contributions, before tax)",
                 bg="#2c3e50", fg="#bdc3c7", font=("arial", 8, "italic")).grid(row=3, column=2, columnspan=2, sticky="w")

        tk.Checkbutton(F1, text="On a medical aid scheme", variable=self.has_medical_aid,
                       bg="#2c3e50", fg="white", selectcolor="#34495e", font=("arial", 11, "bold"),
                       command=self._toggle_dependants).grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 4))

        tk.Label(F1, text="Dependants on scheme (excl. you):", bg="#2c3e50", fg="white",
                 font=("arial", 10)).grid(row=5, column=0, sticky="w")
        self.dependants_entry = tk.Entry(F1, textvariable=self.dependants, width=6, font="arial 11",
                                          validate="key", validatecommand=self.vcmd_int, state="disabled")
        self.dependants_entry.grid(row=5, column=1, sticky="w")

        tk.Checkbutton(F1, text="Include UIF (1%, capped monthly)", variable=self.apply_uif,
                       bg="#2c3e50", fg="white", selectcolor="#34495e", font=("arial", 11, "bold")).grid(row=6, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # ---- Buttons ----
        btn_frame = tk.Frame(self.root, bg="#2c3e50")
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Calculate", command=self.on_calculate, bg="#3498db", fg="white",
                  font=("arial", 12, "bold"), width=12).grid(row=0, column=0, padx=15)
        tk.Button(btn_frame, text="Clear", command=self.on_clear, bg="#e67e22", fg="white",
                  font=("arial", 12, "bold"), width=12).grid(row=0, column=1, padx=15)
        tk.Button(btn_frame, text="Exit", command=self.on_exit, bg="#e74c3c", fg="white",
                  font=("arial", 12, "bold"), width=12).grid(row=0, column=2, padx=15)

        # ---- Results ----
        F2 = tk.LabelFrame(self.root, text="Breakdown", font=("times new roman", 12, "bold"),
                            fg="gold", bg="#2c3e50")
        F2.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        scroll_y = tk.Scrollbar(F2, orient=tk.VERTICAL)
        self.output = tk.Text(F2, yscrollcommand=scroll_y.set, font=("courier new", 10))
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.config(command=self.output.yview)
        self.output.pack(fill=tk.BOTH, expand=True)
        self._write_placeholder()

    # ---- Validators ----
    def _validate_amount(self, proposed):
        if proposed == "":
            return True
        if proposed.count(".") > 1:
            return False
        return all(ch.isdigit() or ch == "." for ch in proposed)

    def _validate_int(self, proposed):
        return proposed == "" or proposed.isdigit()

    def _toggle_dependants(self):
        self.dependants_entry.config(state="normal" if self.has_medical_aid.get() else "disabled")

    # ---- UI actions ----
    def _write_placeholder(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "Enter your details above and click Calculate.\n\n"
                                    "Note: this is a planning estimate based on the published\n"
                                    "SARS tax tables, not an official SARS calculation or tax advice.")

    def on_calculate(self):
        raw = self.salary.get()
        if raw in ("", "."):
            messagebox.showerror("Missing amount", "Please enter a salary amount.")
            return

        amount = float(raw)
        if amount <= 0:
            messagebox.showerror("Invalid amount", "Salary must be greater than zero.")
            return

        taxable_income_annual = amount * 12 if self.frequency.get() == "monthly" else amount
        dependants = int(self.dependants.get()) if self.dependants.get() else 0

        result = calculate(
            taxable_income_annual=taxable_income_annual,
            tax_year=self.tax_year.get(),
            age_group=self.age_group.get(),
            has_medical_aid=self.has_medical_aid.get(),
            dependants=dependants,
            apply_uif=self.apply_uif.get(),
        )
        self._render(result, taxable_income_annual)

    def _render(self, r, taxable_income_annual):
        self.output.delete("1.0", tk.END)
        w = self.output
        w.insert(tk.END, f"Tax year: {self.tax_year.get()}\n")
        w.insert(tk.END, f"Age band: {AGE_LABELS[self.age_group.get()]}\n")
        w.insert(tk.END, f"Annual taxable income: R{taxable_income_annual:,.2f}\n")
        w.insert(tk.END, "=" * 58 + "\n")
        w.insert(tk.END, "Bracket breakdown\n")
        w.insert(tk.END, "-" * 58 + "\n")
        for lower, upper, rate, tax_on_slice in r["breakdown"]:
            upper_label = f"R{upper:,.0f}" if upper != float("inf") else "and above"
            w.insert(tk.END, f"  R{lower:,.0f} - {upper_label:<14} @ {rate*100:>4.0f}%  = R{tax_on_slice:,.2f}\n")
        w.insert(tk.END, "-" * 58 + "\n")
        w.insert(tk.END, f"Gross tax (before rebates):        R{r['gross_tax']:,.2f}\n")
        w.insert(tk.END, f"Less: age-based rebate:            R{r['rebate']:,.2f}\n")
        if self.has_medical_aid.get():
            w.insert(tk.END, f"Less: medical scheme tax credit:   R{r['medical_credit']:,.2f}\n")
        w.insert(tk.END, "=" * 58 + "\n")
        w.insert(tk.END, f"NET ANNUAL TAX (PAYE for the year): R{r['net_annual_tax']:,.2f}\n")
        w.insert(tk.END, "=" * 58 + "\n\n")

        w.insert(tk.END, f"Monthly gross income:               R{r['monthly_gross']:,.2f}\n")
        w.insert(tk.END, f"Monthly PAYE deduction:              R{r['monthly_paye']:,.2f}\n")
        if self.apply_uif.get():
            w.insert(tk.END, f"Monthly UIF deduction (1%, capped):  R{r['uif_monthly']:,.2f}\n")
        w.insert(tk.END, f"Estimated monthly take-home pay:     R{r['net_monthly_pay']:,.2f}\n\n")

        w.insert(tk.END, f"Effective tax rate: {r['effective_rate']:.2f}%\n")
        w.insert(tk.END, f"Marginal tax rate:  {r['marginal_rate']:.0f}%\n\n")
        w.insert(tk.END, "Estimate only -- confirm against the current SARS tables before relying on it.")

    def on_clear(self):
        self.salary.set("")
        self.dependants.set("0")
        self.has_medical_aid.set(False)
        self._toggle_dependants()
        self._write_placeholder()

    def on_exit(self):
        if messagebox.askyesno("Exit", "Close the calculator?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PAYEApp(root)
    root.mainloop()