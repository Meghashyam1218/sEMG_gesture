import machine
import utime

# Define the ADC pin (change this based on your connection)
# adc_pin = 26

# Initialize ADC
adc = machine.ADC(28)
# sensor = adc.channel(pin=adc_pin)

# Set the duration for reading (2 seconds)
read_duration = 2  # in seconds

# Get start time
start_time = utime.time()

# Read sensor values for 2 seconds
while utime.time() - start_time < read_duration:
    sensor_value = adc.read_u16()
    print("Sensor Value:", sensor_value)
    utime.sleep_ms(100)  # adjust sleep time as needed for your sensor and application

# End of the script
