
#define VOLTAGE_1 A1

unsigned long time;

int NUM_SAMPLES = 20;
char clocktime;
char time_t;
float sum1 = 0;     // sum of samples from A1

float R1 = 1000000.00;  
float R2 = 100000.00;

int sample_count = 0;       // current sample number

float V1_ave = 0;
float V1_out = 0;
float V1 = 0.0;       // calculated voltage

void setup() {
  Serial.begin(9600);
   // Start up the library 
}

void loop(void) 
{
while (sample_count < NUM_SAMPLES) 
    {
        sum1 += analogRead(A1);
        sample_count++;
        delay(10);
    }
  V1_ave = float(sum1) / float(NUM_SAMPLES);
  V1_out = V1_ave * 5 / 1024;     
  V1 = V1_out / (R2/(R1+R2));
 
  Serial.println(V1,2);
  sample_count = 0;
  sum1 = 0;
  delay(1000);
}
