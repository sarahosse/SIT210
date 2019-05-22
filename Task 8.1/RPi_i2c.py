/*
    by Sarah Ossedryver
*/


int period = 5000;              // change this if you want to change the period of publishing
const int TMPaddress = 0x48;    // address of TMP102
const int nBytesToRead = 2;     // there are 2 bytes to be read from TMP102
char publishString[30];
int addressSuccess;

void setup()
{
    Serial.begin(9600);
    Wire.begin();               // initialises serial communication library
}


void loop()
{
    // check if a signal is being received from i2c pins
    if (Wire.isEnabled())
    {
        Particle.publish("TMP102", "wire enabled", PRIVATE);
        delay(period/5);
        
        // master (photon) requests bytes from slave (TMP102)
        Wire.requestFrom(TMPaddress, nBytesToRead);
        
        // ensures 2 bytes are available for reading
        if (Wire.available() == nBytesToRead)
        {
            Particle.publish("TMP102", "wire available", PRIVATE);
            delay(period/5);
            byte byte1 = Wire.read();
            byte byte2 = Wire.read();
            
            // removes empty bits from byte 2
            // combines bytes
            // converts to temperature (according to TMP102 datasheet)
            int tempInt = ((( byte1 << 8) | byte2) >> 4) * 0.0625;
            
            snprintf(publishString, sizeof(publishString), "The temperature is %d (C)", tempInt);
            Particle.publish("TMP102", publishString, PRIVATE);
        }
        else
        {
            Particle.publish("TMP102", "wire not available", PRIVATE);
            delay(period/5);
        }
    }
    else
    {
        Wire.begin();
        Particle.publish("TMP102", "the problem is with the wire", PRIVATE);
        delay(period/5);
    }
    
    // wait a period of time
    delay(period);
}
