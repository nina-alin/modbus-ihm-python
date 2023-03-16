#define PIN_LED 5
 
void setup()
{
	pinMode(PIN_LED,OUTPUT);
}

void loop()
{
	digitalWrite(PIN_LED,HIGH);
	delay(500);
	digitalWrite(PIN_LED,LOW);
	delay(500);
}