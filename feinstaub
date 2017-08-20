# Facharbeit

rrdtool create feinstaub.rrd --step 300 DS:werte:GAUGE:600:0:80 RRA:AVERAGE:0.5:12:24
#eine Round-Robin-Datenbank erstellen
#wird benötigt um eine Grafik der Feinstaubdaten erstellen zu können

#Listening 1 (Code aus der MAKE: in modifizierter Form)
#!/bin/bash
WDIR=/usr/local/shellscripts/airquality
srry -F /dev/ttyUSB0 9600 raw
#laut Datenblatt des NOVA PM Sensors muss die Schnittstelle auf 9600 Bit/s konfiguriert werden
#die Werte werden in hexadezimaler Schreibweise ausgegeben
INPUT=$(od --endian=big -x -N10 < /dev/ttyUSB0|haed -n 1|cut -f2-10 -d" ");
#Einschalten der hexadezimale Ausgabe mit -x
#-endian=big weil laut Datenblatt das Low-Byte vor dem High-Byte ausgegeben wird
#/dev/ttyUSB0 ist die Schnittstelle des Sensors
#-N10 sorgt dafür das statt immer neuen Daten nur ein Datenblock mit 10 Bytes ausgegeben wird
echo $INPUT
echo " "
FIRST4BYTES=$(echo $INPUT|cut -b1-4);
echo "FIRST4BYTES
if [ "$FIRST4BYTES" = "aac0 ]; then
  echo "check for correct intro characters: ok"
  logger "check for correct intro characters: ok"
else
  echo "incorrect sequence exiting"
  logger "incorrect sequence, exiting"
  exit;
fi
PPM25LOW=$(echo $INPUT|cut -f2 -d " "|cut -b1-2);
PPM25HIGH=$(echo $INPUT|cut -f2 -d " "|cut -b3-4);
PPM10LOW=$(echo $INPUT|cut -f3 -d " "|cut -b1-2);
PPM10HIGH=$(echo $INPUT|cut -f3 -d " "|cut -b3-4);
#der Ausgelesene 10er-Datenblock enthält Werte, die erst zu Dezimalzahlen konvertiert werden müssen
#Berechnungsformel: (Dezimalwert des High-Bytes x 256 + Dezimalwert des Low-Bytes) / 10 = Feinstaubwert in µ/m³
PPM25LOWDEC=$( echo $((0x$PPM25LOW)) );
PPM25HIGHDEC=$( echo $((0x$PPM25HIGH)) );
PPM10LOWDEC=$( echo $((0x$PPM10LOW)) );
PPM10HIGHDEC=$( echo $((0x$PPM10HIGH)) );
PPM25=$(echo "scale=1;(((PPM25HIGHDEC * 256 ) + $PPM25LOWDEC  ) / 10 ) "bc
-l );
PPM10=$(echo "scale=1;(((PPM10HIGHDEC * 256 ) + $PPM10LOWDEC  ) / 10 ) "bc
-l );
logger "Feinstaub PPM25: $PPM25"
logger "Feinstaub PPM10: $PPM10"
echo "Feinstaub PPM25: $PPM25"
#Ablesen des Wertes für pm25
rrdtool update feinstaub.rrd N:$TEMP
#der Wert wird in die angelegten RRD zeitlich (now) eingetragen
* /5 * * * * /home/pi/feinstaub.sh
#die RRD erwartet alle 5min einen Datenpunkt, also lässt man den Script in diesem Intervall per Cron ausführen
echo "Feinstaub PPM10: $PPM10"
rrdtool update feinstaub.rrd N:$TEMP
#selber Schritt
* /5 * * * * /home/pi/feinstaub.sh
#"
echo $PPM25 > $WDIR/etc/ppm25.txt
echo $PPM10 > $WDIR/etc/ppm10.txt

rrdtool graph feinstaub.gif --start -24h --title "Feinstaub" --vertical-label "µ/m³"  DEF:pm=feinstaub.rrd:werte:AVERAGE LINE1:pm#ff0000:"inhalierbarer Feinstaub";
#erstellt eine Verlaufsgrafik 
#bis jetzt werden beide Datenquellen (pm2.5 und pm10) in einem Diagramm in nur einem Pfad dargestellt (muss optimiert werden)
