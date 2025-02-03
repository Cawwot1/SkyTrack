import time
import keyboard
from maps import Map
from map_data import *

class Game:
    
    def __init__(self):
        self.map_choice = None

    def game_run(self):
        
        #Possible to add speed feature

        self.map_choice = input("Choose map number: ")
        
        if self.map_choice == "map1":
            self.map_choice = map1() #Returns map data
        
        #Change dislpay

        #input-check
        input_check = input("Are you ready: ")

        #Replace with frontend button
        input_check = True

        #Replace with a more complicated algorithm (combos etc.)
        points = 0

        if input_check: #The actual game
            
            print("<-------START------->\n")
            
            for number in self.map_choice["map_data"]:
                
                print(
                        f"PRESS NUMBER: {number}"
                    )

                start = time.time()

                while True:
                    
                    completed_input = False
                    
                    for i in range(1, 9): #Key press detector
                        if keyboard.is_pressed(i) and number == i:
                            completed_input = True
                            points += 1
                            break
                    
                    end = time.time()

                    if (end-start) >= 1:
                        break
                
                if completed_input:
                    print(
                        "Key pressed correctly !!!\n"
                        "<------------------->"
                          )
                else:
                    print(
                        "Key missed\n"
                         "<------------------->"
                          )
