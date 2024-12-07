from machine import Pin, I2C
import time

# Configuration
I2C_SDA_PIN = 4  # GPIO4 (Physical pin 6)
I2C_SCL_PIN = 5  # GPIO5 (Physical pin 7)
I2C_FREQ = 100000  # 100 kHz
EEPROM_ADDRESS = 0x50  # I2C address

# Initialize I2C
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)

def crc5(data):
    """Calculate CRC5 checksum for a given data sequence."""
    crc = 0x1F
    for byte in data:
        for _ in range(8):
            bit = ((byte >> 7) & 1) ^ ((crc >> 4) & 1)
            crc = ((crc << 1) & 0x1F) | bit
            if bit:
                crc ^= 0x15
            byte <<= 1
    return crc & 0x1F

def read_eeprom_data(eeprom_address, start_address, num_bytes):
    """Reads data from the EEPROM via I2C."""
    try:
        i2c.writeto(eeprom_address, bytearray([start_address]))
        data = i2c.readfrom(eeprom_address, num_bytes)
        return list(data)
    except Exception as e:
        print(f"Error reading EEPROM: {e}")
        return []

def parse_data(data):
    """Parse the EEPROM data to extract known values."""
    result = {}
    try:
        # Extract raw serial number bytes for manual inspection
        serial_bytes = data[4:21]
        result["serial_number_raw"] = serial_bytes
        result["serial_number_ascii"] = ''.join(chr(b) if 32 <= b <= 126 else '?' for b in serial_bytes)
        
        # Extract product ID as raw bytes
        product_bytes = data[21:25]
        result["product_id_raw"] = product_bytes
        result["product_id_ascii"] = ''.join(chr(b) if 32 <= b <= 126 else '?' for b in product_bytes)

        # Decode BOM, PCB, and Fixture Versions as hexadecimal values
        bom_version = (data[25] << 8) | data[26]
        pcb_version = (data[27] << 8) | data[28]
        fixture_version = (data[29] << 8) | data[30]
        
        result["bom_version_hex"] = f"0x{bom_version:04X}"
        result["pcb_version_hex"] = f"0x{pcb_version:04X}"
        result["fixture_version_hex"] = f"0x{fixture_version:04X}"
        
        # CRC5 Calculations
        result["crc5_fixture_header"] = crc5(data[0:4])
        result["crc5_cgminer_header"] = crc5(data[4:64])  # Example range
        result["crc5_class_info"] = crc5(data[64:128])   # Example range
        
    except Exception as e:
        print(f"Error parsing data: {e}")
    return result

# Main function
def main():
    print("Initializing EEPROM reader...")
    start_address = 0x00
    num_bytes = 256

    print(f"Reading {num_bytes} bytes starting from address {start_address}...")
    data = read_eeprom_data(EEPROM_ADDRESS, start_address, num_bytes)
    
    if data:
        print(f"Read data: {data}")
        parsed_data = parse_data(data)
        print("\nExtracted Values:")
        for key, value in parsed_data.items():
            print(f"{key}: {value}")
    else:
        print("Failed to read data from EEPROM.")

# Run the script
if __name__ == "__main__":
    main()
