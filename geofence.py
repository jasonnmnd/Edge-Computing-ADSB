from gpiozero import LED
from parseData import CreateAircrafts, Aircraft
import time
import os
import socket

def setupGeofence(planes):
    # redLED = LED(22)
    # greenLED = LED(17)
    # yellowLED = LED(27)
    for plane in planes:
        for radius in plane.radius:
            if radius <= 20:
                print("Plane within 20 miles")
                # greenLED.off()
                # yellowLED.off()
                # redLED.on()
                #time.sleep(5)
                break

            if radius >20 and radius <= 50:
                print("Plane within 20 and 50 miles")
                # redLED.off()
                # greenLED.off()
                # yellowLED.on()
                #time.sleep(5)
                break

            if radius > 50 and radius <=100:
                print("Plane within 50 and 100 miles")
                # redLED.off()
                # yellowLED.off()
                # greenLED.on()
                #time.sleep(5)
                break

if __name__ == "__main__":
    startTime = time.time()

    planes = CreateAircrafts()
    setupGeofence(planes)
    # os.system('ssh pi@raspberrypi.local')
    # os.system('ssh -tt pi@172.20.10.11')
    # os.system('password')
    # os.system('scp /Users/jasondong/Desktop/piTest.html pi@raspberrypi.local:/home/pi/ece590-adsb')
    # os.system('scp /Users/jasondong/Desktop/piTest.html pi@172.20.10.11:/home/pi/ece590-adsb')
    # os.system('password')

    # ip = "172.20.10.11"  # IP of Raspberry Pi
    #
    # # connect to server
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect((ip, 8080))
    # print("CLIENT: connected")
    #
    # # send a message
    # msg = "I am CLIENT"
    # client.send(msg.encode())
    #
    # # recive a message and print it
    # from_server = client.recv(4096).decode()
    # print("Recieved: " + from_server)
    #
    # # exit
    # client.close()

    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))