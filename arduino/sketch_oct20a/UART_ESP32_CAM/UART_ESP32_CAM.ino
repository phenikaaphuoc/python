// CAM

#define DEBUG_ESP              //comment out to deactivate debug console

#ifdef DEBUG_ESP
  #define pDBGln(x) Serial.println(x)
  #define pDBG(x)   Serial.print(x)
#else 
  #define pDBG(...)
  #define pDBGln(...)
#endif

#include "esp_camera.h"
#include "Arduino.h"
#include "soc/soc.h"           // Disable brownour problems
#include "soc/rtc_cntl_reg.h"  // Disable brownour problems
#include "driver/rtc_io.h"
#include "SerialTransfer.h"

// Pin definition for CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

SerialTransfer myTransfer;
HardwareSerial Comm(1);
struct img_meta_data{
  uint16_t counter;
  uint16_t imSize;
  uint16_t numLoops;
  uint16_t sizeLastLoop;
} ImgMetaData;
const uint16_t PIXELS_PER_PACKET = MAX_PACKET_SIZE - sizeof(ImgMetaData);

void setup(){
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //disable brownout detector
 
  Serial.begin(115200);                     // Define and start serial monitor
  // 115200,256000,512000,962100
  Comm.begin(962100, SERIAL_8N1,15,14);     //, Comm_Txd_pin, Comm_Rxd_pin); // Define and start Comm serial port
  myTransfer.begin(Comm);
 
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
 

  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 6;              // tỉ lệ nén khi chuyển sang JPEG, tỉ lệ càng cao, chất lượng càng thấp 
  config.fb_count = 1;                
 
  // Init Camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK){
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
}

void loop(){
  uint16_t startIndex = 0;
  camera_fb_t * fb = NULL;
  //Take Picture with Camera
  fb = esp_camera_fb_get(); 
   
  ImgMetaData.imSize       = fb->len;                             //sizeof(myFb);
  ImgMetaData.numLoops     = (fb->len / PIXELS_PER_PACKET) + 1;   //(sizeof(myFb)/PIXELS_PER_PACKET) + 1; 
  ImgMetaData.sizeLastLoop = fb->len % PIXELS_PER_PACKET;         //(sizeof(myFb)%PIXELS_PER_PACKET);

  // // gui tin hieu do dai mang truoc khi gui anh
  // uint16_t imgsize = fb->len;
  // myTransfer.txObj(imgsize, sizeof(imgsize));
  // myTransfer.sendData(sizeof(imgsize));
  // delay(200);

  for(ImgMetaData.counter=1; ImgMetaData.counter<=ImgMetaData.numLoops; ImgMetaData.counter++){
    myTransfer.txObj(ImgMetaData, sizeof(ImgMetaData));
    stuffPixels(fb->buf, startIndex, sizeof(ImgMetaData), PIXELS_PER_PACKET);
    myTransfer.sendData(MAX_PACKET_SIZE);
     
    pDBGln(F("Sent:"));
    // kết hợp mỗi 2 bit liên tiếp để lấy 16 bit cho các giá trị của metaData 
    pDBG(F("img.counter: "));      pDBGln((uint16_t)((myTransfer.txBuff[1] << 8) | myTransfer.txBuff[0]));
    pDBG(F("img.imSize: "));       pDBGln((uint16_t)((myTransfer.txBuff[3] << 8) | myTransfer.txBuff[2]));
    pDBG(F("img.numLoops: "));     pDBGln((uint16_t)((myTransfer.txBuff[5] << 8) | myTransfer.txBuff[4]));
    pDBG(F("img.sizeLastLoop: ")); pDBGln((uint16_t)((myTransfer.txBuff[7] << 8) | myTransfer.txBuff[6]));

    startIndex += PIXELS_PER_PACKET;    
    delay(100);
    //printBuf();  
  }
  esp_camera_fb_return(fb);   //clear camera memory
  delay(2000);
}

void printStructBuf(){
  pDBG(F("Internal Struct: { "));
  for (uint16_t k=0; k<sizeof(ImgMetaData); k++){
    pDBG(myTransfer.txBuff[k]);
    if (k<(sizeof(ImgMetaData)-1))
      pDBG(F(", "));
    else
      pDBGln(F(" }"));
  }
}

void printBuf(){
  pDBG(F("Pixel Values: { "));
  for (uint16_t k=8; k<MAX_PACKET_SIZE; k++){
    pDBG(myTransfer.txBuff[k]);
    if (k < (MAX_PACKET_SIZE - 1))
      pDBG(F(", "));
    else
      pDBGln(F(" }"));
  }
  pDBGln();
}

void stuffPixels(const uint8_t * pixelBuff, const uint16_t &bufStartIndex, const uint16_t &txStartIndex, const uint16_t &len){
  uint16_t txi = txStartIndex;
  for (uint16_t i=bufStartIndex; i<(bufStartIndex + len); i++)  {
    myTransfer.txBuff[txi] = pixelBuff[i];
    txi++;
  }
}