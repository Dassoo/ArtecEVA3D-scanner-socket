import serial
import time

# 30° rotation per iteration
iterations = 1

for i in range(iterations):
    try:
        ser = serial.Serial('/dev/ttyUSB0', baudrate=38400, timeout=1,
                            bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE)

        ser.write(b'@0G1\r')
        print("Command sent: @0G1\r")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

    # time needed for the single 30° rotation (avoid commands overlap)
    # time.sleep(8)
