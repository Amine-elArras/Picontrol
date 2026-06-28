# gemaakt door Amine el Arras 
# 29-06-2026 

# Oude PYFIRMATA functies in nieuwe python versies
# De PYFIRMATA bibliotheek gebruikt een oude funcite genaamd 'getargspec'
# sinds kort verwijderd uit python , hierdoor verwijs ik verwijs ik de oude functie naar de nieuwe 'getfullargspec'
import inspect
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec


#biblotheek importeren
from flask import Flask, render_template
from pyfirmata import Arduino
#start de flask applicatie
app = Flask(__name__)

# Arduino koppeling en pin configuratie
# Verbinding maken met de Arduino via de USB-kabel op de Raspberry Pi
try:
    board = Arduino('/dev/ttyACM0')

    # d = digital, 12 = pin nummer, o = output
    led_pin = board.get_pin('d:12:o')
    print("Succesvol verbonden met Arduino!")
except Exception as e:
# Als de arduino niet is ingeplugd og op een andere poort zit , vangt dit de fout op 
    print("Kan de Arduino niet vinden op /dev/ttyACM0. Controleer de USB-kabel.")
    print(e)

# De hoofdpagina  (wanneer je naar http://[IP-ADRES]:5000 gaat)
@app.route('/')
def index():
# Flask zoekt in de map 'templates 'naar index.html' en stuurt deze naar de browser 
    return render_template('index.html')

# De 'Aan' knop route (wanneeer je op de groene knop klikt) 
@app.route('/aan')
def led_on():
    try:
        led_pin.write(1) # Stuur een 1 (HIGH / 5 Volt) naar de pin 12 -> LED gaat AAN
    except NameError:
        print("Arduino niet gekoppeld, kan pin niet aansturen.")
     # laad de pagina opnieuw zodat de knoppen in beeld blijven 
    return render_template('index.html')

@app.route('/uit')
def led_off():
    try:
        led_pin.write(0)  # Stuur een 0 (LOW / 0 Volt) naar de pin 12 -> LED gaat UIT
    except NameError:
        print("Arduino niet gekoppeld, kan pin niet aansturen.")
      # laad de pagina opnieuw zodat de knoppen in beeld blijven
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
#uitleg server code hier onder 

#De regel 'if __name__ == "__main__":' controleert HOE dit bestand wordt opgestart.
#
# - Als je in de terminal typt: 'python app.py', dan is dit het hoofdprogramma.
#   Python geeft dit bestand dan de onzichtbare stempel: __name__ = "__main__".
#   De code hieronder wordt dan gewoon netjes uitgevoerd en de server start.
#
# - Mocht dit bestand ooit door een ander Python-script worden geïmporteerd (als hulpje),
#   dan is de stempel NIET gelijk aan "__main__". De code hieronder wordt dan overgeslagen.
#   Hierdoor voorkom je dat de webserver ongevraagd opstart als je de code elders gebruikt. 

   # host='0.0.0.0' zorgt ervoor dat de website bereikbaar is voor alle apparaten in je wifi-netwerk
    # port=5000 stelt het poortnummer in waarop de server luistert
    # debug=True start de automatische herstart-functie bij codewijzigingen
