void setup()
{
	pinMode(5,OUTPUT);
	pinMode(6,OUTPUT);
	pinMode(7,OUTPUT);
	pinMode(8,OUTPUT);
	pinMode(9,OUTPUT);
	pinMode(10,OUTPUT);
	pinMode(11,OUTPUT);
	pinMode(12,OUTPUT);
}

void loop()
{
	clignoteInChain();
	// clignoteAll();
}

void clignoteAll() 
{
	digitalWrite(5,HIGH);
	digitalWrite(6,HIGH);
	digitalWrite(7,HIGH);
	digitalWrite(8,HIGH);
	digitalWrite(9,HIGH);
	digitalWrite(10,HIGH);
	digitalWrite(11,HIGH);
	digitalWrite(12,HIGH);
	delay(500);
	digitalWrite(5,LOW);
	digitalWrite(6,LOW);
	digitalWrite(7,LOW);
	digitalWrite(8,LOW);
	digitalWrite(9,LOW);
	digitalWrite(10,LOW);
	digitalWrite(11,LOW);
	digitalWrite(12,LOW);
	delay(500);

}

void clignoteInChain() 
{
	digitalWrite(5,HIGH);
	delay(500);
	digitalWrite(5,LOW);
	digitalWrite(6,HIGH);
	delay(500);
	digitalWrite(6,LOW);
	digitalWrite(7,HIGH);
	delay(500);
	digitalWrite(7,LOW);
	digitalWrite(8,HIGH);
	delay(500);	
	digitalWrite(8,LOW);
	digitalWrite(9,HIGH);
	delay(500);	
	digitalWrite(9,LOW);
	digitalWrite(10,HIGH);
	delay(500);	
	digitalWrite(10,LOW);
	digitalWrite(11,HIGH);
	delay(500);		
	digitalWrite(11,LOW);
	digitalWrite(12,HIGH);
	delay(500);	
	digitalWrite(12,LOW);
}