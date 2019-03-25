/*
Controlling LEDs over the Interwebs
*/

int blue = D0;
int green = D3;
int red = D5;

int redState = 0;
int greenState = 0;
int blueState = 0;

void setup()
{
    // Here's the pin configuration, same as last time
    pinMode(blue, OUTPUT);
    pinMode(green, OUTPUT);
    pinMode(red, OUTPUT);

    // We are also going to declare a Particle.function so that we can turn the LED on and off from the cloud.
    Particle.function("toggleLEDs", toggleLED);
    //Particle.function("green",toggleGreen);
    //Particle.function("blue",toggleBlue);
    // This is saying that when we ask the cloud for the function "red",
    //it will employ the function toggleRed() from this app.

    digitalWrite(red, LOW);
    digitalWrite(green, LOW);
    digitalWrite(blue, LOW);

}

// function gets called when a matching API request is sent
int toggleLES(String command) // Particle.function takes a string and returns an integer
{
    if (command == "red")
    {
        digitalWrite(red, (redState) ? HIGH : LOW);
        redState = !redState;
        return 1;
    }
    else if (command == "green")
    {
        digitalWrite(green, (greenState) ? HIGH : LOW);
        greenState = !greenState;
        return 1;
    }
    else if (command == "blue")
    {
        digitalWrite(blue, (blueState) ? HIGH : LOW);
        blueState = !blueState;
        return 1;
    }
    else {
        return -1;
    }
}

void loop()
{
   // do nothing
}
