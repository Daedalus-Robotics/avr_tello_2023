import serial.tools.list_ports

ser = serial.Serial()


def configure(com, baud=115200):
    ser.baudrate = baud
    ser.port = com


def close_dropper() -> bool:
    ser.open()

    if ser.is_open:
        ser.write(b"2")
        ser.close()
        return True

    return False


def open_dropper() -> bool:
    ser.open()

    if ser.is_open:
        ser.write(b"1")
        ser.close()

        return True

    return False


def scan_ports(keyw="CP2104"):
    ports = serial.tools.list_ports.comports()
    pts = [port for port, desc, _ in sorted(ports) if keyw in desc]
    return pts
