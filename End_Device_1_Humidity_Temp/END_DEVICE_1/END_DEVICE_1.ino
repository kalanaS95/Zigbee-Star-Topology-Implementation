#include <Wire.h>
#include <SoftwareSerial.h>
#include <string.h>
#include <dht.h>
#define rxPin 2
#define txPin 3
SoftwareSerial xbee =  SoftwareSerial(rxPin, txPin);

//temp sensor initialization.
dht DHT;
#define DHT11_PIN A0

////////////////////////////////////////////// API FRAME BUILDING AND SENDING PART //////////////////////////////////////////////  

// includes up to Options field in the API frame (Size is constant, always 17 bytes)
byte API_Frame_part1[] = {0x7E, 0x00, 0x00, 0x10, 0x01, 0x00, 0x13, 0xA2, 0x00, 0x41, 0xCC, 0x41, 0xA3, 0xFF, 0xFE, 0x00, 0x00};
int curr_API_Frame_length = 14; //exlcluding first 3 bytes (used for frame length calculation)
//this will hold the data section of the API frame
byte* data_field;
int data_field_len = 0;
byte* zigbee_API_Frame;

   
void construct_data(char data[])
{
  int string_len = strlen(data);
  data_field_len = string_len;
  data_field = (byte*)malloc(sizeof(byte) * string_len);
  for(int x=0; x < string_len; x++)
    data_field[x]=data[x];
}

unsigned char calculate_checksum()
{
  int currSum = 0;
  // calculate checksum for the first part of the frame
  for(int x=3; x<17; x++)
    currSum += API_Frame_part1[x];

  //calculate checksum for the data part
  for(int x=0; x<data_field_len; x++)
    currSum += data_field[x];

  return 0xFF - (currSum & 0xFF);
}

void calculate_frame_length()
{
  int total_frame_length = curr_API_Frame_length + data_field_len;
  if(total_frame_length <= 255)
    API_Frame_part1[2] = (unsigned char)total_frame_length;
  else
  {
    // in case value is more than 255 get lower and upper parts of the hex number. Since byte is only 8 bits !
    API_Frame_part1[2] = (unsigned char)(total_frame_length & 0xff); //get the lower part
    API_Frame_part1[1] = (unsigned char)(total_frame_length >> 8);
  }
}


// function will construct the Zigbee API frame and return its length
int construct_Zigbee_API_frame(char data[])
{
  //construct the data part of the frame
  construct_data(data);
  //calculate frame length
  calculate_frame_length();

  zigbee_API_Frame = (byte*)malloc(sizeof(byte)*(17 + data_field_len + 1));
  int count = 0;
  //copying first part of the frame
  for(count; count<17; count++)
    zigbee_API_Frame[count] = API_Frame_part1[count];
 
  //copying data part of the frame
  int x=0;
  for(count,x; count<17+data_field_len; count++,x++)
    zigbee_API_Frame[count] = data_field[x];

  //finally add the checksum
  zigbee_API_Frame[count] = calculate_checksum();

  return count + 1;
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 



void setup(){
 pinMode(rxPin, INPUT);
 pinMode(txPin, OUTPUT);
 xbee.begin(9600);
 Serial.begin(9600);
}

void loop(){

 
 int chk = DHT.read11(DHT11_PIN);
 Serial.print("Temperature = ");
 Serial.println(DHT.temperature);
 Serial.print("Humidity = ");
 Serial.println(DHT.humidity);
 
 char buffer[100];
 sprintf(buffer, "Temperature:%d°C, Humidity:%d%%", (int)DHT.temperature, (int)DHT.humidity);

 int frame_size = construct_Zigbee_API_frame(buffer);
 xbee.write(zigbee_API_Frame,frame_size);
 free(data_field);
 free(zigbee_API_Frame);
 delay(20000);
  

  
  
 
}
