import random
import Game
import Scoreboard
import tkinter as tk
import re
from enum import Enum
root = tk.Tk()

BASE_SCREEN_WIDTH = 2560
BASE_SCREEN_HEIGHT = 1440

# Full Screen
root.attributes('-fullscreen', True)

bg_color = 'powder blue'

# calculate screen dimensions

# common laptop screen size is: 1920W x 1080H
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# for laptop screen size testing
#screen_width = 1920
#screen_height = 1080

# calculate factors for different screen sizes
h_mod = screen_height / BASE_SCREEN_HEIGHT
w_mod = screen_width / BASE_SCREEN_WIDTH
font_size = (int) (min(h_mod, w_mod) * 12)

#h_mod = 0.5
#w_mod = 0.5

print("Screen Width: ",screen_width)
print("Screen Height: ",screen_height)
canvas1 = tk.Canvas(root, width = screen_width, height = screen_height, bg=bg_color)

close_button = tk.Button(root, text="Quit", command=root.destroy, anchor=tk.SW)
canvas1.create_window(30, 30, window=close_button)
canvas1.pack()
SEED = 2022
TEST = False
save_name = ""
players = 0
ppg = 0                 
rounds = 0
saveslot = 0
rounds_played = 0
name_sample = ['AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL']
sitters = [[] for _ in range(100)]
input_wait_flag = False
load_game = False



#names = name_sample
names = ['Maxwell','Cienna De Leon Cienna De Leon','Alec111','Cecilia','Cornelius','Kay Fontelle Slater','Rain Stecklein-Totten','AH','AI','AJ','AK','AL']    #for testing
mode_options = ["Double", "Triple", "Quadruple", "Pentuple", "Hextuple", "Septuple"]
player_names_var = [tk.StringVar() for _ in range(100)]
player_names = ["" for _ in range(100)] 
player_scores = [tk.StringVar() for _ in range(100)]
players_var = tk.StringVar()
rounds_var = tk.StringVar()
game_mode_var = tk.StringVar()
save_name_var = tk.StringVar()

class Mode(Enum):
    Double = 2
    Triple = 3
    Quadruple = 4
    Pentuple = 5
    Hextuple = 6
    Septuple = 7

# NOTES
# jan 24
# ALL terminal inputs will have to be replaced with GUI inputs
# bini bday
# 


# 
# To Do:
#   display save list meta data
#   
#   
#   
# 
# BUGS: 
# 
#
# 


# New game -> new_game_input_screen -> submit_button -> player_name_input_screen -> submit_player_names -> newgame_create
# Load game -> loadgame_button ->
def submit_scores_button():
    global rounds_played
    rounds_played += 1
    random.seed(SEED)
    
    if rounds_played % 2 == 1:
        f = open("GameFiles/scoreboard2", "r")
        f2 = open("GameFiles/scoreboard", "w")
    else:
        f = open("GameFiles/scoreboard", "r")
        f2 = open("GameFiles/scoreboard2", "w")

    for i in range(players):
        try:
            x = player_scores[i].get()
        except:
            x = 0
        print(f"[{x}]    ")

    for i in range(players):
        buf = f.readline().strip()

        # Only read score if the player is not sitting
        #if (i + 1) not in sitters[rounds_played]:
        try:
            y = int(player_scores[i].get())
        except:
            y = 0
        #else: 
            #y = 0

        f2.write(f"{buf}\t{y}\n")

    f.close()
    f2.close()
    # Clearing fields after submit button pressed
    for i in range(players):
        try:
            player_scores[i].delete(0, tk.END)
        except:
            pass
        #if (i + 1) not in sitters[rounds_played]:
        #    player_scores[i].delete(0, tk.END)

    Scoreboard.scoreBoard(rounds_played, players, ppg, player_names)
    saveGame(players, rounds, ppg, rounds_played, player_names)     # Maybe should be rounds_played - 1, not rounds_played??? 

    #print_scores()
    scores_input()

def scores_input():
    """global player_names
    global TEST
    global players
    global sitters
    global rounds_played"""
    clear_frame()
    print_scores()

    print("SITTERS: ",sitters)
    print("Rounds Played: ", rounds_played)
    print("scores_input called\n")
    
    # if this doesn't work try including mode options as global variable
    for i in range(players):
        players_label = tk.Label(root, text=f"{player_names[i][:10]}'s score:", fg='blue', font=('helvetica', font_size, 'bold'), anchor=tk.E, bg=bg_color, width=19)
        canvas1.create_window(80 * h_mod, (170 + (25 * i)) * w_mod, window=players_label)

        if (i + 1) in sitters[rounds_played + 1]:
            print("CONTINUE CALLED ON ", i)
            continue

        player_scores[i] = tk.Entry(root, font=('helvetica', font_size, 'bold'),width=3)
        canvas1.create_window(200 * h_mod,(170 + (25 * i)) * w_mod, window=player_scores[i])

    sub_btn = tk.Button(root, text='Submit', command=submit_scores_button, bg='brown', fg='white')
    canvas1.create_window(200 * h_mod, (175 + (25 * players)) * w_mod, window=sub_btn)

    return 1

def print_scores():
    global saveslot
    global players
    f = open(f"GameFiles/save{saveslot}", "r")
    f2 = open("GameFiles/scOut", "r")

    # I want the scores to be their own color, at least not all red
    past_scores_section = False

    #for _ in range(10):
    #    print("\n\n\n\n")

    # Printing Scores, Pars, Standings
    i = 0
    for line in f2:
        k = 0
        #---------------might not be needed-------------
        for name in player_names:        # replace full names with shortened ones
            line = line.replace(name, player_names[k][:10])
            k += 1
        #-----------------------------------------------
        
        if "Pars" in line or "Scores" in line or "Standings" in line:       # Color the line black if it's a header
            if "Pars" in line:
                past_scores_section = True
            label = tk.Label(root, text=line, fg='black', font=('helvetica', font_size + 5, 'bold'), bg=bg_color) 
            # increment i to move down the screen
            i += 2
            canvas1.create_window(500 * h_mod, (100 + (25 * i - 1)) * w_mod, window=label, anchor=tk.W)
            i += 1
            
        elif "Standings" in line:
            #font_size += 5
            label = tk.Label(root, text=line, fg='black', font=('helvetica', font_size, 'bold'), bg=bg_color)
            canvas1.create_window(600 * h_mod, (100 + (25 * i)) * w_mod, window=label, anchor=tk.E)
        else:

            # Printing Numbers, want good=green, bad=red
            # Split the input string into parts (name and numbers)
            parts = line.split(":")
            if len(parts) < 2:
                continue

            name = parts[0].strip()  # "ALEX"
            numbers = parts[1].strip().split()  # ["8", "-15", "5", "-2", "0", "0", "0"]

            # Label to display the name
            name_label = tk.Label(root, text=name, fg='black', font=('helvetica', font_size, 'bold'), bg=bg_color)
            canvas1.create_window(400 * h_mod, (100 + (25 * i)) * w_mod, window=name_label, anchor=tk.W)
            label = tk.Label(root, text=line, fg='blue', font=('helvetica', font_size, 'bold'), bg=bg_color)

            # Loop over the numbers and create a label for each
            space_between_nums = 0
            for idx, num in enumerate(numbers):
                x = float(num)
                print("X: ",x)
                
                number_value = float(num)  # Convert the string to a float
                if not past_scores_section:
                    # Scores Color
                    color = 'black'
                elif number_value > 0.0:
                    color = 'red'  # Positive numbers are red
                elif number_value < 0.0:
                    color = 'green'  # Negative numbers are green, lower score is good
                else:
                    color = 'black'  # Zero values are black
                print("NUM: ",num)
                
                number_label = tk.Label(root, text=num, fg=color, font=('helvetica', font_size, 'bold'), bg=bg_color, width=4)
                canvas1.create_window((500 + (40 * space_between_nums)) * h_mod, (100 + (25 * i)) * w_mod, window=number_label, anchor=tk.W)
                space_between_nums += 1

        

            i += 1
        
    
    # Print Round Schedules
    line_num = 0
    for line in f:
        line_num += 1
        # Ignore first 5 lines of Save Slot
        if line_num < 6:               
            continue

        # Finding sitters for each round (relevant because entry is taken away from sitting players)
        if line_num > 5 and line_num < 5 + rounds + 1:
            determine_sitters(line, line_num - 5)
        # Converting numbers into player names for display
        matches = line.split("-")

        # Remove empty string at end of list
        matches.pop()

        m = 0
        line_length = 0
        print("Matches5: ",matches)
        for match in matches:
            m += 1
            # Replace player numbers with names
            players_nums = match.split("vs")
            for num in players_nums:
                match = match.replace(num, (" " + player_names[int(num)-1] + " "))

            line_length += len(match) + 100
            print("LINE LENGTH: ",line_length)

            # Alternate colors for clarity
            if m%2==0:
                label = tk.Label(root, text=match, fg='red', font=('helvetica', font_size, 'bold'), bg=bg_color)
            else:
                label = tk.Label(root, text=match, fg='blue', font=('helvetica', font_size, 'bold'), bg=bg_color)

            
            canvas1.create_window((1100 + (100 * (m-1) * ppg)) * h_mod, (100 + (50 * (line_num - 6))) * w_mod, window=label, anchor=tk.W)

        # printing "round" header
        if(line_num - 5 <= rounds):
            print("CONDITION PASSED")
            canvas1.create_text(1000 * h_mod, (100 + (50 * (line_num - 6))) * w_mod, text= f"Round {line_num - 5}", font=('helvetica', font_size + 1, 'bold'), anchor=tk.W)

            
        
        
    """
        for k in range(0, players):
            line = line.replace(f"{k+1}", player_names[k])
        print("LINE2: ",line)
        if "Round" in line:             # Color the line black if it's a round header
            label = tk.Label(root, text=line, fg='black', font=('helvetica', 17, 'bold'))
            canvas1.create_window(700, 100 + (25 * i), window=label, anchor=tk.W)
        else:
            matches = line.split("-")
            m = 0
            print("Matches2: ",matches)
            for match in matches:
                if m%2 == 0:
                    label = tk.Label(root, text=match, fg='red', font=('helvetica', 17, 'bold'))
                    canvas1.create_window(775 + (200 * m), 100 + (25 * (i-1)), window=label, anchor=tk.W)
                else:
                    label = tk.Label(root, text=match, fg='blue', font=('helvetica', 17, 'bold'))
                    canvas1.create_window(775 + (200 * m), 100 + (25 * (i-1)), window=label, anchor=tk.W)
                m += 1
                    
        i += 1
        """
        

    """
    while True:
        buf2 = f2.readline()
        if not buf2:
            break
        buf2 = buf2.strip()
        if not buf_end:
            buf2 = buf2.strip()
        if buf2:
            print(buf2)
        buf = f.readline()
        if not buf_end:
            print(" " * (50 - len(buf2)), end="")
        if temp != buf:
            print(buf, end="")
            temp = buf
        elif not buf_end:
            print("\n")
            buf_end = True

    # Printing Schedule
    while True:
        buf = f.readline()
        if not buf:
            break
        print(" " * 50, end="")
        print(buf, end="")
    """
    

    f.close()
    f2.close()

def makeTemplate(players):
    f = open("GameFiles/scoreboardTemplate", "w")
    for i in range(1, players + 1):
        f.write(f"{i}:\n")
    f.close()

def reset():
    f = open("GameFiles/scoreboardTemplate", "r")
    f2 = open("GameFiles/scoreboard2", "w")
    f3 = open("GameFiles/scoreboard", "w")
    f4 = open("GameFiles/scOut", "w")
    
    while True:
        buf = f.readline()
        if not buf:
            break
        f2.write(buf)

    f.close()
    f2.close()
    f3.close()
    f4.close()

def resetSaves():
    f = open("GameFiles/saveList", "w")
    f.write("1: ______________________________\n2: ______________________________\n3: ______________________________\n")
    f.write("4: ______________________________\n5: ______________________________\n")
    f.close()

def getInput():
    global players
    global rounds
    global ppg
    out = None
    print("\n-- Main Menu --")
    print("0: New Game\n1: Load Saved Game\n2: Testing Mode")
    out = int(input())

    if out == 1: 
        return out
    
    if out == 2: # ADDED OPTION 2 FOR TESTING
        global TEST
        players = 5
        rounds = 8
        ppg = 3
        TEST = True
        print("TEST: ",TEST)
        return  out # ppg, players, rounds

    print("How many players?")
    players = int(input())

    print("How many rounds?")
    rounds = int(input())

    ppg = 0
    while ppg not in range(2, 8):
        print("\n-- Game Selection --")
        print("2: Double\n3: Triple\n4: Quadruple\n5: Pentuple\n6: Hextuple\n7: Septuple\n0: Exit")
        ppg = int(input())

    return 0


def displaySaveList():
    with open("GameFiles/saveList", "r") as save_list:
        for line in save_list:
            if line[3] != '_':
                line = line.replace('_', ' ')
            print(line, end='')

def loadGame():
    global players
    global rounds
    global ppg
    global player_names
    global saveslot
    global rounds_played
    global load_game
    load_game = True
    save = None
    f2 = open("GameFiles/f2", "w")
    s1 = open("GameFiles/scoreboard", "w")
    s2 = open("GameFiles/scoreboard2", "w")
    
    #displaySaveList()
    #display_saves_window()      # this calls select_save_slot() which sets saveslot
    #print("\nEnter a save slot: ")
    #saveslot = int(input())

    save_file_map = {
        1: "GameFiles/save1",
        2: "GameFiles/save2",
        3: "GameFiles/save3",
        4: "GameFiles/save4",
    }
    save = open(save_file_map.get(saveslot, "GameFiles/save5"), "r")

    #----------------------------
    """i = 0
    while(i < 100):
        line = save.readline().strip()
        i += 1
        print(line)


    """
    #----------------------------
    line = save.readline().strip()  # first line
    print(line)
    buf_small = save.readline().strip()  # players 
    print(buf_small)
    split = buf_small.split(" ")
    players = int(split[0])
    f2.write(f"{players}\n")
    #print(f"{players} Players buf:({buf_small})")

    buf_small = save.readline().strip()  # rounds
    split = buf_small.split(" ")
    rounds = int(split[0])
    
    f2.write(f"{rounds}\n")
    #print(f"{rounds} rounds buf:({buf_small})")

    buf_small = save.readline().strip()  # ppg
    print(buf_small)
    split = buf_small.split(" ")
    ppg = int(split[0])
    f2.write(f"{ppg}\n")
    #print(f"{ppg} ppg buf:({buf_small})")

    buf_small = save.readline().strip()  # rounds played
    print(buf_small)
    split = buf_small.split(" ")
    rounds_played = int(split[0])
    #print(f"{rounds_played} rounds played buf:({buf_small})")

    BUFSIZE = (10 * rounds) + 3
    BUF2 = (35 * players)
    if BUF2 > BUFSIZE:
        BUFSIZE = BUF2
    buf = [''] * BUFSIZE

    print("------------SCHEDULE----------")
    for i in range(rounds):
        buf[i] = save.readline()
        f2.write(buf[i])
        print(buf[i], end='')

    print("\n------------SCOREBOARD----------")
    for i in range(players):
        buf[i] = save.readline()
        s1.write(buf[i])
        s2.write(buf[i])
        print(buf[i], end='')

    print("\n------------PLAYERS------------")
    buf = save.readline()
    for i in range(players,2):
        player_names[i] = buf[i:i+1]

    # EXPIREMENTAL-----------------------------------
    for i in range(players):
        buf = save.readline()
        player_names[i] = buf.strip()

    #print(buf)
    print("Names3: ",player_names)

    save.close()
    f2.close()
    s1.close()
    s2.close()
    Scoreboard.scoreBoard(rounds_played, players, ppg, player_names)
    scores_input()

def createGame():
    global saveslot
    first_input = True
    BUFSIZE = 20
    buf = ""
    
    #displaySaveList()  
    #display_saves_window()
    #saveslot = int(input("Enter a save slot: "))     
    
    with open("GameFiles/saveList", "r+") as saveList:
        saveList.seek(3 + (35 * (saveslot-1)))
        saveList.write("_" * 30) # write over any previous save
        print(saveList.tell())
        saveList.seek(saveList.tell() - 30)  # go back to start of line
        
        while first_input or len(buf) < 1 or len(buf) > 30:
            first_input = False
            print("\n(No spaces)\nName of save: ")
            buf = save_name_var.get()
            if len(buf) > 30:
                print("\nError: Save name too long. Must be under 30 characters.")
            else:
                print(f"Length: {len(buf)}   ")
                saveList.write(buf)
    


def saveGame(players, rounds, ppg, rounds_played, player_names):
    global saveslot
    BUFSIZE = (10 * rounds) + 5
    
    save_filename = f"GameFiles/save{saveslot}"
    with open(save_filename, "w") as f:
        f2_filename = "GameFiles/f2"
        f3_filename = "GameFiles/scoreboard" if rounds_played % 2 == 1 else "GameFiles/scoreboard2"
        
        with open(f2_filename, "r") as f2, open(f3_filename, "r") as f3:
            f.write(f"----- Save Slot {saveslot} -----\n")
            f.write(f"{players} Players\n{rounds} Rounds\n{ppg} Players Per Game\n{rounds_played} Rounds Played\n")
            
            # printing schedule
            # ignore first 3 lines of "f2"
            for _ in range(3):
                f2.readline()
            
            for line in f2:
                f.write(line)
            
            # printing scoreboard
            for i in range(players):
                print(f"Saved player {i+1}")
                line = f3.readline()
                f.write(line)
            
            # printing names
            for i in range(players):
                for j in range(2):
                    f.write(player_names[i][j])

            # EXPIREMENTAL--------------------------------------------------
            # Adding full names to end of save file
            for i in range(players):
                f.write("\n")
                f.write(player_names[i])

def do_nothing():
    pass

# New Game Screen 1
def new_game_input_screen():
    print("new game input screen called\n")
    clear_frame()
    global players_var
    global game_mode_var
    # if this doesn't work try including mode options as global variable
    players_label = tk.Label(root, text='Enter number of players:', fg='blue', font=('helvetica', font_size, 'bold'), bg=bg_color)
    players_entry = tk.Entry(root, textvariable= players_var, font=('helvetica', font_size, 'bold'))
    rounds_label = tk.Label(root, text='Enter number of rounds:', fg='blue', font=('helvetica', font_size, 'bold'), bg=bg_color)
    rounds_entry = tk.Entry(root, textvariable= rounds_var, font=('helvetica', font_size, 'bold'))

    game_mode_var.set("Double")
    dropdown = tk.OptionMenu(root, game_mode_var, *mode_options)
    

    # creating submit button
    sub_btn = tk.Button(root, text='Submit', command=submit_button, bg='brown', fg='white')
    canvas1.create_window(170 * h_mod, 170 * w_mod, window=players_label)
    canvas1.create_window(170 * h_mod, 200 * w_mod, window=players_entry)
    canvas1.create_window(170 * h_mod, 250 * w_mod, window=rounds_label)
    canvas1.create_window(170 * h_mod, 300 * w_mod, window=rounds_entry)
    canvas1.create_window(170 * h_mod, 350 * w_mod, window=dropdown)
    canvas1.create_window(170 * h_mod, 400 * w_mod, window=sub_btn)
    #root.mainloop()

# New Game Screen 1
def submit_button():
    global players
    global rounds
    global ppg
    players = int(players_var.get())
    rounds = int(rounds_var.get())
    mode = game_mode_var.get()
    ppg = Mode[mode].value

    print("submit button called\n")
    print(f"players: {players}, rounds: {rounds}, ppg: {ppg}\n")
    clear_frame()
    player_name_input_screen()
    pass

# New Game Screen 2
def player_name_input_screen():
    global player_names
    print("player name input screen called\n")

    player_name_label = tk.Label(root, text='Enter player names:', fg='blue', font=('helvetica', font_size, 'bold'), bg=bg_color)
    canvas1.create_window(170 * h_mod, 170 * w_mod, window=player_name_label)
    # pe stands for player entry
    for i in range(players):
        pe = tk.Entry(root, textvariable= player_names_var[i], font=('helvetica', font_size, 'bold'))
        canvas1.create_window(170 * h_mod, (200 + (50 * i)) * w_mod, window=pe)

    sub_btn = tk.Button(root, text='Submit', command=submit_player_names, bg='brown', fg='white')
    canvas1.create_window(170 * h_mod, (200 + (50 * players)) * w_mod, window=sub_btn)

# New Game Screen 2
def submit_player_names():
    global player_names
    error = False
    print("submit player names called\n")
    for i in range(players):
        player_names[i] = player_names_var[i].get()
        print("NAME ",i, ": ",player_names[i], "   len: ",len(player_names[i]))
        if (len(player_names[i]) < 2):
            print("ERRORRRRRRR")
            error_label = tk.Label(root, text='Error: Player Names must be at least 2 characters long.', fg='red', font=('helvetica', font_size, 'bold'), bg=bg_color)
            canvas1.create_window(500 * h_mod, 500 * w_mod, window=error_label)
            error = True
            player_name_input_screen()
            

    print(player_names)

    if not error: display_saves_window()
    pass

# New Game Screen 3
def newgame_create(): 
    global rounds_played
    global players
    global rounds
    global ppg
    global player_names
    clear_frame()
    Game.game(players, rounds, 2000, ppg, player_names)  
    createGame()
    makeTemplate(players)  
    reset() 
    saveGame(players, rounds, ppg, rounds_played, player_names)
    scores_input()
    """for i in range(rounds_played + 1, rounds + 1):

        print_scores()   
        Scoreboard.scoreBoard(i, players, ppg, names)
            
        print_scores() 
        saveGame(players, rounds, ppg, i-1, names)
        print("Game Saved.")
        """
        
    

def clear_frame():
    for widget in root.winfo_children():
        if widget != canvas1 and widget != close_button:
            widget.destroy()

def loadgame_button():
    global load_game
    load_game = True
    display_saves_window()
    #loadGame()  
    #Scoreboard.scoreBoard(rounds_played, players, ppg, player_names)  
    #print_scores(10*players, 8*rounds)
    #print_scores() 

# New Game Sceen 4
def select_save_slot(selection):
    global saveslot
    saveslot = selection
    print(saveslot)
    clear_frame()
    if(load_game):
        loadGame()
    else:
        enter_save_name()
        
    

def display_saves_window():
    clear_frame()
    f = open("GameFiles/saveList", "r")
    # To Do item: put meta data
    text = tk.Label(root, text='Select a save file:', fg='blue', font=('helvetica', font_size, 'bold'), bg=bg_color)
    canvas1.create_window(170 * h_mod, 100 * w_mod, window=text)
    i = 0
    for line in f:
        i += 1
        if not line.strip():        # for end of file
            break

        # only getting save name from line
        save_name = re.match(r"\d+: ([\w\W]+?)_", line)

        button1 = tk.Button(text=save_name.group(1), command=lambda i=i: select_save_slot(i), bg='brown',fg='white', anchor=tk.CENTER, width=(int)(20 * w_mod))
        label1 = tk.Label(root, text=f"Save {i}:", fg='blue', font=('helvetica', font_size, 'bold'), anchor=tk.CENTER, bg=bg_color)
        canvas1.create_window(100 * h_mod, (100 + (50 * i)) * w_mod, window=label1)
        canvas1.create_window(225 * h_mod, (100 + (50 * i)) * w_mod, window=button1)


# New Game Screen 5
def enter_save_name():
    clear_frame()
    name_label = tk.Label(root, text='Enter a name for the save:', fg='blue', font=('helvetica', font_size, 'bold'), bg=bg_color)
    name_entry = tk.Entry(root, textvariable= save_name_var, font=('helvetica', font_size, 'bold'))
    sub_btn = tk.Button(root, text='Submit', command=submit_save_name_button, bg='brown', fg='white')
    canvas1.create_window(170 * h_mod, 400 * w_mod, window=name_label)
    canvas1.create_window(170 * h_mod, 450 * w_mod, window=name_entry)
    canvas1.create_window(170 * h_mod, 500 * w_mod, window=sub_btn)

# New Game Screen 5
def submit_save_name_button():
    global save_name
    global load_game
    save_name = save_name_var.get()

    newgame_create()




def player_name_input_screen():
    global player_names
    print("player name input screen called\n")

    player_name_label = tk.Label(root, text='Enter player names:', fg='blue', font=('helvetica', font_size, 'bold'), bg=bg_color)
    canvas1.create_window(170 * h_mod, 170 * w_mod, window=player_name_label)
    # pe stands for player entry
    for i in range(players):
        pe = tk.Entry(root, textvariable= player_names_var[i], font=('helvetica', font_size, 'bold'))
        canvas1.create_window(170 * h_mod,(200 + (50 * i)) * w_mod, window=pe)

    sub_btn = tk.Button(root, text='Submit', command=submit_player_names, bg='brown', fg='white')
    canvas1.create_window(170 * h_mod, (200 + (50 * players)) * w_mod, window=sub_btn)


def determine_sitters(line, round):
    print("DETERMINE SITTERS CALLED")
    global sitters
    global players
    global ppg

    for i in range(1, players + 1):
        if f"{i}" not in line:
            print(f"Player {i} is sitting in round {round}")
            sitters[round].append(i)

def create_table(root, rows, cols, data):
    # Create a grid of labels to represent the table
    for i in range(rows):
        for j in range(cols):
            # Create a label for each cell
            label = tk.Label(root, text=data[i][j], borderwidth=1, relief="solid", width=15, height=2)
            label.grid(row=i, column=j, sticky="nsew")

"""
Example of sample data for the table
data = [
    ["Player", "Score", "Pars", "Standings"],
    ["Maxwell", "10", "2", "1"],
    ["Cienna", "8", "3", "2"],
    ["Alec", "5", "4", "3"],
    ["Cecilia", "3", "5", "4"]
]
"""           
def main():

    #label1 = tk.Label(root, text= '', fg='blue', font=('helvetica', font_size, 'bold'))
    #canvas1.create_window(170, 200, window=label1)
    """
    players_sub = 8
    for i in range(players_sub):
        players_label = tk.Label(root, text=f"{names[i][:10]}'s score:", fg='blue', font=('helvetica', font_size, 'bold'), anchor=tk.W, width=19)
        #players_label = tk.Label(root, text="'s score:", fg='blue', font=('helvetica', font_size, 'bold'), anchor=tk.W, width=19)
        player_scores[i] = tk.Entry(root, font=('helvetica', font_size, 'bold'),width=3)
        canvas1.create_window(125, 170 + (25 * i), window=players_label)
        canvas1.create_window(200, 170 + (25 * i), window=player_scores[i])

    sub_btn = tk.Button(root, text='Submit', command=submit_scores_button, bg='brown', fg='white')
    canvas1.create_window(200, 175 + (25 * players_sub), window=sub_btn)
    """

    button1 = tk.Button(text='New Game', command=new_game_input_screen, bg='brown',fg='white')
    canvas1.create_window(170 * h_mod, 170 * w_mod, window=button1)

    button2 = tk.Button(text='Load Game', command=loadgame_button, bg='blue', fg='white')
    canvas1.create_window(170 * h_mod, 220 * w_mod, window=button2)

    #button3 = tk.Button(text='Testing Mode', command=do_nothing, bg='green', fg='white')
    #canvas1.create_window(170, 250, window=button3)
    
    root.mainloop()
    
    """exit = 0
    
    menu_select = getInput()  
    #menu_select = 0
    global TEST
    global names
    global rounds_played
    print(players, " players\n")
    
    if menu_select == 0:
        print("\nEnter Each Player's First and Last Initials")
        for i in range(players):
            print(f"\nPlayer {i+1}: ")
            name = input()
            names[i] = name

        Game.game(players, rounds, 2000, ppg, names)  
        createGame()
        makeTemplate(players)  
        reset()  
    elif menu_select == 1:
        loadGame()  
        Scoreboard.scoreBoard(rounds_played, players, ppg, names)  
        #print_scores(10*players, 8*rounds)
        print_scores()  
    elif menu_select == 2:
        print("MENU WORKING")
        names = name_sample[:players]
        Game.game(players, rounds, 2000, ppg, names)  
        createGame()
        makeTemplate(players)  
        reset() 
    
        
    
    
    for i in range(rounds_played + 1, rounds + 1):
        #print_scores(10*players, 8*rounds)
        print_scores() 
        exit = scores_input(names)  
        if exit == 0 or i == 1:
            Scoreboard.scoreBoard(i, players, ppg, names)
            #print_scores(10*players, 8*rounds)
            print_scores() 
        else:
            break
    
        saveGame(players, rounds, ppg, i-1, names)
        print("Game Saved.")
        """
        
if __name__ == "__main__":
    main()


"""
        if not TEST:
            y = int(player_scores[i].get())
        else:
            y = random.randint(1,52)

        if not TEST:
            print("\n0: Yes\n1: No\nFinalize Scores?")
            x = int(input())
            print("\n\n\n\n")
        else:
            x = 0

        if x == 1:
            scores_input(players, round, names)
            
"""