/*
Controlling LEDs over the Interwebs
Written by: Sarah Ossedryver
*/

int blue = D0;
int green = D3;
int red = D5;
//int builtIn = D7;

int redState = 0;
int greenState = 0;
int blueState = 0;

void setup()
{
    // Here's the pin configuration, same as last time
    pinMode(blue, OUTPUT);
    pinMode(green, OUTPUT);
    pinMode(red, OUTPUT);
    //pinMode(builtIn, OUTPUT);

    // Particle.function exposes "toggleLED" to the cloud
    Particle.function("led", toggleLED);

    digitalWrite(red, LOW);
    digitalWrite(green, LOW);
    digitalWrite(blue, LOW);

}

// function gets called when a matching API request is sent
int toggleLED(String command) // Particle.function takes a string and returns an integer
{
    if (command == "red")
    {
        redState = !redState;
        digitalWrite(red, (redState) ? HIGH : LOW);
        return 1;
    }
    else if (command == "green")
    {
        greenState = !greenState;
        digitalWrite(green, (greenState) ? HIGH : LOW);

        return 2;
    }
    else if (command == "blue")
    {
        blueState = !blueState;
        digitalWrite(blue, (blueState) ? HIGH : LOW);
        return 3;
    }
    else {
        return -1;
    }
}

void loop()
{
   // do nothing
}
