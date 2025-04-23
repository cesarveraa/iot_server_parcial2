import machine
import time
import dht
import network
import urequests
import ujson

# ————————————————
# Configuración Wi-Fi
# ————————————————
SSID     = "TU_SSID"
PASSWORD = "TU_PASSWORD"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("Conectando a Wi-Fi…")
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
print("Conectado, IP:", wlan.ifconfig()[0])

# ————————————————
# Pines y sensores
# ————————————————
dht22    = dht.DHT22(machine.Pin(4))

pot_temp = machine.ADC(machine.Pin(35))
pot_temp.atten(machine.ADC.ATTN_11DB)
pot_temp.width(machine.ADC.WIDTH_12BIT)

mq7_adc  = machine.ADC(machine.Pin(34))
mq7_adc.atten(machine.ADC.ATTN_11DB)
mq7_adc.width(machine.ADC.WIDTH_12BIT)

pot_co   = machine.ADC(machine.Pin(32))
pot_co.atten(machine.ADC.ATTN_11DB)
pot_co.width(machine.ADC.WIDTH_12BIT)

in1 = machine.Pin(16, machine.Pin.OUT)
in2 = machine.Pin(17, machine.Pin.OUT)
ena = machine.PWM(machine.Pin(18), freq=1000)
ena.duty(0)

# ————————————————
# Parámetros de control
# ————————————————
TEMP_UMBRAL    = 25.0
MIX_RATIO      = 0.5
CO_MIN_RAW     = 2
CO_MAX_RAW     = 3000
prev_thr       = CO_MAX_RAW

# ————————————————
# Identificación de este ESP32 (nodo)
# ————————————————
NODE_ID  = "dTnZizlV64YTjnsYHNOK"  # reemplaza con el ID de tu nodo en Firestore
ENDPOINT = "https://iotparcial2.vercel.app/nodes/{}/readings".format(NODE_ID)

# ————————————————
# Funciones auxiliares
# ————————————————
def leer_temp_sim():
    v = pot_temp.read()
    return (v / 4095) * 20 + 20

def calc_thr_co():
    global prev_thr
    v = pot_co.read()
    thr = CO_MIN_RAW + (CO_MAX_RAW - CO_MIN_RAW) * (1 - v / 4095)
    thr = prev_thr * 0.3 + thr * 0.7  # suavizado exponencial
    prev_thr = thr
    return int(thr)

# ————————————————
# Bucle principal
# ————————————————
while True:
    # 1) Leer DHT22
    try:
        dht22.measure()
        t_real = dht22.temperature()
        hum    = dht22.humidity()
    except:
        t_real = None
        hum    = None

    # 2) Leer y calcular temperatura simulada y mixta
    t_sim = leer_temp_sim()
    if t_real is None:
        t_mix = t_sim
    else:
        t_mix = MIX_RATIO * t_real + (1 - MIX_RATIO) * t_sim

    # 3) Leer CO y umbral dinámico
    co_val = mq7_adc.read()
    co_thr = calc_thr_co()

    # 4) Control del motor (L298N)
    motor_on = False
    if t_mix > TEMP_UMBRAL or co_val > co_thr:
        in1.on()
        in2.off()
        ena.duty(512)  # 50% de duty (0–1023)
        motor_on = True
    else:
        in1.off()
        in2.off()
        ena.duty(0)

    # 5) Debug por consola
    print("T_real:", t_real, "T_sim:", round(t_sim,1), "→ T_mix:", round(t_mix,1))
    print("Hum:", hum, "% | CO:", co_val, "Thr_CO:", co_thr)
    print("Motor:", "ON" if motor_on else "OFF")
    print("-" * 40)

    # 6) Construir y enviar payload
    payload = {
        "temperatura_real":     t_real or 0,
        "temperatura_simulada": round(t_sim, 1),
        "temperatura_mixed":    round(t_mix, 1),
        "humedad":              hum or 0,
        "co_raw":               co_val,
        "ventilador_on":        motor_on
    }
    try:
        res = urequests.post(
            ENDPOINT,
            headers={"Content-Type": "application/json"},
            data=ujson.dumps(payload)
        )
        res.close()
    except Exception as e:
        print("Error enviando datos:", e)

    time.sleep(2)
