import paho.mqtt.client as mqtt
import json
import time

# Define callback functions for MQTT events
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to topics on connection
    client.subscribe("medidor/configuracao")
    client.subscribe("medidor/controle")

def on_message(client, userdata, message):
    print("Received message on topic " + message.topic)
    print("Message payload: " + str(message.payload))
    # Process message payload
    if message.topic == "medidor/configuracao":
        process_config(message.payload)
    elif message.topic == "medidor/controle":
        process_control(message.payload)

# Define functions for processing configuration and control messages
def process_config(payload):
    # Convert payload to dictionary
    config = json.loads(payload)
    # Set configuration parameters on smart meter
    medidor.set_config(config)

def process_control(payload):
    # Convert payload to dictionary
    control = json.loads(payload)
    # Perform control action on smart meter
    medidor.perform_control(control)

# Conectar ao medidor inteligente
medidor = SmartMeter('192.168.1.10')

# Configurar a conexão MQTT
client = mqtt.Client()
client.username_pw_set('usuario', 'senha')
client.on_connect = on_connect
client.on_message = on_message
client.connect('mqtt.servidor.com', 1883)

# Iniciar loop de eventos MQTT
client.loop_start()

# Loop principal do programa
while True:
    # Ler os dados do medidor
    dados = medidor.ler_dados()

    # Converter os dados em JSON
    payload = json.dumps(dados)

    # Publicar os dados no tópico MQTT
    client.publish('medidor/dados', payload)

    # Esperar um intervalo de tempo
    time.sleep(10)

# Parar loop de eventos MQTT ao finalizar programa
client.loop_stop()
