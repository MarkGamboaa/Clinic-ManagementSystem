import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import database as db
from database import get_doctor_name

db.connect_db()

class ClinicManagementSystem:
    def __init__(self, window):
        self.window = window
        self.window.title("CLINIC MANAGEMENT SYSTEM")
        self.window.geometry("1000x600")

        tk.Label(window, text="Clinic Management System", font=("Arial", 20)).pack()
        self.frame = tk.Frame(self.window)
        self.frame.pack()

        tk.Button(self.frame, text="Patient", command=self.Patient).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Doctor", command=self.Doctor).grid(row=0, column=1, padx=5, pady=5)

        self.appointments = []  # List to store appointment details

    def clear_frame(self):
        """Clear all widgets from the frame."""
        for widget in self.frame.winfo_children():
            widget.destroy()

    def back_to_main(self):
        self.clear_frame()
        self.__init__(self.window)

    def Patient(self):
        self.clear_frame()
        tk.Label(self.frame, text="Patient").grid(row=0, column=0, padx=5, pady=5, columnspan=3)
        tk.Button(self.frame, text="Login", command=self.PatientLogIn).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.frame, text="Register", command=self.PatientRegister).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.back_to_main).grid(row=2, column=1, padx=5, pady=5)

    def Doctor(self):
        self.clear_frame()
        tk.Label(self.frame, text="Doctor").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Login", command=self.DoctorLogIn).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.back_to_main).grid(row=2, column=0, padx=5, pady=5)

    def PatientLogIn(self):
        self.clear_frame()

        tk.Label(self.frame, text="Username").grid(row=0, column=0, padx=5, pady=5)
        username_entry = tk.Entry(self.frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Password").grid(row=1, column=0, padx=5, pady=5)
        password_entry = tk.Entry(self.frame, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.frame, text="Login", command=lambda: self.Login(username_entry.get(), password_entry.get())).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.Patient).grid(row=2, column=1, padx=5, pady=5)

    def PatientRegister(self):
        self.clear_frame()

        tk.Label(self.frame, text="Username").grid(row=0, column=0, padx=5, pady=5)
        username_entry = tk.Entry(self.frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Password").grid(row=1, column=0, padx=5, pady=5)
        password_entry = tk.Entry(self.frame, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.frame, text="Register", command=lambda: self.Register(username_entry.get(), password_entry.get())).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.Patient).grid(row=2, column=1, padx=5, pady=5)

    def Register(self, username, password):
        if username and password:
            try:
                user_id = db.insert_user(username, password)
                messagebox.showinfo("Success", f"User registered successfully! Your ID is: {user_id}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def Login(self, username, password):
        if username and password:
            print(f"Attempting login for: {username}")  # Debugging output
            if db.validate_user(username, password):
                print("Login successful")  # Debugging output
                self.load_patient_dashboard(username)
            else:
                print("Login failed")  # Debugging output
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    def DoctorLogIn(self):
        self.clear_frame()

        tk.Label(self.frame, text="Username").grid(row=0, column=0, padx=5, pady=5)
        username_entry = tk.Entry(self.frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Password").grid(row=1, column=0, padx=5, pady=5)
        password_entry = tk.Entry(self.frame, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.frame, text="Login", command=lambda: self.DoctorLogin(username_entry.get(), password_entry.get())).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Back", command=self.Doctor).grid(row=2, column=1, padx=5, pady=5)

    def DoctorLogin(self, username, password):
        if username and password:
            if db.validate_doctor(username, password):  # Ensure this function exists in your database module
                self.load_doctor_dashboard(username)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    def load_patient_dashboard(self, username):
        self.clear_frame()
        tk.Label(self.frame, text=f"Welcome, {username}", font=("Arial", 20, "bold")).pack(pady=10)

        tk.Button(self.frame, text="Book Appointment", font=("Arial", 12, "bold"),
                  command=self.BookAppointment).pack(pady=5)
        tk.Button(self.frame, text="View Appointment", font=("Arial", 12, "bold"),
                  command=self.ViewAppointment).pack(pady=5)
        tk.Button(self.frame, text="Cancel Appointment", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.frame, text="View Medical Records", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.Patient).pack(pady=10)

    def BookAppointment(self):
        self.clear_frame()
        
        tk.Label(self.frame, text="Book Appointment", font=("Arial", 20, "bold")).pack(pady=10)

        tk.Label(self.frame, text="Patient Name:", font=("Arial", 12, "bold")).pack(anchor="w", padx=50)
        patient_name_entry = tk.Entry(self.frame, font=("Arial", 12), width=30)
        patient_name_entry.pack(pady=5)

        tk.Label(self.frame, text="Doctor:", font=("Arial", 12, "bold")).pack(anchor="w", padx=50)
        try:
            doctor_name = get_doctor_name()  # Fetch doctor name from the database
        except ValueError as e:
            doctor_name = "Unavailable"
            messagebox.showerror("Error", str(e))
        doctor_label = tk.Label(self.frame, text=doctor_name, font=("Arial", 12), bg="lightgray", width=28, anchor="w")
        doctor_label.pack(pady=5)

        tk.Label(self.frame, text="Date:", font=("Arial", 12, "bold")).pack(anchor="w", padx=50)
        date_entry = tk.Entry(self.frame, font=("Arial", 12), width=30)
        date_entry.pack(pady=5)

        tk.Label(self.frame, text="Time:", font=("Arial", 12, "bold")).pack(anchor="w", padx=50)
        time_entry = tk.Entry(self.frame, font=("Arial", 12), width=30)
        time_entry.pack(pady=5)

        tk.Button(self.frame, text="Submit", font=("Arial", 12, "bold"), command=lambda: self.submit_appointment(patient_name_entry.get(), date_entry.get(), time_entry.get())).pack(pady=10)
        tk.Button(self.frame, text="Back", font=("Arial", 12, "bold"), command=lambda: self.load_patient_dashboard("User")).pack(pady=5)

    def submit_appointment(self, patient_name, date, time):
        if patient_name and date and time:
            try:
                # Fetch the doctor's name dynamically
                doctor_name = get_doctor_name()
                if not doctor_name:
                    raise ValueError("No doctor available.")

                # Store the appointment
                appointment = {
                    "patient_name": patient_name,
                    "doctor_name": doctor_name,  # Use the fetched doctor name
                    "date": date,
                    "time": time
                }
                self.appointments.append(appointment)
                messagebox.showinfo("Success", f"Appointment booked for {patient_name} on {date} at {time} with {doctor_name}.")
                self.load_patient_dashboard(patient_name)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def ViewAppointment(self):
        self.clear_frame()
        tk.Label(self.frame, text="Your Appointments", font=("Arial", 20, "bold")).pack(pady=10)

        if not self.appointments:
            tk.Label(self.frame, text="No appointments found.", font=("Arial", 12)).pack(pady=5)
        else:
            for idx, appointment in enumerate(self.appointments, start=1):
                appointment_text = f"{idx}. {appointment['patient_name']} - {appointment['doctor_name']} on {appointment['date']} at {appointment['time']}"
                tk.Label(self.frame, text=appointment_text, font=("Arial", 12), anchor="w").pack(pady=2)

        tk.Button(self.frame, text="Back", font=("Arial", 12, "bold"), command=lambda: self.load_patient_dashboard("User")).pack(pady=10)

    def load_doctor_dashboard(self, username):
        self.clear_frame()
        tk.Label(self.frame, text=f"Welcome, Dr. {username}", font=("Arial", 20, "bold")).pack(pady=10)

        tk.Button(self.frame, text="View Appointments", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.frame, text="Manage Patients", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.frame, text="Medical Records", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.Doctor).pack(pady=10)

window = tk.Tk()
ClinicManagementSystem(window)
window.mainloop()
