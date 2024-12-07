from machine import Pin, I2C
import time

# Configuration
I2C_SDA_PIN = 4  # GPIO4 (Pico Physical Pin 6)
I2C_SCL_PIN = 5  # GPIO5 (Pico Physical Pin 7)
I2C_FREQ = 100000  # 100 kHz, suitable for most EEPROMs
EEPROM_ADDRESS = 0x50  # Change if your EEPROM uses a different I2C address

# Initialize I2C
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)

# ANSI Escape Codes for Colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def read_eeprom_data(eeprom_address, start_address, num_bytes):
    """Reads data from the EEPROM via I2C."""
    try:
        i2c.writeto(eeprom_address, bytearray([start_address]))
        data = i2c.readfrom(eeprom_address, num_bytes)
        return list(data)
    except Exception as e:
        print(f"{Colors.FAIL}Error reading EEPROM: {e}{Colors.ENDC}")
        return []

def write_eeprom_data(eeprom_address, start_address, data):
    """Writes data to the EEPROM via I2C."""
    try:
        for i in range(len(data)):
            i2c.writeto(eeprom_address, bytearray([start_address + i, data[i]]))
            time.sleep(0.01)  # Delay for the EEPROM write cycle.
        return True
    except Exception as e:
        print(f"{Colors.FAIL}Error writing to EEPROM: {e}{Colors.ENDC}")
        return False

# Main Function
def main():
    print(f"{Colors.HEADER}EEPROM Cloning Tool{Colors.ENDC}")
    
    #1: Read data from the source EEPROM.
    print(f"{Colors.OKBLUE}Initializing I2C bus...{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Reading data from source EEPROM...{Colors.ENDC}")
    
    start_address = 0x00
    num_bytes = 256  # Adjust based on your EEPROM.
    
    source_data = read_eeprom_data(EEPROM_ADDRESS, start_address, num_bytes)
    
    if not source_data:
        print(f"{Colors.FAIL}Failed to read data from source EEPROM.{Colors.ENDC}")
        return
    
    print(f"{Colors.OKGREEN}Data cached successfully:{Colors.ENDC}")
    print(source_data)
    
    # Prompt to switch EEPROMs / Hashboard.
    input(f"{Colors.WARNING}Please disconnect the source EEPROM and connect the target EEPROM. Press Enter to continue...{Colors.ENDC}")
    
    #2: Write cached data to the target EEPROM / Hashboard.
    print(f"{Colors.OKCYAN}Writing data to the target EEPROM...{Colors.ENDC}")
    success = write_eeprom_data(EEPROM_ADDRESS, start_address, source_data)
    
    if success:
        print(f"{Colors.OKGREEN}Data written successfully to the target EEPROM!{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Failed to write data to the target EEPROM.{Colors.ENDC}")

# Runs The Script
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Colors.WARNING}\nOperation cancelled by user.{Colors.ENDC}")
