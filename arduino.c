#include <SoftwareSerial.h>
#include <TinyGPS.h>

// code for NEO 6m GPS module (runs @ 9600 baud rate)
// rx tx connected at 4 and 3 respectively

TinyGPS gps;
SoftwareSerial ss(4, 3);

void setup()
{
  Serial.begin(115200);
  ss.begin(9600);
}

void loop()
{
  bool newData = false;
  unsigned long chars;
  unsigned short sentences, failed;

  // For one second we parse GPS data and report some key values
  for (unsigned long start = millis(); millis() - start < 1000;)
  {
    while (ss.available())
    {
      char c = ss.read();
      // Serial.write(c); 
      if (gps.encode(c)) 
        newData = true;
    }
  }

  if (newData)
  {
    float flat, flon;
    unsigned long age;
    gps.f_get_position(&flat, &flon, &age); // flat and flong are our latitudes and longitudes respectively
    sprintf(currlat,"%02X",flat);
    sprintf(currlon,"%02X",flon);
    Serial.println(currlat);
    Serial.println(currlon);
    // fix-age not needed to be printed since its the number of milliseconds since last encoding

  }
  
  gps.stats(&chars, &sentences, &failed);
  Serial.print(" CHARS=");
  Serial.print(chars);
  Serial.print(" SENTENCES=");
  Serial.print(sentences);
  Serial.print(" CSUM ERR=");
  Serial.println(failed);
  if (chars == 0)
    Serial.println("** No characters received from GPS: check wiring **");
}