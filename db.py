import os
import pymysql
import pymysql.cursors

CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", "1234"),

    "database": os.environ.get("MYSQL_DATABASE", "airline_db"),
}


def connect():
    return pymysql.connect(**CONFIG, cursorclass=pymysql.cursors.DictCursor)


def get_flights():
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT code, route, dep_time AS time, price, seats FROM flights ORDER BY code")
        return cur.fetchall()
    finally:
        conn.close()


def create_booking(pnr, name, age, flight_code, travel_class, fare):
    """Atomically decrement seats and insert booking. Returns False if sold out."""
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE flights SET seats = seats - 1 WHERE code = %s AND seats > 0", (flight_code,))
        if cur.rowcount == 0:
            conn.rollback()
            return False
        cur.execute(
            "INSERT INTO bookings (pnr, passenger_name, age, flight_code, travel_class, fare) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (pnr, name, age, flight_code, travel_class, fare),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def pnr_exists(pnr):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM bookings WHERE pnr = %s", (pnr,))
        return cur.fetchone() is not None
    finally:
        conn.close()


def get_booking(pnr):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT b.pnr, b.passenger_name AS name, b.age, b.flight_code AS flight, f.route, "
            "b.travel_class AS class, b.fare FROM bookings b JOIN flights f ON f.code = b.flight_code "
            "WHERE b.pnr = %s",
            (pnr,),
        )
        return cur.fetchone()
    finally:
        conn.close()


def cancel_booking(pnr):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT flight_code FROM bookings WHERE pnr = %s FOR UPDATE", (pnr,))
        row = cur.fetchone()
        if not row:
            conn.rollback()
            return False
        cur.execute("DELETE FROM bookings WHERE pnr = %s", (pnr,))
        cur.execute("UPDATE flights SET seats = seats + 1 WHERE code = %s", (row['flight_code'],))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
