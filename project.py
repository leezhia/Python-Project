from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time
import os


try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:

    canvas = None

try:
    conn = sqlite3.connect("medical_clinic.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        reason TEXT
    )
    """)


    cursor.execute("PRAGMA table_info(patients)")
    existing_columns = [column[1] for column in cursor.fetchall()]

    if "contact" not in existing_columns:
        cursor.execute("ALTER TABLE patients ADD COLUMN contact TEXT")
    if "address" not in existing_columns:
        cursor.execute("ALTER TABLE patients ADD COLUMN address TEXT")


    # Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor TEXT,
        date TEXT,
        time TEXT,
        status TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
    )
    """)

    # Billing Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS billing(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        amount REAL,
        status TEXT,
        date TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
    )
    """)
    conn.commit()
except sqlite3.Error as db_init_err:
    messagebox.showerror("Database Critical Error",
                         f"Failed to initialize SQLite structural files.\nDetails: {db_init_err}")



root = Tk()
root.title("POWERPUFF MEDICAL CLINIC SYSTEM")
root.geometry("1200x750")
root.config(bg="#fdfbf7")
root.resizable(False, False)

PATADYONG_RED = "green"
HOVER_ORANGE = "#d95d39"
WHITE = "#ffffff"
BG = "#fdfbf7"
GOLD_BTN = "#d49a17"
TEAL_GREEN = "#167a65"
CHARCOAL = "#2b2b2b"


def hover_in(e): e.widget['bg'] = HOVER_ORANGE


def hover_out(e): e.widget['bg'] = PATADYONG_RED



def hide_all_frames():
    try:
        dashboard_frame.pack_forget()
        patients_frame.pack_forget()
        appointments_frame.pack_forget()
        billing_frame.pack_forget()
        reports_frame.pack_forget()
        settings_frame.pack_forget()
        login_frame.pack_forget()
    except Exception as route_err:
        messagebox.showerror("UI Error", f"An error occurred while switching views: {route_err}")


def show_dashboard():
    hide_all_frames()
    refresh_dashboard_metrics()
    dashboard_frame.pack(fill=BOTH, expand=True)


def show_patients():
    hide_all_frames()
    refresh_patient_table()
    patients_frame.pack(fill=BOTH, expand=True)


def show_appointments():
    hide_all_frames()
    refresh_appointments_dropdowns()
    refresh_appointments_table()
    appointments_frame.pack(fill=BOTH, expand=True)


def show_billing():
    hide_all_frames()
    refresh_billing_dropdowns()
    refresh_billing_table()
    billing_frame.pack(fill=BOTH, expand=True)


def show_reports():
    hide_all_frames()
    calculate_and_render_reports()
    reports_frame.pack(fill=BOTH, expand=True)


def show_settings():
    hide_all_frames()
    settings_frame.pack(fill=BOTH, expand=True)

def toggle_password_visibility():
    if show_pass_var.get() == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="•")


def login_manager():
    try:
        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "password":
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            show_pass_var.set(0)
            password_entry.config(show="•")

            login_frame.pack_forget()
            sidebar.pack(side=LEFT, fill=Y)
            content_area.pack(side=RIGHT, fill=BOTH, expand=True)
            show_dashboard()
        else:
            messagebox.showerror("Access Denied", "Invalid Manager Username or Password.")
    except Exception as login_err:
        messagebox.showerror("Authentication Bug",
                             f"Failed handling entry objects.\nLocate: login_manager()\nDetails: {login_err}")


def logout_manager():
    hide_all_frames()
    sidebar.pack_forget()
    content_area.pack_forget()
    login_frame.pack(fill=BOTH, expand=True)

main_container = Frame(root, bg=BG)
main_container.pack(fill=BOTH, expand=True)

login_frame = Frame(main_container, bg=BG)
login_frame.pack(fill=BOTH, expand=True)

login_card = Frame(login_frame, bg=WHITE, highlightthickness=1, highlightbackground="#e2dcd5")
login_card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=480)

Label(login_card, text="❖\nPOWERPUFF CLINIC\nMANAGER PORTAL", font=("Arial", 18, "bold"), fg=PATADYONG_RED, bg=WHITE,
      justify="center").pack(pady=(30, 20))

Label(login_card, text="Username", font=("Arial", 11, "bold"), fg="#555", bg=WHITE).pack(anchor="w", padx=40)
username_entry = Entry(login_card, font=("Arial", 13), bg="#fcfaf7", relief=FLAT, highlightthickness=1,
                       highlightbackground="#ebdcd0")
username_entry.pack(fill=X, padx=40, ipady=8, pady=(5, 12))
username_entry.insert(0, "admin")

Label(login_card, text="Password", font=("Arial", 11, "bold"), fg="#555", bg=WHITE).pack(anchor="w", padx=40)
password_entry = Entry(login_card, font=("Arial", 13), show="•", bg="#fcfaf7", relief=FLAT, highlightthickness=1,
                       highlightbackground="#ebdcd0")
password_entry.pack(fill=X, padx=40, ipady=8, pady=(5, 5))
password_entry.insert(0, "password")

show_pass_var = IntVar()
show_pass_btn = Checkbutton(login_card, text="Show Password", variable=show_pass_var, onvalue=1, offvalue=0, bg=WHITE,
                            fg="#666", font=("Arial", 10), activebackground=WHITE, bd=0,
                            command=toggle_password_visibility)
show_pass_btn.pack(anchor="w", padx=40, pady=(0, 25))

Button(login_card, text="Secure Login", bg=PATADYONG_RED, fg="white", font=("Arial", 12, "bold"), bd=0, cursor="hand2",
       command=login_manager).pack(fill=X, padx=40, ipady=10)


sidebar = Frame(main_container, bg=PATADYONG_RED, width=280)

Label(sidebar, text="❖", font=("Arial", 28, "bold"), fg="white", bg=PATADYONG_RED).pack(pady=(35, 0))
Label(sidebar, text="POWERPUFF\nCLINIC", font=("Arial", 20, "bold"), fg="white", bg=PATADYONG_RED,
      justify="center").pack(pady=(5, 35))



def create_nav_btn(text, command):
    btn = Button(sidebar, text=text, bg=PATADYONG_RED, fg="white", font=("Arial", 14, "bold"), bd=0, cursor="hand2",
                 anchor="w", padx=35, command=command, activebackground=HOVER_ORANGE, activeforeground="white")
    btn.pack(fill=X, ipady=15)
    btn.bind("<Enter>", hover_in)
    btn.bind("<Leave>", hover_out)


create_nav_btn("⌂  Dashboard", show_dashboard)
create_nav_btn("👤  Patients", show_patients)
create_nav_btn("📅  Appointments", show_appointments)
create_nav_btn("💳  Billing", show_billing)
create_nav_btn("📊  Reports", show_reports)
create_nav_btn("⚙  Settings", show_settings)

Frame(sidebar, bg=PATADYONG_RED).pack(fill=BOTH, expand=True)
create_nav_btn("🚪  Logout", logout_manager)

content_area = Frame(main_container, bg=BG)
header = Frame(content_area, bg=WHITE, height=70)
header.pack(fill=X)

Label(header, text="POWERPUFF MEDICAL CLINIC", font=("Arial", 22, "bold"), bg=WHITE, fg=CHARCOAL).pack(side=LEFT,
                                                                                                              padx=30,
                                                                                                              pady=15)
clock_label = Label(header, font=("Arial", 12), bg=WHITE, fg="gray")
clock_label.pack(side=RIGHT, padx=30)


def update_clock():
    try:
        clock_label.config(text=time.strftime("%I:%M:%S %p"))
        root.after(1000, update_clock)
    except Exception:
        pass


update_clock()

page_container = Frame(content_area, bg=BG)
page_container.pack(fill=BOTH, expand=True)


def get_id_from_dropdown_string(selection_string):
    try:
        return int(selection_string.split(" - ")[0])
    except (ValueError, IndexError, AttributeError):
        return None

dashboard_frame = Frame(page_container, bg=BG)
Label(dashboard_frame, text="MANAGEMENT OVERVIEW", font=("Arial", 30, "bold"), bg=BG, fg=PATADYONG_RED).pack(pady=20)

cards_frame = Frame(dashboard_frame, bg=BG)
cards_frame.pack()

dash_cards = {}


def create_dash_card(parent, title, key):
    card = Frame(parent, bg=WHITE, width=220, height=140, highlightthickness=1, highlightbackground="#ebdcd0")
    card.pack(side=LEFT, padx=15)
    card.pack_propagate(False)
    Label(card, text=title, font=("Arial", 13), bg=WHITE, fg="gray").pack(pady=15)
    v_lbl = Label(card, text="0", font=("Arial", 28, "bold"), bg=WHITE, fg=TEAL_GREEN)
    v_lbl.pack()
    dash_cards[key] = v_lbl


create_dash_card(cards_frame, "Total Patients", "patients")
create_dash_card(cards_frame, "Appointments", "appointments")
create_dash_card(cards_frame, "Total Revenue", "revenue")
create_dash_card(cards_frame, "Pending Bills", "pending_bills")


def refresh_dashboard_metrics():
    try:
        cursor.execute("SELECT COUNT(*) FROM patients")
        dash_cards["patients"].config(text=str(cursor.fetchone()[0]))

        cursor.execute("SELECT COUNT(*) FROM appointments")
        dash_cards["appointments"].config(text=str(cursor.fetchone()[0]))

        cursor.execute("SELECT SUM(amount) FROM billing WHERE status='Paid'")
        rev = cursor.fetchone()[0]
        dash_cards["revenue"].config(text=f"${rev:,.2f}" if rev else "₱0.00")

        cursor.execute("SELECT COUNT(*) FROM billing WHERE status='Unpaid'")
        dash_cards["pending_bills"].config(text=str(cursor.fetchone()[0]))
    except sqlite3.Error as db_err:
        messagebox.showerror("Metrics Error", f"Could not sync real-time dashboard data.\nDetails: {db_err}")

patients_frame = Frame(page_container, bg=BG)
Label(patients_frame, text="PATIENT REGISTRY & DISPATCH CENTER", font=("Arial", 24, "bold"), bg=BG,
      fg=PATADYONG_RED).pack(pady=10)

p_content = Frame(patients_frame, bg=BG)
p_content.pack(fill=BOTH, expand=True, padx=20, pady=(5, 15))

p_left_panel = Frame(p_content, bg=BG, width=340)
p_left_panel.pack(side=LEFT, fill=Y, padx=(0, 15))
p_left_panel.pack_propagate(False)

p_form = Frame(p_left_panel, bg=WHITE, highlightthickness=1, highlightbackground="#ebdcd0")
p_form.pack(side=TOP, fill=X, ipady=2)

Label(p_form, text="Add New Patient Profile", font=("Arial", 11, "bold"), bg=WHITE, fg=CHARCOAL).pack(anchor="w",
                                                                                                      padx=15,
                                                                                                      pady=(4, 1))

p_fields = [
    ("Patient Fullname", "name"),
    ("Contact No.", "contact"),
    ("Address", "address"),
    ("Age", "age"),
    ("Medical Reason", "reason")
]
p_entries = {}

for label_text, key in p_fields:
    Label(p_form, text=label_text, bg=WHITE, fg="#555", font=("Arial", 8, "bold")).pack(anchor="w", padx=15,
                                                                                        pady=(0, 0))
    entry = Entry(p_form, font=("Arial", 9), bg="#fcfaf7", relief=FLAT, highlightthickness=1,
                  highlightbackground="#ebdcd0")
    entry.pack(fill=X, ipady=1, padx=15, pady=(1, 1))
    p_entries[key] = entry


def clear_patient_form():
    for ent in p_entries.values(): ent.delete(0, END)


def refresh_patient_table():
    try:
        for row in p_tree.get_children(): p_tree.delete(row)
        cursor.execute("SELECT id, name, contact, address, age, reason FROM patients")
        for row in cursor.fetchall(): p_tree.insert("", END, values=row)
    except sqlite3.Error as db_err:
        messagebox.showerror("Database View Error", f"Failed fetching patient registry table rows.\nDetails: {db_err}")


def register_patient():
    try:
        data = {k: v.get().strip() for k, v in p_entries.items()}


        if not data["name"] or not data["contact"]:
            messagebox.showerror("Validation Error", "Name and Contact variables are required entries.")
            return


        validation_errors = []


        if not data["contact"].isdigit():
            validation_errors.append("Contact Number must contain numbers only.")


        if data["age"] and not data["age"].isdigit():
            validation_errors.append("Age must be a valid whole number value.")


        if validation_errors:
            error_message = "The following data type exceptions were detected:\n\n" + "\n".join(validation_errors)
            messagebox.showerror("Data Type Exception", error_message)
            return


        cursor.execute("INSERT INTO patients(name, contact, address, age, reason) VALUES(?,?,?,?,?)",
                       (data["name"], data["contact"], data["address"], data["age"], data["reason"]))
        conn.commit()
        messagebox.showinfo("Success", "New Patient profile initialized successfully.")
        clear_patient_form()
        refresh_patient_table()
    except sqlite3.Error as db_err:
        messagebox.showerror("Execution Fault", f"Database rejected adding patient execution line.\nDetails: {db_err}")


def delete_patient():
    try:
        selected = p_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient record from the table list first.")
            return
        pid = p_tree.item(selected)['values'][0]
        cursor.execute("DELETE FROM patients WHERE id=?", (pid,))
        conn.commit()
        messagebox.showinfo("Deleted", "Patient record securely wiped from active system.")
        refresh_patient_table()
    except sqlite3.Error as db_err:
        messagebox.showerror("Purge Fault", f"Could not detach chosen database asset record line.\nDetails: {db_err}")


p_btn_frame = Frame(p_form, bg=WHITE)
p_btn_frame.pack(fill=X, padx=15, pady=(3, 3))
Button(p_btn_frame, text="Register", bg=GOLD_BTN, fg="white", font=("Arial", 8, "bold"), bd=0, width=8,
       command=register_patient).pack(side=LEFT, padx=2)
Button(p_btn_frame, text="Delete", bg=PATADYONG_RED, fg="white", font=("Arial", 8, "bold"), bd=0, width=8,
       command=delete_patient).pack(side=LEFT, padx=2)
Button(p_btn_frame, text="Clear", bg=TEAL_GREEN, fg="white", font=("Arial", 8, "bold"), bd=0, width=8,
       command=clear_patient_form).pack(side=LEFT, padx=2)

p_dispatcher = Frame(p_left_panel, bg=WHITE, highlightthickness=1, highlightbackground="#ebdcd0")
p_dispatcher.pack(side=TOP, fill=X, pady=(8, 0), ipady=2)

Label(p_dispatcher, text="⚡ Patient Communications Portal", font=("Arial", 11, "bold"), bg=WHITE,
      fg=PATADYONG_RED).pack(anchor="w", padx=15, pady=(4, 1))
Label(p_dispatcher, text="Select a patient from the table list to begin.", font=("Arial", 8, "italic"), bg=WHITE,
      fg="gray").pack(anchor="w", padx=15, pady=(0, 2))

Label(p_dispatcher, text="Target Recipient:", bg=WHITE, fg="#555", font=("Arial", 8, "bold")).pack(anchor="w", padx=15)
msg_target_lbl = Label(p_dispatcher, text="None Selected", font=("Arial", 9, "bold"), bg="#fcfaf7", fg=TEAL_GREEN,
                       anchor="w", highlightthickness=1, highlightbackground="#ebdcd0")
msg_target_lbl.pack(fill=X, padx=15, ipady=2, pady=1)

Label(p_dispatcher, text="Select Notification Template:", bg=WHITE, fg="#555", font=("Arial", 8, "bold")).pack(
    anchor="w", padx=15, pady=(1, 0))


def apply_sms_template(event):
    selected_template = template_combobox.get()
    patient_name = msg_target_lbl.cget("text").split(" (")[0]
    if patient_name == "None Selected":
        patient_name = "[Patient Name]"

    if selected_template == "Appointment Approaching":
        msg_text.delete("1.0", END)
        msg_text.insert("1.0",
                        f"Good day {patient_name}, this is Powerpuff Clinic. This is a friendly reminder that your upcoming appointment with us is approaching. Please arrive 15 minutes before your slot. Thank you!")
    elif selected_template == "Medical Results Ready":
        msg_text.delete("1.0", END)
        msg_text.insert("1.0",
                        f"Hello {patient_name}, this is Powerpuff Clinic. Your diagnostic lab results/records are now ready for pickup. You may visit the clinic during business hours. Keep safe!")
    elif selected_template == "Custom Empty Message":
        msg_text.delete("1.0", END)


template_combobox = ttk.Combobox(p_dispatcher,
                                 values=["Appointment Approaching", "Medical Results Ready", "Custom Empty Message"],
                                 font=("Arial", 9), state="readonly")
template_combobox.pack(fill=X, padx=15, pady=2)
template_combobox.bind("<<ComboboxSelected>>", apply_sms_template)

Label(p_dispatcher, text="Message Body Box:", bg=WHITE, fg="#555", font=("Arial", 8, "bold")).pack(anchor="w", padx=15,
                                                                                                   pady=(1, 0))
msg_text = Text(p_dispatcher, font=("Arial", 9), bg="#fcfaf7", height=2, relief=FLAT, highlightthickness=1,
                highlightbackground="#ebdcd0")
msg_text.pack(fill=X, padx=15, pady=2)


def transmit_patient_sms():
    target_info = msg_target_lbl.cget("text")
    message_content = msg_text.get("1.0", END).strip()

    if target_info == "None Selected":
        messagebox.showwarning("Dispatch Cancelled",
                               "Please click/select a patient from the right registry table list first.")
        return
    if not message_content:
        messagebox.showwarning("Dispatch Cancelled", "The communication body field cannot be empty.")
        return

    phone_number = target_info.split("(")[1].replace(")", "") if "(" in target_info else "Unknown"
    patient_name = target_info.split(" (")[0]

    print(f"\n[NETWORK TELEMETRY] Initializing cellular handshake link...")
    print(f"[GATEWAY DISPATCH] Target: {phone_number} ({patient_name})")
    print(f"[MESSAGE BODY] -> {message_content}")
    print(f"[STATUS] 200 OK - SMS successfully routed via GSM network array.\n")

    messagebox.showinfo("SMS Dispatched Successfully",
                        f"Notification alert sent to {patient_name} via registration channel ({phone_number}).")
    msg_text.delete("1.0", END)
    template_combobox.set('')


Button(p_dispatcher, text="✉ Dispatch Live SMS Alert", bg=PATADYONG_RED, fg="white", font=("Arial", 10, "bold"), bd=0,
       cursor="hand2", command=transmit_patient_sms).pack(fill=X, padx=15, ipady=4, pady=4)

p_table_frame = Frame(p_content, bg=WHITE, highlightthickness=1, highlightbackground="#ebdcd0")
p_table_frame.pack(side=RIGHT, fill=BOTH, expand=True)

p_scroll = Scrollbar(p_table_frame)
p_scroll.pack(side=RIGHT, fill=Y)

p_tree = ttk.Treeview(p_table_frame,
                      columns=("ID", "Patient Fullname", "Contact No.", "Address", "Age", "Medical Reason"),
                      show="headings", yscrollcommand=p_scroll.set)
p_scroll.config(command=p_tree.yview)

p_tree.heading("ID", text="ID")
p_tree.column("ID", width=40, anchor="center")

p_tree.heading("Patient Fullname", text="Patient Fullname")
p_tree.column("Patient Fullname", width=140, anchor="w")

p_tree.heading("Contact No.", text="Contact No.")
p_tree.column("Contact No.", width=105, anchor="center")

p_tree.heading("Address", text="Address")
p_tree.column("Address", width=130, anchor="w")

p_tree.heading("Age", text="Age")
p_tree.column("Age", width=45, anchor="center")

p_tree.heading("Medical Reason", text="Medical Reason")
p_tree.column("Medical Reason", width=150, anchor="w")

p_tree.pack(fill=BOTH, expand=True, padx=8, pady=8)


def on_patient_row_select(event):
    selected_items = p_tree.selection()
    if selected_items:
        item_data = p_tree.item(selected_items[0])['values']
        p_name = item_data[1]
        p_contact = item_data[2]
        msg_target_lbl.config(text=f"{p_name} ({p_contact})")
        apply_sms_template(None)


p_tree.bind("<<TreeviewSelect>>", on_patient_row_select)



appointments_frame = Frame(page_container, bg=BG)
Label(appointments_frame, text="APPOINTMENT SCHEDULER", font=("Arial", 24, "bold"), bg=BG, fg=PATADYONG_RED).pack(
    pady=15)

a_content = Frame(appointments_frame, bg=BG)
a_content.pack(fill=BOTH, expand=True, padx=20)

a_form = Frame(a_content, bg=WHITE, width=400, highlightthickness=1, highlightbackground="#ebdcd0")
a_form.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
a_form.pack_propagate(False)

Label(a_form, text="Book Appointment Slot", font=("Arial", 16, "bold"), bg=WHITE, fg=CHARCOAL).pack(anchor="w", padx=25,
                                                                                                    pady=15)

Label(a_form, text="Select Patient Profile Link", bg=WHITE, fg="#555", font=("Arial", 10, "bold")).pack(anchor="w",
                                                                                                        padx=25, pady=5)
a_patient_var = StringVar()
a_patient_drop = ttk.Combobox(a_form, textvariable=a_patient_var, font=("Arial", 11), state="readonly")
a_patient_drop.pack(fill=X, padx=25, pady=5)

Label(a_form, text="Assigned Practitioner / Doctor", bg=WHITE, fg="#555", font=("Arial", 10, "bold")).pack(anchor="w",
                                                                                                           padx=25,
                                                                                                           pady=5)
a_doc_var = StringVar()
a_doc_drop = ttk.Combobox(a_form, textvariable=a_doc_var,
                          values=["Dr. Balestramon (Pediatrics)", "Dr. Ogatis (Psychiatry)", "Dr. Ortega (Orthopedics)",
                                  "Dr. Pepino (General Medicine)"], font=("Arial", 11), state="readonly")
a_doc_drop.pack(fill=X, padx=25, pady=5)

Label(a_form, text="Appointment Date (YYYY-MM-DD)", bg=WHITE, fg="#555", font=("Arial", 10, "bold")).pack(anchor="w",
                                                                                                          padx=25,
                                                                                                          pady=5)
a_date_ent = Entry(a_form, font=("Arial", 11), bg="#fcfaf7", relief=FLAT, highlightthickness=1,
                   highlightbackground="#ebdcd0")
a_date_ent.pack(fill=X, ipady=6, padx=25, pady=5)
a_date_ent.insert(0, time.strftime("%Y-%m-%d"))

Label(a_form, text="Appointment Time Window", bg=WHITE, fg="#555", font=("Arial", 10, "bold")).pack(anchor="w", padx=25,
                                                                                                    pady=5)
a_time_ent = Entry(a_form, font=("Arial", 11), bg="#fcfaf7", relief=FLAT, highlightthickness=1,
                   highlightbackground="#ebdcd0")
a_time_ent.pack(fill=X, ipady=6, padx=25, pady=5)
a_time_ent.insert(0, "10:00 AM")

Label(a_form, text="Current Allocation Status", bg=WHITE, fg="#555", font=("Arial", 10, "bold")).pack(anchor="w",
                                                                                                      padx=25, pady=5)
a_status_var = StringVar()
a_status_drop = ttk.Combobox(a_form, textvariable=a_status_var, values=["Scheduled", "Completed", "Cancelled"],
                             font=("Arial", 11), state="readonly")
a_status_drop.current(0)
a_status_drop.pack(fill=X, padx=25, pady=5)


def refresh_appointments_dropdowns():
    try:
        cursor.execute("SELECT id, name FROM patients")
        a_patient_drop['values'] = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
    except sqlite3.Error as db_err:
        messagebox.showerror("Menu Link Fail", f"Dropdown caught database tracking break.\nDetails: {db_err}")


def refresh_appointments_table():
    try:
        for row in a_tree.get_children(): a_tree.delete(row)
        cursor.execute("""
            SELECT appointments.id, patients.name, appointments.doctor, appointments.date, appointments.time, appointments.status 
            FROM appointments JOIN patients ON appointments.patient_id = patients.id
        """)
        for row in cursor.fetchall(): a_tree.insert("", END, values=row)
    except sqlite3.Error as db_err:
        messagebox.showerror("Fetch Fail",
                             f"Join statement error occurred inside Appointment table.\nDetails: {db_err}")


def schedule_appointment():
    try:
        p_sel = a_patient_var.get()
        doc = a_doc_var.get()
        dt = a_date_ent.get().strip()
        tm = a_time_ent.get().strip()
        stat = a_status_var.get()

        pid = get_id_from_dropdown_string(p_sel)
        if not pid or not doc or not dt:
            messagebox.showerror("Error", "Please complete all fields to safely log an appointment mapping.")
            return

        cursor.execute("INSERT INTO appointments(patient_id, doctor, date, time, status) VALUES(?,?,?,?,?)",
                       (pid, doc, dt, tm, stat))
        conn.commit()
        messagebox.showinfo("Scheduled", "Appointment successfully verified and scheduled.")
        refresh_appointments_table()
    except sqlite3.Error as db_err:
        messagebox.showerror("Scheduling Exception",
                             f"Database rejected recording transaction save.\nDetails: {db_err}")


def cancel_appointment():
    try:
        selected = a_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select scheduled row appointment record to remove.")
            return
        aid = a_tree.item(selected)['values'][0]
        cursor.execute("DELETE FROM appointments WHERE id=?", (aid,))
        conn.commit()
        messagebox.showinfo("Removed", "Appointment block successfully detached.")
        refresh_appointments_table()
    except sqlite3.Error as db_err:
        messagebox.showerror("Query Failure",
                             f"Could not clear selected appointment execution line.\nDetails: {db_err}")


a_btn_frame = Frame(a_form, bg=WHITE)
a_btn_frame.pack(fill=X, padx=25, pady=15)
Button(a_btn_frame, text="Schedule Slot", bg=GOLD_BTN, fg="white", font=("Arial", 11, "bold"), bd=0, padx=10, pady=5,
       command=schedule_appointment).pack(side=LEFT, padx=5)
Button(a_btn_frame, text="Remove Slot", bg=PATADYONG_RED, fg="white", font=("Arial", 11, "bold"), bd=0, padx=10, pady=5,
       command=cancel_appointment).pack(side=LEFT, padx=5)

a_table_frame = Frame(a_content, bg=WHITE)
a_table_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

a_tree = ttk.Treeview(a_table_frame, columns=("AppID", "Patient", "Doctor", "Date", "Time", "Status"), show="headings")
for col in ("AppID", "Patient", "Doctor", "Date", "Time", "Status"): a_tree.heading(col, text=col); a_tree.column(col,
                                                                                                                  width=95)
a_tree.pack(fill=BOTH, expand=True, padx=15, pady=15)



billing_frame = Frame(page_container, bg=BG)
Label(billing_frame, text="BILLING & INVOICES", font=("Arial", 24, "bold"), bg=BG, fg=PATADYONG_RED).pack(pady=15)

b_content = Frame(billing_frame, bg=BG)
b_content.pack(fill=BOTH, expand=True, padx=20)

b_form = Frame(b_content, bg=WHITE, width=400, highlightthickness=1, highlightbackground="#ebdcd0")
b_form.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
b_form.pack_propagate(False)

Label(b_form, text="Create New Invoice", font=("Arial", 16, "bold"), bg=WHITE, fg=CHARCOAL).pack(anchor="w", padx=25,
                                                                                                 pady=15)

Label(b_form, text="Link Account Profile", bg=WHITE, fg="#555", font=("Arial", 10, "bold")).pack(anchor="w", padx=25,
                                                                                                 pady=5)
b_patient_var = StringVar()
b_patient_drop = ttk.Combobox(b_form, textvariable=b_patient_var, font=("Arial", 11), state="readonly")
b_patient_drop.pack(fill=X, padx=25, pady=5)

Label(b_form, text="Statement Amount Fee (₱)", bg=WHITE, fg="#555", font=("Arial", 10, "bold")).pack(anchor="w",
                                                                                                     padx=25, pady=5)
b_amt_ent = Entry(b_form, font=("Arial", 11), bg="#fcfaf7", relief=FLAT, highlightthickness=1,
                  highlightbackground="#ebdcd0")
b_amt_ent.pack(fill=X, ipady=6, padx=25, pady=5)

Label(b_form, text="Payment Status Lifecycle", bg=WHITE, fg="#555", font=("Arial", 10, "bold")).pack(anchor="w",
                                                                                                     padx=25, pady=5)
b_status_var = StringVar()
b_status_drop = ttk.Combobox(b_form, textvariable=b_status_var, values=["Unpaid", "Paid"], font=("Arial", 11),
                             state="readonly")
b_status_drop.current(0)
b_status_drop.pack(fill=X, padx=25, pady=5)


def refresh_billing_dropdowns():
    try:
        cursor.execute("SELECT id, name FROM patients")
        b_patient_drop['values'] = [f"{r[0]} - {r[1]}" for r in cursor.fetchall()]
    except sqlite3.Error as db_err:
        messagebox.showerror("Sync Error", f"Failed parsing database records into drop menu.\nDetails: {db_err}")


def refresh_billing_table():
    try:
        for row in b_tree.get_children(): b_tree.delete(row)
        cursor.execute("""
            SELECT billing.id, patients.name, billing.amount, billing.status, billing.date 
            FROM billing JOIN patients ON billing.patient_id = patients.id
        """)
        for row in cursor.fetchall(): b_tree.insert("", END, values=row)
    except sqlite3.Error as db_err:
        messagebox.showerror("Fetch Fail", f"Error refreshing billing module entries.\nDetails: {db_err}")


def create_invoice():
    try:
        p_sel = b_patient_var.get()
        amt = b_amt_ent.get().strip()
        stat = b_status_var.get()
        dt = time.strftime("%Y-%m-%d")

        pid = get_id_from_dropdown_string(p_sel)
        if not pid or not amt:
            messagebox.showerror("Error", "Please make sure to link a patient profile and input an exact amount.")
            return

        cursor.execute("INSERT INTO billing(patient_id, amount, status, date) VALUES(?,?,?,?)",
                       (pid, float(amt), stat, dt))
        conn.commit()
        messagebox.showinfo("Success", "Invoice registered successfully.")
        b_amt_ent.delete(0, END)
        refresh_billing_table()
    except ValueError:
        messagebox.showerror("Format Exception", "Please enter a valid numeric value for the billing amount fee.")
    except sqlite3.Error as db_err:
        messagebox.showerror("Database Rejection", f"Failed to record invoice execution line.\nDetails: {db_err}")


def print_pdf_receipt():
    if not canvas:
        messagebox.showerror("Dependency Error", "ReportLab library not detected in local runtime environmental files.")
        return
    try:
        selected = b_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please highlight/select an invoice line item entry row first.")
            return

        row_vals = b_tree.item(selected)['values']
        inv_id, p_name, amt, stat, dt = row_vals

        filename = f"Invoice_{inv_id}.pdf"
        pdf = canvas.Canvas(filename, pagesize=letter)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(100, 750, "POWERPUFF MEDICAL CLINIC INVOICE")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 720, f"Invoice ID Reference: {inv_id}")
        pdf.drawString(100, 700, f"Issued Date Timeline: {dt}")
        pdf.drawString(100, 680, f"Patient Registered Account: {p_name}")
        pdf.drawString(100, 660, f"Total Assessed Statement Value: ${float(amt):,.2f}")
        pdf.drawString(100, 640, f"Transaction Clearance Status: {stat}")
        pdf.drawString(100, 600, "Thank you for trusting Powerpuff Medical Clinic.")
        pdf.showPage()
        pdf.save()

        messagebox.showinfo("PDF Generated", f"Invoice safely compiled to root directory as: {filename}")
    except Exception as pdf_err:
        messagebox.showerror("PDF Compile Error", f"Dynamic printing generation engine failed.\nDetails: {pdf_err}")


b_btn_frame = Frame(b_form, bg=WHITE)
b_btn_frame.pack(fill=X, padx=25, pady=15)
Button(b_btn_frame, text="Log Invoice", bg=GOLD_BTN, fg="white", font=("Arial", 11, "bold"), bd=0, padx=10, pady=5,
       command=create_invoice).pack(side=LEFT, padx=5)
Button(b_btn_frame, text="🖨 Export PDF", bg=TEAL_GREEN, fg="white", font=("Arial", 11, "bold"), bd=0, padx=10, pady=5,
       command=print_pdf_receipt).pack(side=LEFT, padx=5)

b_table_frame = Frame(b_content, bg=WHITE)
b_table_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

b_tree = ttk.Treeview(b_table_frame, columns=("InvID", "Patient Account", "Statement Amount", "Status", "Date"),
                      show="headings")
for col in ("InvID", "Patient Account", "Statement Amount", "Status", "Date"): b_tree.heading(col,
                                                                                              text=col); b_tree.column(
    col, width=110)
b_tree.pack(fill=BOTH, expand=True, padx=15, pady=15)


reports_frame = Frame(page_container, bg=BG)
Label(reports_frame, text="CLINICAL ANALYTICS REPORTS", font=("Arial", 24, "bold"), bg=BG, fg=PATADYONG_RED).pack(
    pady=20)

rep_content = Frame(reports_frame, bg=WHITE, highlightthickness=1, highlightbackground="#ebdcd0")
rep_content.pack(fill=BOTH, expand=True, padx=40, pady=20)

rep_text = Text(rep_content, font=("Courier New", 12), bg="#fcfaf7", bd=0, state=DISABLED)
rep_text.pack(fill=BOTH, expand=True, padx=20, pady=20)


def calculate_and_render_reports():
    try:
        cursor.execute("SELECT COUNT(*) FROM patients")
        t_patients = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM appointments WHERE status='Scheduled'")
        active_app = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(amount) FROM billing WHERE status='Paid'")
        total_rev = cursor.fetchone()[0] or 0.0

        cursor.execute("SELECT SUM(amount) FROM billing WHERE status='Unpaid'")
        unpaid_rev = cursor.fetchone()[0] or 0.0

        report_summary = f"""
============================================================
           POWERPUFF MEDICAL CLINIC ANALYTICS
              GENERATED TIMELINE: {time.strftime("%Y-%m-%d %I:%M:%S %p")}
============================================================

 [1] REGISTRY DEMOGRAPHICS METRICS
     - Cumulative Registered Patients Base Profile Count: {t_patients}

 [2] OUTPATIENT SCHEDULER MATRIX TELEMETRY
     - Total Active Line Scheduled Appointments Queue  : {active_app}

 [3] FINANCIAL LEDGER BALANCE METRICS
     - Total Settled Realized Liquid Revenue Asset Pipeline : ₱{total_rev:,.2f}
     - Outstanding Unsettled Account Receivable Values     : ₱{unpaid_rev:,.2f}

============================================================
              END OF DATA TRANSACTION LOG
============================================================
"""
        rep_text.config(state=NORMAL)
        rep_text.delete("1.0", END)
        rep_text.insert("1.0", report_summary)
        rep_text.config(state=DISABLED)
    except sqlite3.Error as rep_err:
        messagebox.showerror("Analytics Failure",
                             f"Failed parsing database records for generation engine.\nDetails: {rep_err}")




settings_frame = Frame(page_container, bg=BG)
Label(settings_frame, text="SYSTEM CORE CONFIGURATIONS", font=("Arial", 24, "bold"), bg=BG, fg=PATADYONG_RED).pack(
    pady=20)

set_content = Frame(settings_frame, bg=WHITE, highlightthickness=1, highlightbackground="#ebdcd0")
set_content.pack(fill=BOTH, expand=True, padx=50, pady=30)

Label(set_content, text="Admin Security Engine Access Key Configuration", font=("Arial", 14, "bold"), bg=WHITE,
      fg=CHARCOAL).pack(anchor="w", padx=30, pady=(30, 10))


def purge_entire_database():
    confirm = messagebox.askyesno("CRITICAL SYSTEM OVERRIDE REQUEST",
                                  "Are you sure you want to securely format all structural databases?\nThis action clears all patients, bookings, and receipts permanently.")
    if confirm:
        try:
            cursor.execute("DROP TABLE IF EXISTS patients")
            cursor.execute("DROP TABLE IF EXISTS appointments")
            cursor.execute("DROP TABLE IF EXISTS billing")
            conn.commit()
            messagebox.showinfo("Database Formatted",
                                "Structural files deleted. Re-launch system environment variables to generate clean assets.")
            root.destroy()
        except sqlite3.Error as purge_err:
            messagebox.showerror("Override Fault",
                                 f"Database engine rejected raw sector formatting execution trace.\nDetails: {purge_err}")


Button(set_content, text="⚠ DELETE DATA", bg=PATADYONG_RED, fg=WHITE,
       font=("Arial", 12, "bold"), bd=0, padx=20, pady=10, command=purge_entire_database).pack(anchor="w", padx=30,
                                                                                               pady=20)

hide_all_frames()
login_frame.pack(fill=BOTH, expand=True)

root.mainloop()