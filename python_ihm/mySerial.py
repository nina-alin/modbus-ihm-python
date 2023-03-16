import serial
from enum import Enum
from datetime import datetime
from flask import current_app, g


def get_serial():
    if 'serial' not in g:
        g.serial = serial.Serial(
            port=current_app.config['SERIAL_PORT'],
            baudrate=current_app.config['SERIAL_BAUDRATE'],
            parity=current_app.config['SERIAL_PARITY'],
            stopbits=current_app.config['SERIAL_STOPBITS'],
            bytesize=current_app.config['SERIAL_BYTESIZE'],
            timeout=current_app.config['SERIAL_TIMEOUT']
        )

    return g.serial


def close_serial(e=None):
    ser = g.pop('serial', None)

    if ser is not None:
        ser.close()


# TODO: enum to check serial function code
def send_serial(ser, cmd):
    # print("Sending data")
    # print(f"Command: {cmd[:-2]}")
    cmd = [ord(c) for c in cmd]
    # print(f"Data: {cmd}")
    # print(f"Hex: {[hex(x) for x in cmd]}")

    ser.write(cmd)


def read_serial(ser):
    # print(f"Start receiving")
    data = ser.read_until(expected=serial.LF)
    # print(f"Data: {data.decode('utf-8')}")
    return data.decode("utf-8")


def calculate_lrc(data):
    lrc = 0
    for i in range(0, len(data), 2):
        lrc = lrc + int(data[i: i + 2], 16)

    lrc = (~lrc + 1) & 0xff

    return f"{lrc:02X}"


def read_input_register(ser, address, number, slave="01"):
    content = f"{slave}04{address}{number}"
    lrc = calculate_lrc(content)
    cmd = f":{content}{lrc}\r\n"

    send_serial(ser, cmd)
    return read_serial(ser)


def read_holding_register(ser, address, number, slave="01"):
    content = f"{slave}03{address}{number}"
    lrc = calculate_lrc(content)
    cmd = f":{content}{lrc}\r\n"

    send_serial(ser, cmd)
    return read_serial(ser)


def write_holding_register(ser, address, value, slave="01"):
    content = f"{slave}06{address}{value}"
    # print(f"content: {content}")
    lrc = calculate_lrc(content)
    cmd = f":{content}{lrc}\r\n"

    send_serial(ser, cmd)
    return read_serial(ser)


def check_error(data):
    current_lrc = data[-4:-2]
    valid_lrc = calculate_lrc(data[1:-4])

    if current_lrc != valid_lrc:
        print(f"An error occurred. Expected LRC to be {valid_lrc}, Got: {current_lrc}")
        return False

    if data[3:4] == 83:
        print(f"An error occurred during reading holding register. Code: {data[5:7]}")
        return True
    if data[3:4] == 84:
        print(f"An error occurred during reading input register. Code: {data[5:7]}")
        return True
    if data[3:4] == 86:
        print(f"An error occurred during writing holding register . Code: {data[5:7]}")
        return True
    return False


# TODO: get hours and minutes
def get_time(ser, slave="01"):
    data = read_input_register(ser, "0005", "0001", slave=slave)
    if check_error(data):
        return
    nb_octets = int(data[5:7])
    seconds = int(f"0x{data[9:11]}", 16)
    return seconds


def get_temperature(ser, slave="01"):
    data = read_input_register(ser, "0001", "0001", slave=slave)
    nb_octets = int(data[5:7])
    if check_error(data):
        return
    temperature_int = int(f"0x{data[7:9]}", 16)
    temperature_dec = int(f"0x{data[9:11]}", 16)
    temperature = float(f"{temperature_int}.{temperature_dec}")
    return temperature


def write_bargraph(ser, data, slave="01"):
    if data > 1023:
        print(f"An error occurred. Expected data to be less than 1023, Got: {data}")
        return
    value = f"{data:02X}".rjust(4, "0")
    # print(f"Bargraph data: {data}")
    # print(f"Bargraph value: {value}")
    data = write_holding_register(ser, "0001", value, slave=slave)
    check_error(data)


class Command(Enum):
    UPDATE_DATE_TIME = "10"
    START_MESURE = "20"
    STOP_MESURE = "30"
    SLOW_BLINK = "40"
    FAST_BLINK = "50"
    CUSTOM_BLINK = "60"


def set_command(ser, command, slave="01"):
    if command.value in Command.__members__:
        print(f"An error occurred. Expected command to be one of {list(Command)}, Got: {command}")
        return

    (index, last_command) = get_command(ser, slave=slave)

    value = f"{index + 1:02X}".rjust(2, "0")
    value += f"{command.value}"

    data = write_holding_register(ser, "0000", value, slave=slave)
    check_error(data)


def get_command(ser, slave="01"):
    data = read_holding_register(ser, "0000", "0001", slave=slave)
    if check_error(data):
        return
    nb_octets = int(data[5:7])
    index = int(f"0x{data[7:9]}", 16)
    command = data[9:11]
    return index, command


def set_second(ser, slave="01"):
    now = datetime.now()
    seconds = f"{now.second:02X}".rjust(4, "0")

    data = write_holding_register(ser, "0005", seconds, slave=slave)
    if check_error(data):
        return
    time.sleep(1)
    set_command(ser, Command.UPDATE_DATE_TIME, slave=slave)
