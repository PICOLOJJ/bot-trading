import time
import requests
import pandas as pd

# CONFIGURACIÓN
TOKEN = "8910965730:AAGqITg_VEah4CJDE33gF2C5cU7589TvzXE"
CHAT_ID = "1114179487"
SYMBOL = "BTCUSDT"         
INTERVAL = "5m"            

def enviar_mensaje(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    requests.post(url, data=payload)

def obtener_datos():
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=250"
    res = requests.get(url).json()
    df = pd.DataFrame(res, columns=['time', 'open', 'high', 'low', 'close', 'volume', '_', '_', '_', '_', '_', '_'])
    df['close'] = df['close'].astype(float)
    return df

def analizar_mercado():
    df = obtener_datos()
    
    # Cálculo de Medias Móviles (MA 50 y MA 200)
    df['MA50'] = df['close'].rolling(window=50).mean()
    df['MA200'] = df['close'].rolling(window=200).mean()

    # Valores de la vela anterior y actual
    prev_ma50 = df['MA50'].iloc[-2]
    prev_ma200 = df['MA200'].iloc[-2]
    curr_ma50 = df['MA50'].iloc[-1]
    curr_ma200 = df['MA200'].iloc[-1]
    precio_actual = df['close'].iloc[-1]

    # Imprimir en la consola de Pydroid para confirmar lectura
    print(f"[{time.strftime('%H:%M:%S')}] {SYMBOL} | Precio: ${precio_actual:.2f} | MA50: {curr_ma50:.2f} | MA200: {curr_ma200:.2f}")

    # Detección de Cruce de Oro (Compra / CALL)
    if prev_ma50 <= prev_ma200 and curr_ma50 > curr_ma200:
        enviar_mensaje(f"🚨 ALERTA TRADING 🚨\n\n✨ CRUCE DE ORO (COMPRA / CALL)\nPar: {SYMBOL}\nTemporalidad: {INTERVAL}\nLa MA50 cruzó por encima de la MA200.")
        print("--> ¡Cruce de Oro detectado! Alerta enviada a Telegram.")
    
    # Detección de Cruce de Muerte (Venta / PUT)
    elif prev_ma50 >= prev_ma200 and curr_ma50 < curr_ma200:
        enviar_mensaje(f"🚨 ALERTA TRADING 🚨\n\n💀 CRUCE DE MUERTE (VENTA / PUT)\nPar: {SYMBOL}\nTemporalidad: {INTERVAL}\nLa MA50 cruzó por debajo de la MA200.")
        print("--> ¡Cruce de Muerte detectado! Alerta enviada a Telegram.")

# Notificación al arrancar la ejecución
enviar_mensaje("🤖 Bot de alertas iniciado correctamente en tu dispositivo.")

while True:
    try:
        analizar_mercado()
        time.sleep(60)  # Revisa el mercado cada 60 segundos
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
