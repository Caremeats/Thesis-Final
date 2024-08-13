#include <SparkFun_ADXL345.h> // Include the SparkFun ADXL345 library

ADXL345 adxl = ADXL345(); // Create an instance of the ADXL345 class

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
  adxl.powerOn(); // Turn on the ADXL345 accelerometer
  adxl.setTapThreshold(0); // Reset tap threshold for accelerometer
}

void loop() {
  int sensorValue = analogRead(A0); // Read analog input from pin A0
  float voltage = sensorValue * (9.0 / 1023.0); // Convert analog reading to voltage (0-5V)
  Serial.print("V:"); // Print label indicating voltage
  Serial.println(String(voltage, 2)); // Print voltage value with 2 decimal places
  delay(100); // Delay for 100 milliseconds

  int x, y, z; // Declare variables to store accelerometer readings
  adxl.readAccel(&x, &y, &z); // Read accelerometer values into x, y, and z variables

  float accelx = x * (9.81 / 1000); // Convert x-axis acceleration to m/s^2 where 9.81 is the acceleration due to gravity and 1000 
  float accely = y * (9.81 / 1000); // for scaling factor due to the fact accelerometer readings reach up to negative 32000 positive on so.
                                    // To take calculations to unit of m/2^2 we need to divide by 1000.

  float punchSpeed = sqrt(sq(accelx) + sq(accely)); // Calculate resultant acceleration (magnitude), using pythagorean theorem, 
                                                    //first we take the square root of each reading of X and Y Axis and getting their sum, 
                                                    //then those summed values are squared root once again to obtain resultant acceleration magnitude.
 
  Serial.print("S:"); // Print label indicating punch speed
  Serial.println(String(punchSpeed, 2)); // Print punch speed with 2 decimal places
      
  delay(100); // Delay for 100 milliseconds
}