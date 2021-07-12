# IFS-Lystem
Python program to draw fractals of iterated function systems defined by an L-system.

Modified from original Python program by Gianni Perez (2018) at 
https://github.com/ambron60/l-system-drawing

Input: \
   (1) L-system rules (e.g. F -> F+F-F; end with blank 0) \
   (2) axiom \
   (3) angle increment in degrees \
   (4) initial direction \
   (5) IFS scaling factor \
   (6) scale for window  \
   (7) graphic window size \
   (8) number of iterations 
   
Input can be entered manually or via a text file in the same directory as the program.
The graphic window size (7) and number of iterations (8) are not part of the file
and will always be entered manually while program is running.

After the fractal is drawn for a specified iteration, the program will ask for another
iteration value until the user enters 0 (or any negative value).

Usage: \
    python IFSLsystem.py \
       or \
    python IFSLsystem.py filename.txt \
    
A typical file would look like \
:# Heighway Dragon \
rule: F -> Z \
rule: X -> +FX--FY+ \
rule: Y -> -FX++FY- \
end of rules: 0 \
axiom: FX \
angle: 45 \
direction: 0 \
scaling: 0.7071067812 \
iterations: 8 \
x-range: -0.4,1.25 \
y-range: -0.6,1.05 

Example files are contained in the IFS folder.

For more information about the fractals of some classic iterated function systems, see \
https://larryriddle.agnesscott.org/ifs/ifs.htm
