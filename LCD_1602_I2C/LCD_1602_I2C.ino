#include <LiquidCrystal_AIP31068_I2C.h>
#include <LiquidCrystal_AIP31068_SPI.h>

LiquidCrystal_AIP31068_I2C lcd(0x3E,20,4);  // set the LCD address to 0x3E for a 20 chars and 4 line display

void setup()
{
  lcd.init();                      // initialize the lcd 
  // Print a message to the LCD.
  lcd.setCursor(1,0);
  lcd.print("Hello, world!");
  lcd.setCursor(1,1);
  lcd.print("From Arduino!");
}


void loop()
{
}