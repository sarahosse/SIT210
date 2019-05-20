// These #include statements were automatically added by the Particle IDE.
#include <HC_SR04.h>
#include <ThingSpeak.h>

TCPClient client;

// APIs
unsigned long NightChannel = 783583;
const char * NightAPI = "M327H552G27A4HSI";

unsigned long DayChannel = 783772;
const char * DayAPI = "RZX2M3UOKCQRVE8B";

unsigned long ledChannel = 783852;
const char * ledAPI = "BZYFZPYEXU4RDYI6";

// LED pins
int YELLOW = D0;
int ORANGE = D1;
int RED = D2;

// Sensor pins
int TRIG = D4;
int ECHO = D5;
HC_SR04 rangeFinder = HC_SR04(TRIG, ECHO);

// variables for storing present and past distance, and others
int previousCM = 0;
int currentCM = 0;

int movementCounter = 0;
int secondsFromSleepInitiation = 0;
int percentOfMovement = 0;


void setup()
{
    // wait 10 seconds for sensor to settle
    delay(10000);
    
    // set LEDS as output
    pinMode(YELLOW, OUTPUT);
    pinMode(ORANGE, OUTPUT);
    pinMode(RED, OUTPUT);
    
    // set LEDS as off
    digitalWrite(YELLOW, LOW);
    digitalWrite(ORANGE, LOW);
    digitalWrite(RED, LOW);
    
    // set initial distance
    previousCM = rangeFinder.getDistanceCM();
    
    // initialise TS library and settings
    ThingSpeak.begin(client);
}


void loop()
{
    // retrieve the time of the last button presses for nighttime and morning
    String StartNightTime = ThingSpeak.readCreatedAt(NightChannel, NightAPI);
    String StopNightTime = ThingSpeak.readCreatedAt(DayChannel, DayAPI);
  
    // ITS NIGHT TIME; LET THE FESTIVITIES COMMENCE!!! ---------------------------------------------
    
    // if night time has been signalled, we can commence meausuring movement
    while (StartNightTime > StopNightTime)
    {
        // get current distance
        currentCM = rangeFinder.getDistanceCM();
      
        // publish the distance
        Particle.publish("Distance", (String) currentCM), PRIVATE;
      
        // check if distance is the same as last second
        if (currentCM != previousCM)
        {
            // add onto the movement counter
            movementCounter++;
        }
        
        // temporarily store dist. to be compared against next dist.
        previousCM = currentCM;
    
        // add a second onto sleep time counter
        secondsFromSleepInitiation++;
    
        // wait until at least 3 hrs of sleep has passed
        if (secondsFromSleepInitiation > 10800)
        {
            // checks how much movement has happened in prior 10 minutes
            if (secondsFromSleepInitiation % 600 == 0)
            {
                // calculates percent of movement in previous 10 minutes
                percentOfMovement = movementCounter/6;
                Particle.publish("Movement", (String) percentOfMovement, PRIVATE);
                movementCounter = 0;
            }
        }
        
        // ALARM SOUNDS + LEDs ON --------------------------------------------------------------------
        
        // Pi sends a "1" 5 seconds before it starts alarm
        if (ThingSpeak.readIntField(ledChannel, 1, ledAPI) == 1)
        {
            digitalWrite(YELLOW, HIGH);
            digitalWrite(ORANGE, HIGH);
            digitalWrite(RED, HIGH);
        }
        
        // LEDs FLASH WHILE MICROPHONE RECORDS -------------------------------------------------------

        // LEDs will flash while microphone is recording
        else if (ThingSpeak.readIntField(ledChannel, 1, ledAPI) == 2)
        {
            while (ThingSpeak.readIntField(ledChannel, 1, ledAPI) == 2)
            {
                digitalWrite(YELLOW, LOW);
                digitalWrite(ORANGE, LOW);
                digitalWrite(RED, LOW);
                delay(1000);
                digitalWrite(YELLOW, HIGH);
                digitalWrite(ORANGE, HIGH);
                digitalWrite(RED, HIGH);
                delay(1000);
            }
        }
        
        // RECORDING STOPPED, LEDs OFF  --------------------------------------------------------------

        // keep LEDs off (or turn them off)
        else if (ThingSpeak.readIntField(ledChannel, 1, ledAPI) == 0)
        {
            digitalWrite(YELLOW, LOW);
            digitalWrite(ORANGE, LOW);
            digitalWrite(RED, LOW);
        }
        
        // check if morning button has been pressed
        StopNightTime = ThingSpeak.readCreatedAt(DayChannel, DayAPI);
    
        // check distance every second
        delay(1000);
    }
    
    // IT IS DAY TIME! -----------------------------------------------------------
    
    Particle.publish("Daytime", (String) "I'm listening for a button, maybe?", PRIVATE);
    
    // check every five minutes during the day
    delay(300000);
}
