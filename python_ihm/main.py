import flask
import db
import serial
import mySerial


app = flask.Flask(__name__)
app.debug = True

app.config["DATABASE"] = "IOT.db"
app.config["SERIAL_PORT"] = "COM4"
app.config["SERIAL_BAUDRATE"] = 9600
app.config["SERIAL_PARITY"] = serial.PARITY_NONE
app.config["SERIAL_STOPBITS"] = serial.STOPBITS_ONE
app.config["SERIAL_BYTESIZE"] = serial.EIGHTBITS
app.config["SERIAL_TIMEOUT"] = 3


def init_app(flask_app):
    flask_app.teardown_appcontext(db.close_db())
    flask_app.teardown_appcontext(mySerial.close_serial())


@app.route('/')
def index():
    con = db.get_db()
    data = db.get_input_register(con)

    return flask.render_template('index.html', data=data)


@app.route('/temperature', methods=["POST"])
def save_temperature():
    ser = mySerial.get_serial()
    con = db.get_db()

    temperature = mySerial.get_temperature(ser)
    print(temperature)
    db.save_input_register(con, 1, "2023-01-01 12:12:12", temperature)

    mySerial.close_serial()
    db.close_db()
    return flask.redirect('/')


if __name__ == '__main__':

    db.init_db()
    app.run()
