import machine
import utime
import math
# Constants for enum-like behavior
FILTER_TYPE_LOWPASS = 0
FILTER_TYPE_HIGHPASS = 1
NOTCH_FREQ_50HZ = 50
NOTCH_FREQ_60HZ = 60
SAMPLE_FREQ_500HZ = 500
SAMPLE_FREQ_1000HZ = 1000

# Coefficients of transfer function of LPF
lpf_numerator_coef = [[0.3913, 0.7827, 0.3913], [0.1311, 0.2622, 0.1311]]
lpf_denominator_coef = [[1.0000, 0.3695, 0.1958], [1.0000, -0.7478, 0.2722]]

# Coefficients of transfer function of HPF
hpf_numerator_coef = [[0.8371, -1.6742, 0.8371], [0.9150, -1.8299, 0.9150]]
hpf_denominator_coef = [[1.0000, -1.6475, 0.7009], [1.0000, -1.8227, 0.8372]]

# Coefficients of transfer function of anti-hum filter for 50Hz
ahf_numerator_coef_50Hz = [
    [0.9522, -1.5407, 0.9522, 0.8158, -0.8045, 0.0855],
    [0.5869, -1.1146, 0.5869, 1.0499, -2.0000, 1.0499]
]
ahf_denominator_coef_50Hz = [
    [1.0000, -1.5395, 0.9056, 1.0000 - 1.1187, 0.3129],
    [1.0000, -1.8844, 0.9893, 1.0000, -1.8991, 0.9892]
]
ahf_output_gain_coef_50Hz = [1.3422, 1.4399]

# Coefficients of transfer function of anti-hum filter for 60Hz
ahf_numerator_coef_60Hz = [
    [0.9528, -1.3891, 0.9528, 0.8272, -0.7225, 0.0264],
    [0.5824, -1.0810, 0.5824, 1.0736, -2.0000, 1.0736]
]
ahf_denominator_coef_60Hz = [
    [1.0000, -1.3880, 0.9066, 1.0000, -0.9739, 0.2371],
    [1.0000, -1.8407, 0.9894, 1.0000, -1.8584, 0.9891]
]
ahf_output_gain_coef_60Hz = [1.3430, 1.4206]

class FILTER_2nd:
    def __init__(self):
        self.states = [0, 0]
        self.num = [0, 0, 0]
        self.den = [0, 0, 0]

    def init(self, ftype, sample_freq):
        self.states = [0, 0]
        if ftype == FILTER_TYPE_LOWPASS:
            if sample_freq == SAMPLE_FREQ_500HZ:
                self.num = lpf_numerator_coef[0]
                self.den = lpf_denominator_coef[0]
            elif sample_freq == SAMPLE_FREQ_1000HZ:
                self.num = lpf_numerator_coef[1]
                self.den = lpf_denominator_coef[1]
        elif ftype == FILTER_TYPE_HIGHPASS:
            if sample_freq == SAMPLE_FREQ_500HZ:
                self.num = hpf_numerator_coef[0]
                self.den = hpf_denominator_coef[0]
            elif sample_freq == SAMPLE_FREQ_1000HZ:
                self.num = hpf_numerator_coef[1]
                self.den = hpf_denominator_coef[1]

    def update(self, input_value):
        tmp = (input_value - self.den[1] * self.states[0] - self.den[2] * self.states[1]) / self.den[0]
        output = self.num[0] * tmp + self.num[1] * self.states[0] + self.num[2] * self.states[1]
        self.states[1] = self.states[0]
        self.states[0] = tmp
        return output

class FILTER_4th:
    def __init__(self):
        self.states = [0, 0, 0, 0]
        self.num = [0, 0, 0, 0, 0, 0]
        self.den = [0, 0, 0, 0, 0, 0]
        self.gain = 0

    def init(self, sample_freq, hum_freq):
        self.gain = 0
        self.states = [0, 0, 0, 0]
        if hum_freq == NOTCH_FREQ_50HZ:
            if sample_freq == SAMPLE_FREQ_500HZ:
                self.num = ahf_numerator_coef_50Hz[0]
                self.den = ahf_denominator_coef_50Hz[0]
                self.gain = ahf_output_gain_coef_50Hz[0]
            elif sample_freq == SAMPLE_FREQ_1000HZ:
                self.num = ahf_numerator_coef_50Hz[1]
                self.den = ahf_denominator_coef_50Hz[1]
                self.gain = ahf_output_gain_coef_50Hz[1]
        elif hum_freq == NOTCH_FREQ_60HZ:
            if sample_freq == SAMPLE_FREQ_500HZ:
                self.num = ahf_numerator_coef_60Hz[0]
                self.den = ahf_denominator_coef_60Hz[0]
                self.gain = ahf_output_gain_coef_60Hz[0]
            elif sample_freq == SAMPLE_FREQ_1000HZ:
                self.num = ahf_numerator_coef_60Hz[1]
                self.den = ahf_denominator_coef_60Hz[1]
                self.gain = ahf_output_gain_coef_60Hz[1]

    def update(self, input_value):
        output = 0
        stage_in = 0
        stage_out = self.num[0] * input_value + self.states[0]
        self.states[0] = (self.num[1] * input_value + self.states[1]) - self.den[1] * stage_out
        self.states[1] = self.num[2] * input_value - self.den[2] * stage_out
        stage_in = stage_out
        stage_out = self.num[3] * stage_out + self.states[2]
        self.states[2] = (self.num[4] * stage_in + self.states[3]) - self.den[4] * stage_out
        self.states[3] = self.num[5] * stage_in - self.den[5] * stage_out
        output = self.gain * stage_out
        return output

class EMGFilters:
    def __init__(self):
        self.sample_freq = 0
        self.notch_freq = 0
        self.bypass_enabled = True
        self.notch_filter_enabled = False
        self.lowpass_filter_enabled = False
        self.highpass_filter_enabled = False

    def init(self, sample_freq, notch_freq, enable_notch_filter=True, enable_lowpass_filter=True, enable_highpass_filter=True):
        self.sample_freq = sample_freq
        self.notch_freq = notch_freq
        self.bypass_enabled = True
        if (sample_freq in [SAMPLE_FREQ_500HZ, SAMPLE_FREQ_1000HZ]) and (notch_freq in [NOTCH_FREQ_50HZ, NOTCH_FREQ_60HZ]):
            self.bypass_enabled = False

        self.lpf = FILTER_2nd()
        self.hpf = FILTER_2nd()
        self.ahf = FILTER_4th()

        self.lpf.init(FILTER_TYPE_LOWPASS, self.sample_freq)
        self.hpf.init(FILTER_TYPE_HIGHPASS, self.sample_freq)
        self.ahf.init(self.sample_freq, self.notch_freq)

        self.notch_filter_enabled = enable_notch_filter
        self.lowpass_filter_enabled = enable_lowpass_filter
        self.highpass_filter_enabled = enable_highpass_filter

    def update(self, input_value):
        output = 0
        if self.bypass_enabled:
            return input_value

        if self.notch_filter_enabled:
            output = self.ahf.update(input_value)
        else:
            output = input_value

        if self.lowpass_filter_enabled:
            output = self.lpf.update(output)

        if self.highpass_filter_enabled:
            output = self.hpf.update(output)

        return output

# Constants for hardware configuration
ANALOG_PIN = 26  # Replace with the actual analog pin connected to the EMG sensor
SAMPLE_FREQ = SAMPLE_FREQ_1000HZ  # Adjust based on your application
NOTCH_FREQ = NOTCH_FREQ_50HZ  # Adjust based on your application

# Create instances of the filters
emg_filters = EMGFilters()
emg_filters.init(SAMPLE_FREQ, NOTCH_FREQ, enable_notch_filter=True, enable_lowpass_filter=True, enable_highpass_filter=True)

# Function to read analog signal and apply filters
def filter_emg_signal(emg_filters,i):
    led = machine.Pin('LED', machine.Pin.OUT)
    led.value(False)
    adc = machine.ADC(28)  # Create an ADC channel
    adc1 = machine.ADC(26)
    f=open('/new.csv','a')
    f.write("POT Value 1,POT Value 2\n")
    read_duration = 6  # in seconds
    if i < 1:
        wait_duration=2
    else:
        wait_duration=1
# Get start time
    start_time = utime.time()

# Read sensor values for 3 seconds
    while utime.time() - start_time < read_duration:
        raw_value = adc.read_u16()
        raw_value2 = adc1.read_u16()
        # Apply the filters to the raw analog signal
        filtered_value = emg_filters.update(raw_value)
        # Apply the filters to the raw analog signal
        filtered_value1 = emg_filters.update(raw_value2)
        
        value1 = filtered_value*filtered_value
        value2 = filtered_value1*filtered_value1
        threshold1=0
        threshold2=0
        value3=math.sqrt(value1)
        value4=math.sqrt(value2)
        if(value3 > threshold1 and value4>threshold2 and utime.time() - start_time > wait_duration):
            f.write(str(value3)+","+str(value4)+"\n")
#             print(value1,value2)
            led.value(True)
            print(value3,",",value4,",",i)
#         print(value3,",",value4)

        utime.sleep_ms(100)  # Adjust the sleep duration based on your sampling rate
    f.close()
# Create instances of the filters
emg_filters = EMGFilters()
emg_filters.init(SAMPLE_FREQ, NOTCH_FREQ, enable_notch_filter=True, enable_lowpass_filter=True, enable_highpass_filter=True)

# Run the filter function
for i in range(10):
    filter_emg_signal(emg_filters,i)

