import machine
import time
import network
#import dht
import urequests
import urandom as random  # Menggunakan urandom sebagai pengganti random
from vl53l0x import VL53L0X
from machine import I2C, Pin, SoftI2C
from time import sleep
from bh1750 import BH1750

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("room","scambles")

while not wlan.isconnected():
    print(".",end="")
    time.sleep(.1)

print("WLAN is connected")
UBIDOTS_ENDPOINT = "https://industrial.api.ubidots.com/api/v1.6/devices/corelogic/"
FLASK_ENDPOINT = "http://192.168.1.2:2000/save"

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)

# Inisialisasi sensor
light_sensor = BH1750(i2c)  # Pastikan library kompatibel dengan cara ini
tof = VL53L0X(i2c)
tof.init()  # Inisialisasi VL53L0X

try:
    while True:
        # Membaca nilai cahaya
        lux = light_sensor.luminance(BH1750.CONT_HIRES_1)
        print("Cahaya: {:.2f} lux".format(lux))

        # Membaca jarak
        tof.start()
        distance = tof.read()
        tof.stop()
        print("Jarak: {} mm".format(distance))

        sleep(1)  # Tunggu 1 detik sebelum membaca kembali
    
        data = {"Cahaya": lux, "Jarak": distance}
        headers = {"Content-Type":"application/json","X-Auth-Token":"BBUS-eCkv24LYNvWw8SKQR0TWg1z3SlCWuC"}
        response = urequests.post(UBIDOTS_ENDPOINT,json=data,headers=headers)
    
        print(f"response ubidots: {response.status_code}")
        response.close()
    
        headers = {"Content-Type":"application/json"}
        response = urequests.post(FLASK_ENDPOINT,json=data,headers=headers)
    
        print(f"response flask: {response.status_code}")
        response.close()

except Exception as e:
    print("Terjadi kesalahan:", e)

