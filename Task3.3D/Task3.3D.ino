/*
Subscribing to Pats and Waves from Deakin Lab
*/

int blue = D0;
int green = D3;
int red = D5;

int redState = 0;
int greenState = 0;
int blueState = 0;

void eventPublished(const char *event, const char *data);

void setup()
{
    
    Particle.subscribe("Deakin_RIOT_SIT210_Photon_Buddy", eventPublished)
    // Here's the pin configuration, same as last time
    pinMode(blue, OUTPUT);
    pinMode(green, OUTPUT);
    pinMode(red, OUTPUT);

    // Particle.function exposes "toggleLED" to the cloud
    Particle.function("toggleLED", toggleLED);

    digitalWrite(red, LOW);
    digitalWrite(green, LOW);
    digitalWrite(blue, LOW);

}


// Particle.subscribe handlers don't return anything
// they take event name and data

void eventPublished(const char *event, const char *data)
{
    if (strcmp(data, "wave") == 0)
    {
        // flash LEDs 3 times
        toggleLED("red");
        delay(1000);
        toggleLED("red");
    }
    else if (strcmp(data, "pat") == 0)
    {
        // shine for longer
        toggleLED("red");
        delay(5000);
        toggleLED("red");
    }
    else
    {
        // nothing?
    }
}



// function gets called when a matching API request is sent
int toggleLED(String command) // Particle.function takes a string and returns an integer
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
