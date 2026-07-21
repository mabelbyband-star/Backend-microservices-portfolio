class Vehicle:
    def __init__(self):
      self.color = "Factory white"
      self.added_upgrades = []

      self.brand = input("Write the brand you want; TESLA, FORD, TOYOTA: ").upper()
      if self.brand == "TESLA":
        self.model = input("Write the Tesla model you want; MODEL 3, MODEL Y: ").upper()
        pass
      elif self.brand == "FORD":
        self.model = input("Write the Ford model you want; MUSTANG, F150: ").upper()
        pass
      elif self.brand == "TOYOTA":
        self.model = input ("Write the Toyota model you want; RUNNER, PRIUS: ").upper()
        pass
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
        return f"Updated color of your car: {self.color}" #### Im updating the deafault attribute self.color, Im re-using it. 

  
    def add_upgrade(self):
      print("")
      print(f"You want any of these upgrades? if no, enter 0.")
      
      self.upgrades = ["1.Premium sound system","2.Sport wheels","3.Fog lights"]

      while True:
        for upgrade in self.upgrades:
          print(upgrade)
    
        upgrades_input = input("Enter a number: ")
        
        try: 
        # I am handling the possible errors when asking the user to enter numbers, and user enters letters.          
          index_number = int(upgrades_input) - 1
  
          if index_number == -1:
          # I am choosing -1 so when the user enters 0 the service is done, and the loop stops.
          # since 0 - 1 = -1. due to the index_number math.
            print(f"No more upgrades added.")
            #else: no need to use else
            print(f"Added upgrades: {self.added_upgrades}")
            print("")
            print(f"Thanks!")
            break
            
          if index_number >= 0 and index_number < len(self.upgrades):
                #print(f"Following upgrade added: {self.upgrades[index]}")
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
      # remmeber the method should return other wise it will output a "NONE, Identation at level of the while loop."
      return f"Your added upgrades: {self.added_upgrades}"    

vh2 = Vehicle()
car_features = [vh2.brand_model(), vh2.paint_vehicle(), vh2.add_upgrade()]
for x in car_features:
  print(x)
