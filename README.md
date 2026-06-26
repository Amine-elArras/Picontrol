PiControl

PiControl is een leerproject waarin een Raspberry Pi samenwerkt met een Arduino Uno om fysieke hardware te besturen via een webinterface.

---

 Wat doet dit project?

Met PiControl kun je:

 LEDs aan/uit zetten via een webpagina
 Temperatuur uitlezen met sensoren
 Servo’s besturen vanaf je browser
 Tekst tonen op een LCD-scherm
 Knoppen en input van Arduino uitlezen
 Alles bedienen via een Raspberry Pi webserver

---

 Architectuur

Browser (PC / Telefoon)
        ↓
Raspberry Pi (Python Flask server)
        ↓ USB Serial
Arduino Uno
   ├── LED
   ├── Servo
   ├── Sensoren
   ├── LCD
   └── Knoppen

---

 Technologieën

Raspberry Pi:
 Linux (Raspberry Pi OS)
 Python
 Flask (webserver)
 Serial communication (pyserial)

Arduino:
 C++
 Arduino IDE
 GPIO (LEDs, sensors, servo, LCD)

Web:
 HTML
 CSS
 JavaScript (optioneel)

---

 Hardware benodigdheden

Arduino Starter Kit:
 Arduino Uno
 LEDs
 Weerstanden
 Knoppen
 Servo motor
 LCD display
 Temperatuursensor
 Lichtsensor

Raspberry Pi:
 Raspberry Pi 3/4/5
 microSD kaart
 Internet verbinding

---

 Hoe werkt het?

1. Raspberry Pi draait Flask server
2. Browser opent webpagina
3. Jij klikt op knop (bv. LED aan)
4. Pi stuurt commando via USB
5. Arduino schakelt hardware

---


 

 Doel

Begrijpen hoe software en hardware samenwerken in IoT systemen.

---

 Status
 In ontwikkeling (fase 1)
