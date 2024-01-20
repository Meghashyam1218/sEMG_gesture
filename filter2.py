import machine
import utime

# Constants for hardware configuration
ANALOG_PIN = 26  # Replace with the actual analog pin connected to the EMG sensor
SAMPLE_FREQ = 1000  # Adjust based on your application
NOTCH_FREQ = 60  # Adjust based on your application

class FILTER_2nd:
    def __init__(self, ftype, sample_freq):
        self.states = [0, 0]
        self.num = [0, 0, 0]
        self.den = [0, 0, 0]
        self.init(ftype, sample_freq)

    def init(self, ftype, sample_freq):
        self.states = [0, 0]
        if ftype == "lowpass":
            if sample_freq == 500:
                self.num = [0.3913, 0.7827, 0.3913]
                self.den = [1.0000, 0.3695, 0.1958]
            elif sample_freq == 1000:
                self.num = [0.1311, 0.2622, 0.1311]
                self.den = [1.0000, -0.7478, 0.2722]
        elif ftype == "highpass":
            if sample_freq == 500:
                self.num = [0.8371, -1.6742, 0.8371]
                self.den = [1.0000, -1.6475, 0.7009]
            elif sample_freq == 1000:
                self.num = [0.9150, -1.8299, 0.9150]
                self.den = [1.0000, -1.8227, 0.8372]

    def update(self, input_value):
        tmp = (input_value - self.den[1] * self.states[0] - self.den[2] * self.states[1]) / self.den[0]
        output = self.num[0] * tmp + self.num[1] * self.states[0] + self.num[2] * self.states[1]
        self.states[1] = self.states[0]
        self.states[0] = tmp
        return output

class EMGFilters:
    def __init__(self, sample_freq, notch_freq):
        self.sample_freq = sample_freq
        self.notch_freq = notch_freq
        self.bypass_enabled = True
        self.notch_filter_enabled = False
        self.lowpass_filter_enabled = False
        self.highpass_filter_enabled = False
        self.lpf = FILTER_2nd("lowpass", sample_freq)
        self.hpf = FILTER_2nd("highpass", sample_freq)

    def init(self, enable_notch_filter=True, enable_lowpass_filter=True, enable_highpass_filter=True):
        self.bypass_enabled = True
        if (self.sample_freq in [500, 1000]) and (self.notch_freq in [50, 60]):
            self.bypass_enabled = False

        self.notch_filter_enabled = enable_notch_filter
        self.lowpass_filter_enabled = enable_lowpass_filter
        self.highpass_filter_enabled = enable_highpass_filter

    def update(self, input_value):
        output = 0
        if self.bypass_enabled:
            return input_value

        if self.lowpass_filter_enabled:
            output = self.lpf.update(input_value)

        if self.highpass_filter_enabled:
            output = self.hpf.update(output)

        return output

# Create instances of the filters
emg_filters = EMGFilters(SAMPLE_FREQ, NOTCH_FREQ)
emg_filters.init(enable_notch_filter=True, enable_lowpass_filter=True, enable_highpass_filter=True)

# Function to read analog signal and apply filters
def filter_emg_signal(emg_filters):
    adc = machine.ADC(26)  # Create an ADC object
#     pin = machine.Pin(26)  # Specify the analog pin
#     adc_c = adc.channel(pin=pin)  # Create an ADC channel

    while True:
        raw_value = adc.read_u16()

        # Apply the filters to the raw analog signal
        filtered_value = emg_filters.update(raw_value)

        # Print or process the filtered value as needed
        print(filtered_value)

        utime.sleep_ms(10)  # Adjust the sleep duration based on your sampling rate

# Run the filter function
filter_emg_signal(emg_filters)
