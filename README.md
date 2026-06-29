# PiControl

PiControl is een leerproject waarin een Raspberry Pi samenwerkt met een Arduino Uno om fysieke hardware te besturen via een webinterface.

---

## Wat doet dit project?

Met PiControl kun je een LED-lampje op Pin 12 van de Arduino draadloos aan- en uitzetten via een lokale webpagina die wordt gehost op de Raspberry Pi. In de toekomst kan dit project worden uitgebreid voor het uitlezen van sensoren en het aansturen van servo's.

---

## Architectuur en Hardware-verbinding

### Systeemarchitectuur

Browser (PC / Telefoon)
       ↓ (HTTP-verzoeken zoals /aan en /uit)
Raspberry Pi (Python Flask server)
       ↓ USB Serial (Firmata-protocol via /dev/ttyACM0)
Arduino Uno
   └── Fysieke Schakeling (Breadboard

### Hardware-opstelling (Breadboard)
hgDe LED is als volgt aangesloten op de Arduino Uno via het breadboard:
1. Een jumperdraad loopt van Pin 12 op de Arduino naar een rij op het breadboard.
2. Op diezelfde rij is de lange poot (anode/pluspool) van de LED aangesloten.
3. De korte poot (kathode/minpool) van de LED is verbonden met een weerstand om de stroom te begrenzen.
4. De andere kant van de weerstand is via een jumperdraad verbonden met de GND (Ground/minpool) pin van de Arduino.

---

## Exacte stappen en terminal-commando's

Om dit project vanaf nul op te zetten en werkend te krijgen, zijn de volgende stappen uitgevoerd in de terminal van de Raspberry Pi:

### 1. Projectstructuur en mappen aangemaakt
Er is een overzichtelijke mappenstructuur opgezet in de home-directory van de Raspberry Pi om de backend en frontend van elkaar te scheiden:

mkdir -p ~/Projects/PiControl/web-server/templates
mkdir -p ~/Projects/PiControl/web-server/static

Dit resulteerde in de volgende structuur:
- web-server/app.py (De Python Flask backend)
- web-server/templates/index.html (De HTML-frontend voor de knoppen)
- web-server/static/style.css (De CSS-opmaak van de website)
- .gitignore (Bestand om ongewenste mappen uit Git te houden)

### 2. Virtuele omgeving (venv) opgezet
Omdat modern Raspberry Pi OS standaard globale installaties via pip vermijdt met een externally-managed-environment melding, is er een geïsoleerde virtuele omgeving aangemaakt:

cd ~/Projects/PiControl
python3 -m venv venv
source venv/bin/activate
pip install flask pyfirmata


### 4. Arduino geconfigureerd met StandardFirmata
Om te zorgen dat de Arduino de commando's van Python begrijpt, is de Arduino via de computer geprogrammeerd met het Firmata-protocol:
1. De Arduino is aangesloten op een pc of laptop.
2. In de Arduino IDE is het voorbeeld geopend via: Bestand > Voorbeelden > Firmata > StandardFirmata.
3. Deze code is geupload naar de Arduino Uno.
4. De Arduino is daarna met een USB-kabel definitief aangesloten op een van de USB-poorten van de Raspberry Pi.

---

## Volledige Code-uitleg

### Backend (web-server/app.py)
In dit bestand draait de Flask-webserver. Omdat pyfirmata een oudere library is die crashte op nieuwere Python-versies door het ontbreken van inspect.getargspec, is er handmatig een 'monkey-patch' toegevoegd om de library compatibel te maken.

import inspect
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

from flask import Flask, render_template
from pyfirmata import Arduino

app = Flask(__name__)

try:
    # Maak verbinding met de Arduino op de standaard Linux USB-poort
    board = Arduino('/dev/ttyACM0')
    # Definieer pin 12 als een Digitale Output (d=digital, 12=pin, o=output)
    led_pin = board.get_pin('d:12:o')
    print("Succesvol verbonden met Arduino!")
except Exception as e:
    print("Kan de Arduino niet vinden op /dev/ttyACM0. Controleer de USB-kabel.")
    print(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aan')
def led_on():
    try:
        led_pin.write(1) # Stuur 5 Volt naar pin 12
    except NameError:
        print("Arduino niet gekoppeld, kan pin niet aansturen.")
    return render_template('index.html')

@app.route('/uit')
def led_off():
    try:
        led_pin.write(0) # Stuur 0 Volt naar pin 12
    except NameError:
        print("Arduino niet gekoppeld, can pin niet aansturen.")
    return render_template('index.html')

if __name__ == '__main__':
    # De server luistert op alle IP-adressen binnen het lokale netwerk op poort 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

### Frontend (web-server/templates/index.html)
De HTML-pagina bevat de knoppen die communiceren met de Flask-routes. Er is gekozen voor een opzet waarbij normale hyperlinks de server aansturen en de pagina verversen.

<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arduino LED Bediening</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>PiControl: Arduino LED</h1>
        <p>Bedien de LED op Pin 12 van de Arduino rechtstreeks vanaf de Raspberry Pi webserver.</p>
        <hr>
        <div class="button-container">
            <a href="/aan" class="btn btn-on">Zet LED AAN</a>
            <a href="/uit" class="btn btn-off">Zet LED UIT</a>
        </div>
    </div>
</body>
</html>

---

## Gecorrigeerde Foutmeldingen (Troubleshooting Log)

Tijdens de ontwikkeling zijn de volgende specifieke problemen opgelost:
- externally-managed-environment: Opgelost door het project volledig te isoleren binnen een Python venv.
- AttributeError: module 'inspect' has no attribute 'getargspec': Opgelost door inspect.getargspec handmatig te patchen naar inspect.getfullargspec bovenaan het Python-script.
- [Errno 2] No such file or directory: '/dev/ttyACM0': Dit gebeurde toen de Arduino werd losgekoppeld voor de software-update. Opgelost door met 'ls /dev/tty*' te verifieren dat de Arduino na het inpluggen inderdaad weer netjes op /dev/ttyACM0 verscheen.
- Permission Denied op USB: Opgelost door de Linux-gebruikersrechten uit te breiden met de dialout groep.

---

## Hoe je het project start

1. Sluit de Arduino via USB aan op de Raspberry Pi.
2. Open de terminal op de Pi en navigeer naar de map:
   cd ~/Projects/PiControl/web-server
3. Activeer de virtuele omgeving:
   source venv/bin/activate
4. Start de Flask-server:
   python app.py
5. Open een browser op een pc of telefoon binnen hetzelfde wifi-netwerk en surf naar het IP-adres van de Pi op poort 5000.

---

## Security en Privacy

Dit project maakt gebruik van een .gitignore bestand. Dit voorkomt dat de omvangrijke venv/ map (die duizenden lokale Python-systeembestanden bevat) per ongeluk naar GitHub wordt geupload.

Daarnaast is de webserver geconfigureerd met host='0.0.0.0'. Dit stelt apparaten binnen het eigen wifi-netwerk in staat om de pagina te bezoeken, maar stelt de server niet open voor het openbare internet. Er worden geen gevoelige openbare IP-adressen of wachtwoorden in de code opgeslagen.
