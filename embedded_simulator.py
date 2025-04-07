import time

# Virtual GPIO class
class VirtualGPIO:
    def __init__(self):
        self.pins = {}

    def write(self, pin, value):
        self.pins[pin] = value
        print(f"GPIO {pin} set to {value}")

    def read(self, pin):
        return self.pins.get(pin, 0)

# Virtual UART class
class VirtualUART:
    def send(self, message):
        print(f"[UART TX]: {message}")

# Virtual ADC class (e.g., temperature sensor)
class VirtualADC:
    def __init__(self):
        self.sensors = {0: 25.0}  # Start at 25°C

    def read(self, channel):
        return self.sensors.get(channel, 0.0)

# Virtual time manager
class VirtualTime:
    def __init__(self):
        self.start_time = time.time()

    def elapsed(self):
        return time.time() - self.start_time

# Initialize virtual components
gpio = VirtualGPIO()
uart = VirtualUART()
adc = VirtualADC()
vtime = VirtualTime()

# State tracking
last_cooling_state = None

# User-defined main loop
def user_loop():
    global last_cooling_state

    temp = adc.read(0)
    print(f"Temperature: {temp:.1f}°C")

    if temp >= 30.5:
        gpio.write(13, 1)
        if last_cooling_state != 1:
            uart.send("COOLING ON")
            last_cooling_state = 1
        adc.sensors[0] -= 0.6  # Cooling effect
    elif temp <= 28.0:
        gpio.write(13, 0)
        if last_cooling_state != 0:
            uart.send("COOLING OFF")
            last_cooling_state = 0
    else:
        if gpio.read(13) == 1:
            adc.sensors[0] -= 0.6  # Cooling continues

    # Simulate heating when cooling is OFF
    if gpio.read(13) == 0:
        adc.sensors[0] += 0.5  # Environment heats up

# Main simulation loop
def run_simulation(timeout=10.0, interval=0.1):
    print("=== Starting Embedded System Simulation ===")
    gpio.write(13, 0)
    uart.send("SYSTEM BOOT")

    while True:
        elapsed = vtime.elapsed()
        if elapsed > timeout:
            break
        print(f"\nVirtual Time: {elapsed:.2f}s")
        user_loop()
        time.sleep(interval)

    print("\nSimulation stopped")
    print("=== Simulation Complete ===")
    print(f"Final GPIO States: {gpio.pins}")
    print(f"Final Temperature: {adc.sensors[0]:.2f}°C")

# Run the simulation
if __name__ == "__main__":
    run_simulation()
