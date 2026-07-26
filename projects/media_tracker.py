"""
Library / Media Tracker
========================

Tracks books, courses, or any other media you're working through -- status,
rating, notes -- backed by a local SQLite database instead of in-memory
state, so the list survives closing the app.

The database lives at media_tracker.db, next to this script, and is created
automatically on first run.

`MediaDB` has no tkinter dependency, so the CRUD layer can be reused/tested
independently of the GUI (see the test at the bottom of this docstring-style
note: run this file's logic against a temp DB without ever opening a window).
"""

import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media_tracker.db")

STATUS_OPTIONS = ["To Do", "In Progress", "Completed", "Abandoned"]
TYPE_SUGGESTIONS = ["Book", "Course", "Movie", "Podcast", "Article", "Other"]
RATING_OPTIONS = ["Not rated", "1", "2", "3", "4", "5"]

COLUMNS = ("id", "title", "media_type", "creator", "status", "rating", "date_added", "date_completed")
COLUMN_LABELS = {
    "id": "ID", "title": "Title", "media_type": "Type", "creator": "Author/Creator",
    "status": "Status", "rating": "Rating", "date_added": "Added", "date_completed": "Completed",
}


# ================= Data layer (no GUI dependency) =================
class MediaDB:
    """Thin wrapper around sqlite3 handling all CRUD for media_items."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_schema()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS media_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    media_type TEXT NOT NULL,
                    creator TEXT,
                    status TEXT NOT NULL,
                    rating INTEGER,
                    date_added TEXT NOT NULL,
                    date_completed TEXT,
                    notes TEXT
                )
            """)

    def add_item(self, title, media_type, creator, status, rating, date_added, date_completed, notes):
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO media_items
                   (title, media_type, creator, status, rating, date_added, date_completed, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (title, media_type, creator, status, rating, date_added, date_completed, notes),
            )
            return cur.lastrowid

    def update_item(self, item_id, title, media_type, creator, status, rating, date_added, date_completed, notes):
        with self._connect() as conn:
            conn.execute(
                """UPDATE media_items
                   SET title=?, media_type=?, creator=?, status=?, rating=?,
                       date_added=?, date_completed=?, notes=?
                   WHERE id=?""",
                (title, media_type, creator, status, rating, date_added, date_completed, notes, item_id),
            )

    def delete_item(self, item_id):
        with self._connect() as conn:
            conn.execute("DELETE FROM media_items WHERE id=?", (item_id,))

    def get_item(self, item_id):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM media_items WHERE id=?", (item_id,)).fetchone()
            return dict(row) if row else None

    def get_all(self, search_text="", status_filter="All", type_filter="All"):
        query = "SELECT * FROM media_items WHERE 1=1"
        params = []
        if search_text:
            query += " AND (title LIKE ? OR creator LIKE ?)"
            like = f"%{search_text}%"
            params += [like, like]
        if status_filter != "All":
            query += " AND status = ?"
            params.append(status_filter)
        if type_filter != "All":
            query += " AND media_type = ?"
            params.append(type_filter)
        query += " ORDER BY date_added DESC, id DESC"
        with self._connect() as conn:
            return [dict(r) for r in conn.execute(query, params).fetchall()]

    def distinct_types(self):
        with self._connect() as conn:
            rows = conn.execute("SELECT DISTINCT media_type FROM media_items ORDER BY media_type").fetchall()
            return [r["media_type"] for r in rows]

    def stats(self):
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) c FROM media_items").fetchone()["c"]
            completed = conn.execute("SELECT COUNT(*) c FROM media_items WHERE status='Completed'").fetchone()["c"]
            avg_rating = conn.execute("SELECT AVG(rating) a FROM media_items WHERE rating IS NOT NULL").fetchone()["a"]
            return total, completed, (avg_rating or 0)


def valid_date_str(s):
    if s == "":
        return True
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ================= GUI =================
class MediaTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library / Media Tracker")
        self.root.geometry("1050x720")
        self.root.configure(bg="#2c3e50")

        self.db = MediaDB()
        self.selected_id = None

        title = tk.Label(self.root, text="Library / Media Tracker", bd=12, relief=tk.GROOVE,
                          bg="#1abc9c", fg="white", font=("times new roman", 22, "bold"), pady=2)
        title.pack(fill=tk.X)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        body = tk.Frame(self.root, bg="#2c3e50")
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        self._build_form(body)
        self._build_list(body)

        self.stats_label = tk.Label(self.root, text="", bg="#2c3e50", fg="lightgreen", font=("arial", 10, "bold"))
        self.stats_label.pack(pady=(0, 8))

        self.refresh_list()

    # ---------------- Form (left) ----------------
    def _build_form(self, parent):
        F1 = tk.LabelFrame(parent, text="Item Details", font=("times new roman", 12, "bold"),
                            fg="gold", bg="#2c3e50", padx=10, pady=10)
        F1.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.title_var = tk.StringVar()
        self.type_var = tk.StringVar(value="Book")
        self.creator_var = tk.StringVar()
        self.status_var = tk.StringVar(value="To Do")
        self.rating_var = tk.StringVar(value="Not rated")
        self.date_added_var = tk.StringVar(value=date.today().isoformat())
        self.date_completed_var = tk.StringVar()

        row = 0
        tk.Label(F1, text="Title *", bg="#2c3e50", fg="white", font=("arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=4)
        tk.Entry(F1, textvariable=self.title_var, width=28, font="arial 11").grid(row=row, column=1, columnspan=2, pady=4)

        row += 1
        tk.Label(F1, text="Type", bg="#2c3e50", fg="white", font=("arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Combobox(F1, textvariable=self.type_var, values=TYPE_SUGGESTIONS, width=25).grid(row=row, column=1, columnspan=2, pady=4)

        row += 1
        tk.Label(F1, text="Author/Creator", bg="#2c3e50", fg="white", font=("arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=4)
        tk.Entry(F1, textvariable=self.creator_var, width=28, font="arial 11").grid(row=row, column=1, columnspan=2, pady=4)

        row += 1
        tk.Label(F1, text="Status", bg="#2c3e50", fg="white", font=("arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Combobox(F1, textvariable=self.status_var, values=STATUS_OPTIONS, state="readonly", width=25).grid(row=row, column=1, columnspan=2, pady=4)

        row += 1
        tk.Label(F1, text="Rating", bg="#2c3e50", fg="white", font=("arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Combobox(F1, textvariable=self.rating_var, values=RATING_OPTIONS, state="readonly", width=25).grid(row=row, column=1, columnspan=2, pady=4)

        row += 1
        tk.Label(F1, text="Date added", bg="#2c3e50", fg="white", font=("arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=4)
        tk.Entry(F1, textvariable=self.date_added_var, width=14, font="arial 11").grid(row=row, column=1, sticky="w", pady=4)
        tk.Button(F1, text="Today", command=lambda: self.date_added_var.set(date.today().isoformat()),
                  bg="#34495e", fg="white", font=("arial", 8)).grid(row=row, column=2, sticky="w")

        row += 1
        tk.Label(F1, text="Date completed", bg="#2c3e50", fg="white", font=("arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=4)
        tk.Entry(F1, textvariable=self.date_completed_var, width=14, font="arial 11").grid(row=row, column=1, sticky="w", pady=4)
        tk.Button(F1, text="Today", command=lambda: self.date_completed_var.set(date.today().isoformat()),
                  bg="#34495e", fg="white", font=("arial", 8)).grid(row=row, column=2, sticky="w")
        row += 1
        tk.Label(F1, text="(format: YYYY-MM-DD)", bg="#2c3e50", fg="#95a5a6", font=("arial", 8, "italic")).grid(row=row, column=1, sticky="w")

        row += 1
        tk.Label(F1, text="Notes", bg="#2c3e50", fg="white", font=("arial", 10, "bold")).grid(row=row, column=0, sticky="nw", pady=4)
        self.notes_text = tk.Text(F1, width=28, height=6, font="arial 10")
        self.notes_text.grid(row=row, column=1, columnspan=2, pady=4)

        row += 1
        btns = tk.Frame(F1, bg="#2c3e50")
        btns.grid(row=row, column=0, columnspan=3, pady=(10, 0))
        tk.Button(btns, text="Add New", command=self.on_add, bg="#2ecc71", fg="white",
                  font=("arial", 10, "bold"), width=10).grid(row=0, column=0, padx=4, pady=3)
        tk.Button(btns, text="Update", command=self.on_update, bg="#3498db", fg="white",
                  font=("arial", 10, "bold"), width=10).grid(row=0, column=1, padx=4, pady=3)
        tk.Button(btns, text="Delete", command=self.on_delete, bg="#e74c3c", fg="white",
                  font=("arial", 10, "bold"), width=10).grid(row=1, column=0, padx=4, pady=3)
        tk.Button(btns, text="Clear / New", command=self.on_clear, bg="#e67e22", fg="white",
                  font=("arial", 10, "bold"), width=10).grid(row=1, column=1, padx=4, pady=3)

    # ---------------- List + filters (right) ----------------
    def _build_list(self, parent):
        right = tk.Frame(parent, bg="#2c3e50")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        filt = tk.LabelFrame(right, text="Search & Filter", font=("times new roman", 11, "bold"),
                              fg="gold", bg="#2c3e50", padx=8, pady=8)
        filt.pack(fill=tk.X, pady=(0, 8))

        self.search_var = tk.StringVar()
        self.status_filter_var = tk.StringVar(value="All")
        self.type_filter_var = tk.StringVar(value="All")

        tk.Label(filt, text="Search:", bg="#2c3e50", fg="white", font=("arial", 10)).grid(row=0, column=0, sticky="w")
        search_entry = tk.Entry(filt, textvariable=self.search_var, width=20, font="arial 10")
        search_entry.grid(row=0, column=1, padx=6)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_list())

        tk.Label(filt, text="Status:", bg="#2c3e50", fg="white", font=("arial", 10)).grid(row=0, column=2, sticky="w")
        self.status_filter_combo = ttk.Combobox(filt, textvariable=self.status_filter_var,
                                                  values=["All"] + STATUS_OPTIONS, state="readonly", width=14)
        self.status_filter_combo.grid(row=0, column=3, padx=6)
        self.status_filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_list())

        tk.Label(filt, text="Type:", bg="#2c3e50", fg="white", font=("arial", 10)).grid(row=0, column=4, sticky="w")
        self.type_filter_combo = ttk.Combobox(filt, textvariable=self.type_filter_var,
                                               state="readonly", width=14)
        self.type_filter_combo.grid(row=0, column=5, padx=6)
        self.type_filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_list())

        tree_frame = tk.Frame(right, bg="#2c3e50")
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=COLUMNS, show="headings", selectmode="browse")
        for col in COLUMNS:
            self.tree.heading(col, text=COLUMN_LABELS[col], command=lambda c=col: self.sort_by_column(c))
            width = 50 if col == "id" else (90 if col in ("status", "rating", "date_added", "date_completed") else 180)
            self.tree.column(col, width=width, anchor="w")

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        self._sort_state = {}

    # ---------------- Data <-> form helpers ----------------
    def get_form_values(self):
        rating_raw = self.rating_var.get()
        rating = None if rating_raw == "Not rated" else int(rating_raw)
        return {
            "title": self.title_var.get().strip(),
            "media_type": self.type_var.get().strip() or "Other",
            "creator": self.creator_var.get().strip(),
            "status": self.status_var.get(),
            "rating": rating,
            "date_added": self.date_added_var.get().strip() or date.today().isoformat(),
            "date_completed": self.date_completed_var.get().strip(),
            "notes": self.notes_text.get("1.0", tk.END).strip(),
        }

    def populate_form(self, item):
        self.title_var.set(item["title"])
        self.type_var.set(item["media_type"])
        self.creator_var.set(item["creator"] or "")
        self.status_var.set(item["status"])
        self.rating_var.set("Not rated" if item["rating"] is None else str(item["rating"]))
        self.date_added_var.set(item["date_added"] or "")
        self.date_completed_var.set(item["date_completed"] or "")
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert(tk.END, item["notes"] or "")

    def validate_form(self, values):
        if not values["title"]:
            messagebox.showerror("Missing title", "Title is required.")
            return False
        if not valid_date_str(values["date_added"]):
            messagebox.showerror("Invalid date", "Date added must be in YYYY-MM-DD format.")
            return False
        if not valid_date_str(values["date_completed"]):
            messagebox.showerror("Invalid date", "Date completed must be in YYYY-MM-DD format (or left blank).")
            return False
        return True

    # ---------------- Button actions ----------------
    def on_add(self):
        values = self.get_form_values()
        if not self.validate_form(values):
            return
        new_id = self.db.add_item(**values)
        messagebox.showinfo("Added", f"Added '{values['title']}' (ID {new_id}).")
        self.on_clear()
        self.refresh_list()

    def on_update(self):
        if self.selected_id is None:
            messagebox.showerror("No selection", "Select a row in the list to update first.")
            return
        values = self.get_form_values()
        if not self.validate_form(values):
            return
        self.db.update_item(self.selected_id, **values)
        self.refresh_list()

    def on_delete(self):
        if self.selected_id is None:
            messagebox.showerror("No selection", "Select a row in the list to delete first.")
            return
        if messagebox.askyesno("Delete", "Delete the selected item? This can't be undone."):
            self.db.delete_item(self.selected_id)
            self.on_clear()
            self.refresh_list()

    def on_clear(self):
        self.selected_id = None
        self.title_var.set("")
        self.type_var.set("Book")
        self.creator_var.set("")
        self.status_var.set("To Do")
        self.rating_var.set("Not rated")
        self.date_added_var.set(date.today().isoformat())
        self.date_completed_var.set("")
        self.notes_text.delete("1.0", tk.END)
        for row_id in self.tree.selection():
            self.tree.selection_remove(row_id)

    def on_row_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        item_id = int(self.tree.item(selection[0])["values"][0])
        item = self.db.get_item(item_id)
        if item:
            self.selected_id = item_id
            self.populate_form(item)

    def sort_by_column(self, col):
        reverse = self._sort_state.get(col, False)
        rows = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try:
            rows.sort(key=lambda t: float(t[0]) if t[0] not in ("", None) else -1, reverse=reverse)
        except ValueError:
            rows.sort(key=lambda t: t[0].lower(), reverse=reverse)
        for index, (_, k) in enumerate(rows):
            self.tree.move(k, "", index)
        self._sort_state[col] = not reverse

    # ---------------- Refresh ----------------
    def refresh_list(self):
        for row_id in self.tree.get_children():
            self.tree.delete(row_id)

        items = self.db.get_all(
            search_text=self.search_var.get().strip(),
            status_filter=self.status_filter_var.get(),
            type_filter=self.type_filter_var.get(),
        )
        for item in items:
            self.tree.insert("", tk.END, values=(
                item["id"], item["title"], item["media_type"], item["creator"] or "",
                item["status"], "-" if item["rating"] is None else item["rating"],
                item["date_added"] or "", item["date_completed"] or "",
            ))

        self.type_filter_combo["values"] = ["All"] + self.db.distinct_types()

        total, completed, avg_rating = self.db.stats()
        self.stats_label.config(
            text=f"{total} item(s) total   |   {completed} completed   |   avg rating: {avg_rating:.1f}/5"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = MediaTrackerApp(root)
    root.mainloop()