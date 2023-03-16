#include <DHT.h>
#include <DHT_U.h>

#define PIN_DHT 2
#define DHT_VERSION DHT22

#define PIN_LED_LIFE 13

#define PIN_LED_1 3
#define PIN_LED_2 4
#define PIN_LED_3 5
#define PIN_LED_4 6
#define PIN_LED_5 7
#define PIN_LED_6 8
#define PIN_LED_7 9
#define PIN_LED_8 10

#define MODBUS_ADD_HIGH 0x30
#define MODBUS_ADD_LOW 0x31

int count = 0;
bool led_life = false;

float temperature = 0.0;
float humidity = 0.0;

const int BUFFER_SIZE = 100;
byte buf[BUFFER_SIZE];

DHT dht(PIN_DHT, DHT_VERSION);

void setup() {
  dht.begin();
	Serial.begin(9600);
	Serial.setTimeout(30000);
  
  pinMode(PIN_LED_LIFE, OUTPUT);

  pinMode(PIN_LED_1, OUTPUT);
  pinMode(PIN_LED_2, OUTPUT);
  pinMode(PIN_LED_3, OUTPUT);
  pinMode(PIN_LED_4, OUTPUT);
  pinMode(PIN_LED_5, OUTPUT);
  pinMode(PIN_LED_6, OUTPUT);
  pinMode(PIN_LED_7, OUTPUT);
  pinMode(PIN_LED_8, OUTPUT);
}

void loop() {

	if (Serial.available() > 0) 
	{
		read();
	 }

	if (count % 500 == 0) {
		led_life = life(led_life);
	}
	
	if (count % 2000 == 0) {
		temperature = dht.readTemperature();
		humidity = dht.readHumidity();
	}
	
	if (count % 10000 == 0) {
		count = 0;
	}
	
	count = count + 100;
	delay(100);
}

bool life(bool led_life) {
	if (led_life) {
		digitalWrite(PIN_LED_LIFE, LOW);
	} else {
		digitalWrite(PIN_LED_LIFE, HIGH);
	}
	return !led_life;
}

void read() {
	int rlen = Serial.readBytesUntil(0x0D, buf, BUFFER_SIZE);
	
	// Check if start with :
	if (buf[0] != 0x3A) {
		return;
	}
	
	// Check if slave is 01
	if (buf[1] != MODBUS_ADD_HIGH && buf[2] != MODBUS_ADD_LOW) {
		return;
	}
	
	// Check if function is 04
	if (buf[3] != 0x30 && buf[4] != 0x34) {
		return;
	}
	
	byte address[] = { buf[5], buf[6], buf[7], buf[8] };
	
	// Check if address is under 10
	if (address[0] != 0x30 || address[1] != 0x30 || address[2] != 0x30) {
		send_read_error();
		return;
	}
	
	switch (address[3]) {
		// Version boitier
		case 0x30:
			send_read_response({0x30});
		break;
		// Température
		case 0x31:
		byte bytes[] = {
			(int) temperature & 0xFF, 
			((int) temperature >> 16) & 0xFF,
			};
			// TODO: Check the data of the temp
			send_read_response(bytes);
		break;
		// Année courante
		case 0x32:
			send_read_response({0x30});
		break;
		// Version boitier
		case 0x33:
			send_read_response({0x30});
		break;
		// Version boitier
		case 0x34:
			send_read_response({0x30});
		break;
		// Version boitier
		case 0x35:
			send_read_response({0x30});
		break;
		// Version boitier
		case 0x36:
			send_read_response({0x30});
		break;
		// Erreur
		default:
			send_read_error();
			return;
	}	
}

void send_read_error() {
	// :
	Serial.print(':');
	// slave
	Serial.print("01");
	// function
	Serial.print("38");
	// Error
	// TODO
	Serial.print("ER");
	// LRC
	// TODO
	Serial.print("LR");
	// CR
	Serial.write(0x0D);
	// LF
	Serial.write(0x0A);
}

void send_read_response(byte bytes[]) {	
	// :
	Serial.print(':');
	// slave
	Serial.print("01");
	// function
	Serial.print("04");
	// Number of bytes
	Serial.print(sizeof(bytes));
	// Bytes
	for (int i = 0; i < sizeof(bytes); i++) {
	  	Serial.write(bytes[i]);
	}
	// LRC
	// TODO
	Serial.print("LR");
	// CR
	Serial.write(0x0D);
	// LF
	Serial.write(0x0A);
}