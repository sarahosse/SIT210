/*
Subscribing to Pats and Waves from Deakin Lab
Written by: Sarah Ossedryver
*/
int green = D3;
int red = D5;
void eventPublished(const char *event, const char *data);
void setup()
{
    Particle.subscribe("Deakin_RIOT_SIT210_Photon_Buddy", eventPublished);
    
    pinMode(green, OUTPUT);
    pinMode(red, OUTPUT);
    digitalWrite(red, LOW);
    digitalWrite(green, LOW);
}
// Particle.subscribe handlers don't return anything; they take event name and data
void eventPublished(const char *event, const char *data)
{
    if (strcmp(data, "wave") == 0)
    {
        // flash LEDs 3 times
        digitalWrite(red, HIGH);
        delay(1000);
        digitalWrite(red, LOW);
    }
    else if (strcmp(data, "pat") == 0)
    {
        // shine for longer
        digitalWrite(green, HIGH);
        delay(1000);
        digitalWrite(green, LOW);
    }
    else
    {
        // nothing
    }
}
void loop()
{
   // do nothing
}
