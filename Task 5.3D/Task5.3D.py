import RPi.GPIO as GPIO, time
from Tkinter import *

window = Tk()
window.geometry("300x50")
window.title("String to Morse Code")

# the input text is saved to this variable
textInput = StringVar()

LED = 18 # LED pin number
unit = 0.5 # sets the unit length for the morse code

# setup the pin mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

# blinks a dot
def dot():
	GPIO.output(LED, True)
	time.sleep(unit)
	GPIO.output(LED, False)
	time.sleep(unit)

# blinks a dash
def dash():
	GPIO.output(LED, True)
	time.sleep(unit*3)
	GPIO.output(LED, False)
	time.sleep(unit)

# longer break for a new character (3 units)
def newChar():
	time.sleep(unit*2)

# functions for each letter of the alphabet
# calls the dot, dash and newChar functions in the relevant order
def A():
	dot()
	dash()

def B():
	dash()
	dot()
	dot()
	dot()
	
def C():
	dash()
	dot()
	dash()
	dot()

def D():
	dash()
	dot()
	dot()
	
def E():
	dot()

def F():
	dot()
	dot()
	dash()
	dot()

def G():
	dash()
	dash()
	dot()
	
def H():
	dot()
	dot()
	dot()
	dot()
	
def I():
	dot()
	dot()
	
def J():
	dot()
	dash()
	dash()
	dash()
	
def K():
	dash()
	dot()
	dash()
	
def L():
	dot()
	dash()
	dot()
	dot()
	
def M():
	dash()
	dash()
	
def N():
	dash()
	dot()
	
def O():
	dash()
	dash()
	dash()
	
def P():
	dot()
	dash()
	dash()
	dot()
	
def Q():
	dash()
	dash()
	dot()
	dash()
	
def R():
	dot()
	dash()
	dot()
	
def S():
	dot()
	dot()
	dot()

def T():
	dash()
	
def U():
	dot()
	dot()
	dash()
	
def V():
	dot()
	dot()
	dot()
	dash()
	
def W():
	dot()
	dash()
	dash()
	
def X():
	dash()
	dot()
	dot()
	dash()

def Y():
	dash()
	dot()
	dash()
	dash()
	
def Z():
	dash()
	dash()
	dot()
	dot()

# iterates through the text input and calls the appropriate function for each letter
def convertToCode():
	MorseText = textInput.get()
	if len(MorseText) > 12:
		return
	for i in MorseText:
		if i.upper() == "A":
			A()
		elif i.upper() == "B":
			B()
		elif i.upper() == "C":
			C()
		elif i.upper() == "D":
			D()
		elif i.upper() == "E":
			E()	
		elif i.upper() == "F":
			F()
		elif i.upper() == "G":
			G()
		elif i.upper() == "H":
			H()
		elif i.upper() == "I":
			I()
		elif i.upper() == "J":
			J()
		elif i.upper() == "K":
			K()
		elif i.upper() == "L":
			L()
		elif i.upper() == "M":
			M()
		elif i.upper() == "N":
			N()
		elif i.upper() == "O":
			O()
		elif i.upper() == "P":
			P()
		elif i.upper() == "Q":
			Q()
		elif i.upper() == "R":
			R()
		elif i.upper() == "S":
			S()
		elif i.upper() == "T":
			T()
		elif i.upper() == "U":
			U()
		elif i.upper() == "V":
			V()
		elif i.upper() == "W":
			W()
		elif i.upper() == "X":
			X()
		elif i.upper() == "Y":
			Y()
		elif i.upper() == "Z":
			Z()
		newChar()

textEntry = Entry(window, width=12, textvariable=textInput)#.grid(column=2, row=1)
convertButton = Button(window, text="Convert to Morse Code", command=convertToCode)#.grid(column=2, row=13)

textEntry.pack(side=LEFT)
convertButton.pack(side=RIGHT)

window.mainloop()
