/*
Periodically Publish Temperature to ThingSpeak
Written by: Sarah Ossedryver
*/

double lightSensor = A0;
int period = 1000;          // change this if you want to change the period of publishing
double lightValue = 1500;      // this value is judged to be the approximation of "direct" sunlight
bool statusOfLight = 0;

// function for reading and returning the value 
double getLight()
{
    double lightValue = analogRead(lightSensor);
    return (lightValue);
    
}

// initialises the light sensor
void setup()
{
    pinMode(lightSensor, INPUT);
}

// continuously loops through this code, publishing the value returned from getTemp
void loop()
{
    if (getLight() > lightValue && statusOfLight == 0)
    {
        Particle.publish("Sunlight", "Terrarium is sunbaking", PRIVATE);
        statusOfLight = 1;
    }
    if (getLight() < lightValue && statusOfLight == 1)
    {
        Particle.publish("Sunlight", "Terrarium in shade", PRIVATE);
        statusOfLight = 0;
    }
    delay(period);
}
