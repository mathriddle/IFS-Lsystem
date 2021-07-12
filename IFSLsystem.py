"""
Drawing fractals of iterated function systems using L-system
Modified from original Python program by Gianni Perez (2018) at 
https://github.com/ambron60/l-system-drawing
Input:
   (1) L-system rules (e.g. F -> F+F-F; end with blank 0)
   (2) axiom
   (3) angle increment in degrees
   (4) initial direction
   (5) IFS scaling factor
   (6) scale for window 
   (7) graphic window size
   (8) number of iterations
Input can be entered manually or via a text file in the same directory as the program.
The number of iterations (6) and graphic window size (8) are not part of the file
and will always be entered manually while program is running.
usage:
    python IFSLsystem.py
       or
    python IFSLsystem.py filename.txt
"""

import turtle
import sys
import os

SYSTEM_RULES = {}  # generator system rules for l-system
IFS = {}                    # holds info about iterated function system

def derivation(axiom, steps):
    derived = [axiom]  
    for _ in range(steps):
        next_seq = derived[-1]
        next_axiom = [rule(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived

def rule(sequence):
    if sequence in SYSTEM_RULES:
        return SYSTEM_RULES[sequence]
    return sequence

def draw_l_system(turtle, SYSTEM_RULES, seg_length, angle, init_heading):
    turtle.pd()
    turtle.hideturtle()
    turtle.pensize(1)
    turtle.speed(0)
    turtle.setheading(init_heading)    
    stack = []
    kolors = ["black","red","DarkGreen","blue","DarkOrange2","brown","purple"]
    curKolor = 0
    turtle.color(kolors[curKolor])
    for command in SYSTEM_RULES:
        if command in ["F", "G", "R", "L"]:
            turtle.forward(seg_length)
        elif command == "f":
            turtle.pu()  
            turtle.forward(seg_length)
            turtle.pd()
        elif command == "+":
            turtle.left(angle)
        elif command == "-":
            turtle.right(angle)
        elif command == "[":
            stack.append((turtle.position(), turtle.heading()))
        elif command == "]":
            turtle.pu()  
            position, heading = stack.pop()
            turtle.goto(position)
            turtle.setheading(heading)
            turtle.pd()
        elif command == "c":  #used with axiom when multiple copies of fractal are drawn
            curKolor = (curKolor+1) % len(kolors)
            turtle.color(kolors[curKolor])

def userinput():    #user enters IFS info manually
    #Ask for rules. A rule must include the -> notation
    rule_num = 1
    while True:
        rule = input("Enter rule[%d] (or 0 when done): " % rule_num)
        rule = "".join(rule.split())
        while (rule != '0') and (rule.count("->") != 1):
            print("   *** Error: must use '->' in rule[%d]. Try again. ***" % rule_num)
            rule = input("Enter rule[%d] (or 0 when done): " % rule_num)
            rule = "".join(rule.split())
        if rule == '0':
            break          
        key, value = rule.split("->")
        SYSTEM_RULES[key] = value
        rule_num += 1
        
    #Ask for axiom
    axiom = input("Enter axiom: ")
    IFS["axiom"] = "".join(axiom.split())
    
    #Ask for angle. Should be in degrees
    IFS["angle"] = float(input("Enter angle increment in degrees: "))

    #Ask for initial heading in degrees
    IFS["alpha"] = float(input("Enter initial heading: "))
    
    #Ask for IFS scaling factor. This should be between 0 and 1 for converging IFS
    scaling = float(input("Enter IFS scaling factor: "))
    while (scaling <= 0) or (scaling >=1):
        print ('   *** Error: IFS scaling factor should be between 0 and 1 ***')
        scaling = float(input("Enter IFS scaling factor: "))
    IFS["scale"] = scaling
    
    #Window limits along axes 
    xlimits = input("Enter min x, max x: ")
    while xlimits.count(",") != 1:
        xlimits = input("Enter min x, max x: ") 
    xmin, xmax = [ float(w) for w in xlimits.split(",")]
    ylimits = input("Enter min y, max y: ")
    while ylimits.count(",") != 1:
        ylimits = input("Enter min y, max y: ") 
    ymin, ymax = [ float(w) for w in ylimits.split(",")]
    IFS["xaxes"] = [xmin,xmax]
    IFS["yaxes"] = [ymin,ymax]

def readinput():    #get IFS input from a file
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        filepath2 = filepath + ".txt"
        if not os.path.isfile(filepath2):
            print("File {} does not exist in this directory.".format(filepath))
            sys.exit()
        filepath = filepath2
    with open(filepath, 'r') as f:
        line = "".join(f.readline().split()).partition(":")[2]
        while (line[0]=='#'):   #Ignore comments indicated by # symbol
            line = "".join(f.readline().split()).partition(":")[2]
        while (line != '0'):
            key, value = line.split("->")
            SYSTEM_RULES[key] = value
            line = "".join(f.readline().split()).partition(":")[2]
        IFS["axiom"] = "".join(f.readline().split()).partition(":")[2]
        IFS["angle"] = float(f.readline().partition(":")[2])
        IFS["alpha"] = float(f.readline().partition(":")[2])
        IFS["scale"] = float(f.readline().partition(":")[2])
        IFS["xaxes"] = [ float(w) for w in f.readline().partition(":")[2].split(",")]
        IFS["yaxes"] = [ float(w) for w in f.readline().partition(":")[2].split(",")]
    f.close()

def draw():
    xmin = IFS["xaxes"][0]
    xmax = IFS["xaxes"][1]
    ymin = IFS["yaxes"][0]
    ymax = IFS["yaxes"][1]
    #Ask for window size
    wsize = int(input("Enter window size in pixels: "))  
    if ymax-ymin > xmax-xmin:
        ysize = wsize
        xsize = round((xmax-xmin)/(ymax-ymin)*wsize)
    else:
        xsize = wsize
        ysize = round((ymax-ymin)/(xmax-xmin)*wsize)
    # Ask for iterations. Loop until iterations=0
    iterations = int(input("Enter number of iterations: "))  
    winCreated = False
    if (iterations > 0):  
        # Set turtle parameters 
        win = turtle.Screen()  # create graphics window
        win.setup(xsize, ysize)
        win.setworldcoordinates(xmin,ymin,xmax,ymax) 
        t = turtle.Turtle()  # recursive turtle
        t.hideturtle() 
        winCreated = True
    while (iterations > 0):    #Create the L-system
        model = derivation(IFS["axiom"], iterations)  # axiom (initial string), nth iterations
        segment_length = IFS["scale"]**iterations   
        draw_l_system(t, model[-1], segment_length, IFS["angle"], IFS["alpha"])  # draw model
        iterations = int(input("Enter number of iterations (0 to end): "))     
        if (iterations > 0): win.reset()      
    if (winCreated):
        win.exitonclick()   #Graphics window closes when user clicks in window

def main():
    narg = len(sys.argv)
    if narg == 1:    #get input from user
        ifs = userinput()
    else:                #read input from file
        ifs = readinput()
    draw()
    
if __name__ == "__main__":
    main()
