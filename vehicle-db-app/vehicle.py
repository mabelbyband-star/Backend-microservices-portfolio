import psycopg2
import time
from fastapi import FastAPI

app = FastAPI()

class Vehicle:
    def __init__(self):
      self.color = "Factory white"
      self.added_upgrades = []
      self.brand = input("Write the brand you want; TESLA, FORD, TOYOTA: ").upper()
      if self.brand == "TESLA":
        self.model = input("Write the Tesla model you want; MODEL 3, MODEL Y: ").upper()
      elif self.brand == "FORD":
        self.model = input("Write the Ford model you want; MUSTANG, F150: ").upper()
      elif self.brand == "TOYOTA":
        self.model = input("Write the Toyota model you want; RUNNER, PRIUS: ").upper()
      else:
        print("Write a correct brand.")
      self.year = input("Write what year model you want 2026 or 2027: ")

    def brand_model(self):
      return f"Your car is a {self.brand} - {self.model},year {self.year},color {self.color}."

    def paint_vehicle(self):
      self.color = input("Want a change of color,if no just write NO. Colors available: BLUE, RED, YELLOW?: ").upper()
      if self.color == "NO":
        return f"NO"
      else:
        return f"Updated color of your car: {self.color}"

    def add_upgrade(self):
      print("")
      print(f"You want any of these upgrades? if no, enter 0.")
      self.upgrades = ["1.Premium sound system","2.Sport wheels","3.Fog lights"]
      while True:
        for upgrade in self.upgrades:
          print(upgrade)
        upgrades_input = input("Enter a number: ")
        try:
          index_number = int(upgrades_input) - 1
          if index_number == -1:
            print(f"No more upgrades added.")
            print(f"Added upgrades: {self.added_upgrades}")
            print("")
            print(f"Thanks!")
            break
          if index_number >= 0 and index_number < len(self.upgrades):
            self.added_upgrades.append(self.upgrades[index_number])
            print("NICE UPGRADE!")
            print(f"Selected upgrades added: {self.added_upgrades}")
            print("")
            print("Any other upgrade? if no, enter 0:")
          else:
            print(f"Invalid number, try again.")
            print("")
        except ValueError:
          print(f"Enter a valid number.")
          print("")
      return f"Your added upgrades: {self.added_upgrades}"

    def save_to_db(self):
      for attempt in range(5):
        try:
          conn = psycopg2.connect(
              host="db", database="vehicledb", user="myuser", password="mypassword"
          )
          cur = conn.cursor()
          cur.execute("""
              CREATE TABLE IF NOT EXISTS vehicles (
                  id SERIAL PRIMARY KEY,
                  brand TEXT, model TEXT, year TEXT, color TEXT, upgrades TEXT
              )
          """)
          cur.execute(
              "INSERT INTO vehicles (brand, model, year, color, upgrades) VALUES (%s, %s, %s, %s, %s)",
              (self.brand, self.model, self.year, self.color, ", ".join(self.added_upgrades))
          )
          conn.commit()
          cur.close()
          conn.close()
          print("Saved to database!")
          return
        except psycopg2.OperationalError:
          print("Database not ready yet, retrying...")
          time.sleep(2)
      print("Could not connect to database.")


# ---- New: API endpoints to VIEW saved vehicles ----

@app.get("/vehicles")
def get_vehicles():
    conn = psycopg2.connect(host="db", database="vehicledb", user="myuser", password="mypassword")
    cur = conn.cursor()
    cur.execute("SELECT id, brand, model, year, color, upgrades FROM vehicles;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    vehicles = [
        {"id": r[0], "brand": r[1], "model": r[2], "year": r[3], "color": r[4], "upgrades": r[5]}
        for r in rows
    ]
    return {"vehicles": vehicles}


if __name__ == "__main__":
    vh2 = Vehicle()
    car_features = [vh2.brand_model(), vh2.paint_vehicle(), vh2.add_upgrade()]
    for x in car_features:
      print(x)
    vh2.save_to_db()