import time

def game_generator(speed, level):
    
    required_inputs = [] #for each line
    note_num = 0
    points = 0

    test_score = [[1, 0, 0, 0, 0], #Left, Up, Right, Down, Spacebar
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0]]

    #Note: find a way to generate score while running for functions

    #Game-run backend
    for line in test_score:
        for note in line:
            if note_num == 0 and note != 0:
                required_inputs.append("left")
            elif note_num == 1 and note != 0:
                required_inputs.append("up")
            elif note_num == 2 and note != 0:
                required_inputs.append("right")
            elif note_num == 3 and note != 0:
                required_inputs.append("down")
            elif note_num == 4 and note != 0:
                required_inputs.append("spacebar")
            note_num += 1
        
        #Run while loop while waiting 1 sec
        while True:
            if #left-press
                required_inputs.remove("left")
                points += 1
            if #up-press
                required_inputs.remove("up")
                points += 1
            if #right-press
                required_inputs.remove("right")
                points += 1
            if #down-press
                required_inputs.remove("down")
                points += 1
            if #spacebar-press
                required_inputs.remove("spacebar")
                points += 1

        note_num = 0
        


if __name__ == "__main__":
    
