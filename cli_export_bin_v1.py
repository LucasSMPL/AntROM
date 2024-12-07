from machine import Pin, I2C

# Configuration
I2C_SDA_PIN = 4  # GPIO4 (Physical pin 6)
I2C_SCL_PIN = 5  # GPIO5 (Physical pin 7)
I2C_FREQ = 100000  # 100 kHz, suitable for most EEPROMs
EEPROM_ADDRESS = 0x50  # EEPROM I2C Address

# Initialize I2C
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)

def read_eeprom_data(eeprom_address, start_address, num_bytes):
    """Reads data from the EEPROM via I2C."""
    try:
        i2c.writeto(eeprom_address, bytearray([start_address]))
        data = i2c.readfrom(eeprom_address, num_bytes)
        return list(data)
    except Exception as e:
        print(f"Error reading EEPROM: {e}")
        return []

def dump_to_terminal(data):
    """Output the EEPROM data in binary format for saving."""
    binary_data = bytearray(data)  # Convert to binary format
    print("EEPROM Data (Binary):")
    print(binary_data.hex())  # Output as a hex string for easy saving
    print("\n--- Copy the above hex data and save it as a .bin file ---")

def main():
    print("Reading EEPROM data...")
    start_address = 0x00
    num_bytes = 256  # Adjust based on your EEPROM size

    data = read_eeprom_data(EEPROM_ADDRESS, start_address, num_bytes)
    
    if data:
        print("EEPROM data read successfully.")
        dump_to_terminal(data)
    else:
        print("Failed to read EEPROM data.")

# Run the script
if __name__ == "__main__":
    main()
