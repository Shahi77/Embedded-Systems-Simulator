import time

class GPIO:
    def __init__(self):
        self.pins = {}

    def setup(self, pin, value=0):
        self.pins[pin] = value
        print(f"GPIO {pin} set to {value}")

    def write(self, pin, value):
        if self.pins.get(pin) != value:
            self.pins[pin] = value
            print(f"GPIO {pin} set to {value}")

    def read(self, pin):
        return self.pins.get(pin, 0)

class UART:
    def transmit(self, message):
        print(f"[UART TX]: {message}")

class ADC:
    def __init__(self):
        self.temperature = 25.0
        self.direction = 1  # 1: heating, -1: cooling

    def read_temperature(self):
        # Simulate fluctuation when cooling is on
        if self.temperature >= 30.5:
            self.direction = -1
        elif self.temperature <= 27.5:
            self.direction = 1
        self.temperature += 0.6 * self.direction
        return round(self.temperature, 1)

class EmbeddedSystemSimulator:
    def __init__(self):
        self.gpio = GPIO()
        self.uart = UART()
        self.adc = ADC()
        self.virtual_time = 0.0
        self.cooling_pin = 13

    def initialize(self):
        print("=== Starting Embedded System Simulation ===")
        self.gpio.setup(self.cooling_pin, 0)
        self.uart.transmit("SYSTEM BOOT")

    def run(self, duration=10.0, step=0.11):
        self.initialize()
        while self.virtual_time <= duration:
            print(f"\nVirtual Time: {self.virtual_time:.2f}s")
            temp = self.adc.read_temperature()
            print(f"Temperature: {temp}°C")

            if temp >= 30.0 and self.gpio.read(self.cooling_pin) == 0:
                self.gpio.write(self.cooling_pin, 1)
                self.uart.transmit("COOLING ON")
            elif temp < 28.0 and self.gpio.read(self.cooling_pin) == 1:
                self.gpio.write(self.cooling_pin, 0)
                self.uart.transmit("COOLING OFF")

            self.virtual_time += step
            time.sleep(0.01)  # Simulate real-time delay

        print("\nSimulation stopped")
        print("=== Simulation Complete ===")
        print("Final GPIO States:", self.gpio.pins)

if __name__ == "__main__":
    sim = EmbeddedSystemSimulator()
    sim.run()
