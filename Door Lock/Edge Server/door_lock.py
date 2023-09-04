from serial import Serial

# Wrapper around Serial that can communicate with Arduino sketch.
class DoorLock(Serial):
    def set(self, value):
        self.write(b"set " + str(int(value)).encode("utf-8") + b"\n")
    
    def state(self):
        self.reset_input_buffer()
        self.write(b"state\n")
        return self.readline().decode("utf-8").rstrip() == "Locked"

# Simple test routine, only when run directly
if __name__ == "__main__":
    import time
    lock = DoorLock("/dev/ttyACM0", 115200)
    time.sleep(2)
    while True:
        print(lock.state())
        input()
        lock.set(True)
        print(lock.state())
        input()
        lock.set(False)
    
