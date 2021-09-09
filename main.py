import sqlite3 as sqlite
import constants
from RPi import GPIO
import time
from datetime import datetime

class Button:
    pin: int
    
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)
        
    def get_state(self) -> bool:
        return GPIO.input(self.pin)
    
    def wait_for_on(self):
        GPIO.wait_for_edge(self.pin, GPIO.RISING)

    def wait_for_off(self):
        GPIO.wait_for_edge(self.pin, GPIO.FALLING)


class Led:
    pin: int
    is_on: bool
    
    def __init__(self, pin: int):
        self.pin = pin
        self.is_on = False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)
        
    def set_state(self, on: bool):
        self.is_on = on
        GPIO.output(self.pin, self.is_on)
        

class Main:
    Button: Button
    Led: Led
    DB_Connection: sqlite.Connection
    DB_Cursor: sqlite.Cursor
    
    def __init__(self, button_pin: int, led_pin: int, db_filename: str):
        self.Button = Button(button_pin)
        self.Led = Led(led_pin)
        self.DB_Connection = sqlite.Connection(db_filename)
        self.DB_Cursor = self.DB_Connection.cursor()
        
    def run(self):
        try:
            toggle_state = False
            while True:
                self.Button.wait_for_on()
                start_time = time.time()
                self.Button.wait_for_off()
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                if(elapsed_time > 1):
                    continue

                toggle_state = not toggle_state
                self.Led.set_state(toggle_state)
                self.DB_Cursor.execute("""
                    INSERT INTO ledstate (is_on, time_changed) VALUES(:is_on, :time_changed)
                """, {"is_on": toggle_state, "time_changed": start_time})
        except KeyboardInterrupt:
            GPIO.cleanup()
            self.DB_Connection.commit()
            self.DB_Connection.close()


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    m = Main(constants.BUTTONPIN, constants.LEDPIN, constants.DBFILENAME)
    m.run()
