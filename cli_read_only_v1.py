from machine import Pin, I2C
import time

# Configuration
I2C_SDA_PIN = 4  # GPIO4 (Physical pin 6)
I2C_SCL_PIN = 5  # GPIO5 (Physical pin 7)
I2C_FREQ = 100000  # 100 kHz, suitable for most EEPROMs
EEPROM_ADDRESS = 0x50  # Change if your EEPROM uses a different I2C address

# Initialize I2C
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)

def read_eeprom_data(eeprom_address, start_address, num_bytes):
    """Reads data from the EEPROM via I2C.
    
    Args:
        eeprom_address (int): I2C address of the EEPROM.
        start_address (int): Starting address to read from in the EEPROM.
        num_bytes (int): Number of bytes to read.
    
    Returns:
        list: A list of bytes read from the EEPROM.
    """
    try:
        # Send The Starting Address
        i2c.writeto(eeprom_address, bytearray([start_address]))
        
        # Read The Specified Number of Bytes
        data = i2c.readfrom(eeprom_address, num_bytes)
        
        return list(data)
    except Exception as e:
        print(f"Error reading EEPROM: {e}")
        return []

# Main Function
def main():
    print("Initializing EEPROM Reader...")
    
    start_address = 0x00  
    num_bytes = 256     
    
    print(f"Reading {num_bytes} bytes starting from address {start_address}...")
    
    # Read Data
    data = read_eeprom_data(EEPROM_ADDRESS, start_address, num_bytes)
    
    if data:
        print(f"Read data: {data}")
    else:
        print("Failed to read data from EEPROM.")

# Run Script
if __name__ == "__main__":
    main()
