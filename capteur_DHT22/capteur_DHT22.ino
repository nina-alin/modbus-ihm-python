#include "DHT.h"

#define PIN_DHT22 2
#define PIN_LED 4

DHT dht(PIN_DHT22, DHT22);

void setup() 
{
   	dht.begin();
	pinMode(PIN_LED, OUTPUT);
}

void loop() {
   float t = dht.readTemperature();
   if (t > 24) {
	digitalWrite(PIN_LED, HIGH);
	} else {
	digitalWrite(PIN_LED, LOW);
	}
	delay(500);
}