import RPi.GPIO as GPIO, time
from Tkinter import *

window = Tk()
window.geometry("100x100")
window.title("Choose LED")

r = StringVar()
g = StringVar()
b = StringVar()

r.set("X")
g.set("Y")
b.set("Z")


redLED = 18
greenLED = 5
blueLED = 22

pinList = [redLED, greenLED, blueLED]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinList, GPIO.OUT)


def redToggle():
	GPIO.output(redLED, True)
	GPIO.output(greenLED, False)
	GPIO.output(blueLED, False)
	g.set("R")
	b.set("R")

def greenToggle():
	GPIO.output(greenLED, True)
	GPIO.output(redLED, False)
	GPIO.output(blueLED, False)
	r.set("G")
	b.set("G")

def blueToggle():
	GPIO.output(blueLED, True)
	GPIO.output(redLED, False)
	GPIO.output(greenLED, False)
	r.set("B")
	g.set("B")

def exitWindow():
	GPIO.output(redLED, False)
	GPIO.output(greenLED, False)
	GPIO.output(blueLED, False)
	window.destroy()

red = Radiobutton(window, text="Red", variable=r, value="R", command=redToggle)
green = Radiobutton(window, text="Green", variable=g, value="G", command=greenToggle)
blue = Radiobutton(window, text="Blue", variable=b, value="B", command=blueToggle)

exit = Button(window, text="exit", command=exitWindow)

red.pack(anchor=W)
green.pack(anchor=W)
blue.pack(anchor=W)
exit.pack()

window.mainloop()
