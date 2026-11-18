# Airline Ticketing System

A simple desktop airline ticketing and booking application built with Python Tkinter and MySQL.

## Features

- **Browse Flights**: View available flights, routes, departure times, fares, and real-time seat availability.
- **Book Tickets**: Reserve seats with passenger details, select Economy or Business class, and receive an auto-generated 6-character PNR.
- **Manage Bookings**: Look up booking details using PNR.
- **Cancel Bookings**: Cancel existing reservations and automatically restore available seat counts.

## Prerequisites

- Python 3.8+
- MySQL Server

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/maanit-gupta/AirlineTicketingSystem.git
   cd AirlineTicketingSystem
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the Database:**
   Import `schema.sql` into your MySQL server:
   ```bash
   mysql -u root -p < schema.sql
   ```

4. **Database Configuration:**
   By default, the application connects to `localhost` with user `root`, database `airline_db`. You can customize database connection settings using environment variables:
   - `MYSQL_HOST` (default: `localhost`)
   - `MYSQL_USER` (default: `root`)
   - `MYSQL_PASSWORD` (default: `1234`)
   - `MYSQL_DATABASE` (default: `airline_db`)

5. **Run the Application:**
   ```bash
   python main.py
   ```
