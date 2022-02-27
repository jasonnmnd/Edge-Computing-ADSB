from gpiozero import LED
from parseData import CreateAircrafts, Aircraft
import time

def setupGeofence(planes):
    redLED = LED(22)
    greenLED = LED(17)
    yellowLED = LED(27)
    for plane in planes:
        for radius in plane.radius:
            if radius <= 20:
                print("Plane within 20 miles")
                greenLED.off()
                yellowLED.off()
                redLED.on()
                time.sleep(5)
                break

            if radius >20 and radius <= 50:
                print("Plane within 20 and 50 miles")
                redLED.off()
                greenLED.off()
                yellowLED.on()
                time.sleep(5)
                break

            if radius > 50 and radius <=100:
                print("Plane within 50 and 100 miles")
                redLED.off()
                yellowLED.off()
                greenLED.on()
                time.sleep(5)
                break

if __name__ == "__main__":
    planes = CreateAircrafts()
    setupGeofence(planes)