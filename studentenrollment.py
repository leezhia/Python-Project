import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os


class StudentEnrollmentSystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Enrollment System")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        # Database connection
        self.db_connection = None
        self.connect_db()


        self.input_frame = ttk.LabelFrame(
            self.root,
            text="Student Information",
            padding=10
        )
        self.input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.button_frame = ttk.Frame(self.root, padding=10)
        self.button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.tree_frame = ttk.Frame(self.root, padding=10)
        self.tree_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Configure resizing
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)


        ttk.Label(self.input_frame, text="Student ID:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.student_id = ttk.Entry(self.input_frame, width=20)
        self.student_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="First Name:").grid(
            row=0, column=2, padx=5, pady=5, sticky="e"
        )
        self.first_name = ttk.Entry(self.input_frame, width=20)
        self.first_name.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Last Name:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.last_name = ttk.Entry(self.input_frame, width=20)
        self.last_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Email:").grid(
            row=1, column=2, padx=5, pady=5, sticky="e"
        )
        self.email = ttk.Entry(self.input_frame, width=20)
        self.email.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Phone:").grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )
        self.phone = ttk.Entry(self.input_frame, width=20)
        self.phone.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Course:").grid(
            row=2, column=2, padx=5, pady=5, sticky="e"
        )
        self.course = ttk.Entry(self.input_frame, width=20)
        self.course.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Enrollment Date:").grid(
            row=3, column=0, padx=5, pady=5, sticky="e"
        )
        self.enrollment_date = ttk.Entry(self.input_frame, width=20)
        self.enrollment_date.grid(row=3, column=1, padx=5, pady=5)

        self.enrollment_date.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )


        ttk.Button(
            self.button_frame,
            text="Add Student",
            command=self.add_student
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            self.button_frame,
            text="Update Student",
            command=self.update_student
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            self.button_frame,
            text="Delete Student",
            command=self.delete_student
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            self.button_frame,
            text="Clear Fields",
            command=self.clear_fields
        ).grid(row=0, column=3, padx=5)

        ttk.Button(
            self.button_frame,
            text="Refresh Data",
            command=self.load_data
        ).grid(row=0, column=4, padx=5)


        columns = (
            "student_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "course",
            "enrollment_date"
        )

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show="headings"
        )

        headings = [
            "Student ID",
            "First Name",
            "Last Name",
            "Email",
            "Phone",
            "Course",
            "Enrollment Date"
        ]

        for col, heading in zip(columns, headings):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(
            self.tree_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.load_data()

    # ================= DATABASE =================
    def connect_db(self):
        try:
            if not os.path.exists("data"):
                os.makedirs("data")

            self.db_connection = sqlite3.connect(
                "data/student_db.sqlite"
            )

            self.create_table()

        except sqlite3.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Error connecting to database:\n{err}"
            )

    def create_table(self):
        try:
            cursor = self.db_connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    course TEXT,
                    enrollment_date TEXT
                )
            """)

            self.db_connection.commit()

        except sqlite3.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Error creating table:\n{err}"
            )

    def add_student(self):

        student_id = self.student_id.get()
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        email = self.email.get()
        phone = self.phone.get()
        course = self.course.get()
        enrollment_date = self.enrollment_date.get()

        if not student_id or not first_name or not last_name:
            messagebox.showerror(
                "Input Error",
                "Student ID, First Name, and Last Name are required!"
            )
            return

        try:
            cursor = self.db_connection.cursor()

            cursor.execute("""
                INSERT INTO students
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                first_name,
                last_name,
                email,
                phone,
                course,
                enrollment_date
            ))

            self.db_connection.commit()

            messagebox.showinfo(
                "Success",
                "Student added successfully!"
            )

            self.load_data()
            self.clear_fields()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Student ID already exists!"
            )

        except sqlite3.Error as err:
            messagebox.showerror(
                "Database Error",
                f"{err}"
            )

    def update_student(self):

        student_id = self.student_id.get()

        if not student_id:
            messagebox.showerror(
                "Input Error",
                "Select a student first!"
            )
            return

        try:
            cursor = self.db_connection.cursor()

            cursor.execute("""
                UPDATE students
                SET first_name=?,
                    last_name=?,
                    email=?,
                    phone=?,
                    course=?,
                    enrollment_date=?
                WHERE student_id=?
            """, (
                self.first_name.get(),
                self.last_name.get(),
                self.email.get(),
                self.phone.get(),
                self.course.get(),
                self.enrollment_date.get(),
                student_id
            ))

            self.db_connection.commit()

            messagebox.showinfo(
                "Success",
                "Student updated successfully!"
            )

            self.load_data()

        except sqlite3.Error as err:
            messagebox.showerror(
                "Database Error",
                f"{err}"
            )

    def delete_student(self):

        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror(
                "Selection Error",
                "Select a student to delete!"
            )
            return

        student_id = self.tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete student {student_id}?"
        )

        if not confirm:
            return

        try:
            cursor = self.db_connection.cursor()

            cursor.execute(
                "DELETE FROM students WHERE student_id=?",
                (student_id,)
            )

            self.db_connection.commit()

            messagebox.showinfo(
                "Success",
                "Student deleted successfully!"
            )

            self.load_data()
            self.clear_fields()

        except sqlite3.Error as err:
            messagebox.showerror(
                "Database Error",
                f"{err}"
            )

    def load_data(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cursor = self.db_connection.cursor()

            cursor.execute(
                "SELECT * FROM students ORDER BY student_id"
            )

            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row)

        except sqlite3.Error as err:
            messagebox.showerror(
                "Database Error",
                f"{err}"
            )


    def clear_fields(self):

        self.student_id.delete(0, tk.END)
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.course.delete(0, tk.END)
        self.enrollment_date.delete(0, tk.END)

        self.enrollment_date.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

    def on_tree_select(self, event):

        selected_item = self.tree.selection()

        if not selected_item:
            return

        values = self.tree.item(selected_item)["values"]

        self.clear_fields()

        self.student_id.insert(0, values[0])
        self.first_name.insert(0, values[1])
        self.last_name.insert(0, values[2])
        self.email.insert(0, values[3])
        self.phone.insert(0, values[4])
        self.course.insert(0, values[5])
        self.enrollment_date.insert(0, values[6])


# ================= MAIN =================
def main():
    root = tk.Tk()
    app = StudentEnrollmentSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()