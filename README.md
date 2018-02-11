# Project LoCATE
This project is an attempt to make indoor localization of assets and people in healthcare facilities as painless as possible by utilizing the existing infrustructure in the facilities, namely WiFi.

It currently works by using Raspberry Pi's as edge nodes that use the RSSI values of wireless access points nearby to gauge where they are. A goal is to make these edge nodes as small and long lasting as possible.

The entire program is currently contained inside the Python script, _locate.py_.
