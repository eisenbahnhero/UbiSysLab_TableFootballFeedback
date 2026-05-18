# UbiSysLab – Table Football Feedback (TFF)

Dieses Projekt implementiert ein modulares Audio-Feedback-System für einen Kicker. An jeder Ecke des Tisches ist ein Lautsprecher angebracht, der kontextabhängige Sounds abspielt – gesteuert durch ein Master/Slave-Netzwerk auf Basis des **Raspberry Pi Pico 2W**.

---

## Module

[Circuit-Diagramm](hardware/01_Circuit_diagram.pdf)
[Setup-Diagramm](hardware/02_Setup.pdf)

### TFF Master-Modul

Das Master-Modul übernimmt die zentrale Steuerungslogik des Systems:

- **Soundsteuerung:** Entscheidet, wann welcher Sound an welchem Lautsprecher abgespielt wird.
- **I2C0 (Master):** Sendet Soundbefehle an alle angeschlossenen TFF Slave-Module.
- **I2C1 (Slave):** Empfängt Positions- und Spielinformationen (z. B. Ballposition) vom Ball-Tracking-System.
- **WLAN-Access-Point:** Stellt ein Web-Interface bereit, über das Sounds manuell ausgelöst werden können – unabhängig vom Tracking.
- **Eigene Lautsprecher:** Kann zusätzlich selbst Sounds über die angeschlossenen Lautsprecher abspielen.

### TFF Slave-Modul

- **I2C0 (Slave):** Empfängt Soundbefehle vom Master-Modul und spielt die entsprechenden Sounds über die angeschlossenen Lautsprecher ab.

---

## Hardware-Setup

An jedem TFF-Modul werden zwei Lautsprecher angeschlossen (je eine Ecke des Kickers). Das System besteht aus:

[Setup-Diagramm](hardware/02_Setup.pdf)

## Kommunikation

Das System verwendet bewusst **zwei getrennte I2C-Busse**:

Die Trennung der Busse hat zwei Vorteile:
1. **Erhöhte Reichweite** – Separate Busse reduzieren kapazitive Last.
2. **Entkopplung** – Das TFF-System kann unabhängig vom Ball-Tracking-System entwickelt und getestet werden.

---

## Web-Interface

Das Master-Modul öffnet einen **WLAN-Access-Point**. Nach dem Verbinden mit einem Smartphone oder Laptop ist über den Browser ein Web-Interface erreichbar, das folgende Funktionen bietet:

- Manuelles Auslösen von Sounds
- Test des Systems ohne aktives Ball-Tracking

---

## Abhängigkeiten / Verwandte Projekte

- **Ball-Tracking-System** – Liefert über I2C1 die Spielinformationen an das TFF Master-Modul. Dieses Projekt ist bewusst von TFF entkoppelt.
