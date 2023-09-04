from serial import Serial

# Wrapping the KeyPad around Serial
class KeyPad(Serial):
    def state(self):
        self.reset_input_buffer()
        return self.readline().decode("utf-8").rstrip()

# For direct testing    
if __name__ == "__main__":
    import time
    keypad = KeyPad("/dev/ttyS0", 9600)
    time.sleep(2)
    while True:
        print(keypad.state())

