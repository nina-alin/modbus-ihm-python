def main():
    """
    save_input_register(conn, 1, "2020-01-01 12:12:00", 22.0)
    data = get_input_register(conn, limit=10)
    print(data)

    print("Set Command: START MESURE")
    set_command(ser, Command.START_MESURE)
    print("START MESURE Command set")
    time.sleep(1)

    print()

    seconds = get_time(ser)
    print(f"Time: {seconds}")
    time.sleep(1)

    print()

    print("Set: Seconds")
    set_second(ser)
    print("Seconds set")
    time.sleep(1)

    print()

    seconds = get_time(ser)
    print(f"Time: {seconds}")
    time.sleep(1)

    print()

    temperature = get_temperature(ser)
    print(f"Temp: {temperature}")
    time.sleep(1)

    print()

    print("Set Bargraph: Temperature")
    write_bargraph(ser, int(temperature))
    print("Temperature set to bargraph")
    time.sleep(1)

    print()

    print("Set Command: FAST BLINK")
    set_command(ser, Command.FAST_BLINK)
    print("FAST BLINK Command set")
    time.sleep(1)

    print()

    print("Set Command: STOP MESURE")
    set_command(ser, Command.STOP_MESURE)
    print("STOP MESURE Command set")
    time.sleep(1)
    """
