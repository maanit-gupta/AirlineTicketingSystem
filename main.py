import tkinter as tk
from tkinter import messagebox
import random
import string
import db

flights = []
BUSINESS_SURCHARGE = 80

def refresh_flights():
    global flights
    flights = db.get_flights()
    flight_listbox.delete(0, tk.END)
    for f in flights:
        flight_listbox.insert(tk.END, f"{f['code']} | {f['route']} | Dep: {f['time']} | Base: ${f['price']} | Seats: {f['seats']}")

def book_ticket():
    selected = flight_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select a flight from the list.")
        return

    name = name_entry.get().strip()
    age_str = age_entry.get().strip()
    travel_class = class_var.get()

    if not name:
        messagebox.showerror("Error", "Please enter passenger name.")
        return

    if not age_str.isdigit() or int(age_str) <= 0:
        messagebox.showerror("Error", "Please enter a valid positive age.")
        return

    flight = flights[selected[0]]
    if flight["seats"] <= 0:
        messagebox.showerror("Unavailable", "No seats available on this flight.")
        return

    pnr = "".join(random.choices(string.ascii_uppercase, k=6))
    while db.pnr_exists(pnr):
        pnr = "".join(random.choices(string.ascii_uppercase, k=6))

    fare = flight["price"] + (BUSINESS_SURCHARGE if travel_class == "Business" else 0)
    if not db.create_booking(pnr, name, int(age_str), flight["code"], travel_class, fare):
        refresh_flights()
        messagebox.showerror("Unavailable", "No seats available on this flight.")
        return

    refresh_flights()
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    messagebox.showinfo("Booking Confirmed", f"Ticket booked successfully!\nPNR: {pnr}\nTotal Fare: ${fare}")

def view_booking():
    pnr = pnr_entry.get().strip().upper()
    if not pnr:
        messagebox.showerror("Error", "Please enter a PNR.")
        return

    b = db.get_booking(pnr)
    if not b:
        messagebox.showerror("Not Found", f"No booking found for PNR: {pnr}")
        return

    details = f"PNR: {pnr}\nPassenger: {b['name']} (Age: {b['age']})\nFlight: {b['flight']} ({b['route']})\nClass: {b['class']}\nTotal Fare: ${b['fare']}"
    messagebox.showinfo("Booking Details", details)

def cancel_ticket():
    pnr = pnr_entry.get().strip().upper()
    if not pnr:
        messagebox.showerror("Error", "Please enter a PNR.")
        return

    b = db.get_booking(pnr)
    if not b:
        messagebox.showerror("Not Found", f"No booking found for PNR: {pnr}")
        return

    db.cancel_booking(pnr)
    refresh_flights()
    pnr_entry.delete(0, tk.END)
    messagebox.showinfo("Cancelled", f"Booking with PNR {pnr} has been cancelled.")

root = tk.Tk()
root.title("Airline Ticketing System")
root.geometry("560x500")

tk.Label(root, text="Available Flights").pack(anchor="w", padx=10, pady=(10, 2))
flight_listbox = tk.Listbox(root, width=70, height=6)
flight_listbox.pack(padx=10, fill="x")

book_frame = tk.LabelFrame(root, text="Passenger Details & Booking", padx=10, pady=8)
book_frame.pack(padx=10, pady=10, fill="x")

tk.Label(book_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=2)
name_entry = tk.Entry(book_frame, width=25)
name_entry.grid(row=0, column=1, sticky="w", pady=2)

tk.Label(book_frame, text="Age:").grid(row=1, column=0, sticky="w", pady=2)
age_entry = tk.Entry(book_frame, width=10)
age_entry.grid(row=1, column=1, sticky="w", pady=2)

tk.Label(book_frame, text="Class:").grid(row=2, column=0, sticky="w", pady=2)
class_var = tk.StringVar(value="Economy")
tk.Radiobutton(book_frame, text="Economy", variable=class_var, value="Economy").grid(row=2, column=1, sticky="w")
tk.Radiobutton(book_frame, text="Business (+ $80)", variable=class_var, value="Business").grid(row=2, column=1, padx=(90, 0), sticky="w")

tk.Button(book_frame, text="Book Ticket", command=book_ticket).grid(row=3, column=0, columnspan=2, pady=(8, 2))

manage_frame = tk.LabelFrame(root, text="Manage Booking", padx=10, pady=8)
manage_frame.pack(padx=10, pady=5, fill="x")

tk.Label(manage_frame, text="Enter PNR:").grid(row=0, column=0, sticky="w")
pnr_entry = tk.Entry(manage_frame, width=15)
pnr_entry.grid(row=0, column=1, padx=5, sticky="w")

tk.Button(manage_frame, text="View Booking", command=view_booking).grid(row=0, column=2, padx=5)
tk.Button(manage_frame, text="Cancel Ticket", command=cancel_ticket).grid(row=0, column=3, padx=5)

refresh_flights()

if __name__ == "__main__":
    root.mainloop()
