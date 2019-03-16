
// Written by Sarah Ossedryver
// Task 2.1P for SIT210
// Deakin University T1, 2019


// Everyone knows the drill. Code blinks 'SARAH' in Morse Code repeatedly.

// MORSE CODE INFO:
//      If the duration of a dot is taken to be one unit then that of a dash is three units.
//      The space between the components of one character is one unit.
//      The space between characters is three units.
//      The space between words is seven units.


int LED = D7; // built-in LED
int unit = 500; // unit duration

// initiate built-in LED
void setup()
{
   pinMode(LED, OUTPUT);
}


// blinks a dot
void dot()
{
    digitalWrite(LED, HIGH);
    delay(unit);
    digitalWrite(LED, LOW);
    delay(unit);
}

// blinks a dash
void dash()
{
    digitalWrite(LED, HIGH);
    delay(unit*3);
    digitalWrite(LED, LOW);
    delay(unit);
}

// longer break for a new character (3 units)
void new_char()
{
    delay(unit*2);
}

// longer break for a new word (7 units)
void new_word()
{
    delay(unit*6);
}

// currently spells SARAH on loop
void loop() {
    
    // S ( ... )
    dot();
    dot();
    dot();
    
    new_char();
    
    // A ( . _ )
    dot();
    dash();
    
    new_char();
    
    // R ( . _ . )
    dot();
    dash();
    dot();
    
    new_char();
    
    // A ( . _ )
    dot();
    dash();
    
    new_char();
    
    // H ( .... )
    dot();
    dot();
    dot();
    dot();
    
    new_word();
}
