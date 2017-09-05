#UART-Konverter
wget https://github.com/aperepel/raspberrypi-ch340-driver/releases/download/4.4.11-v7/ch34x.ko
#Treiber installieren
sudo insmod ch34x.ko
#Treiber/Modul in den Kernel einspeisen
ls /lib/modules/$(uname -r)/kernel/drivers/usb/serial
#sichergehen, dass der Treiber isntalliert wurde
sudo reboot
#erst beim reboot werden die Änderungen vorgenommen

#NOVA PM SDS011
sudo apt-get -fym isntall bc
#ein benötigtes Programm (bc) wird installiert

#rrdtool
sudo apt-get install rrdtool
#rrdtool wird installiert, um Grafiken erstellen zu können

#Temperatursensor DS18B20
sudo nano /boot/config.txt
#diese Datei wird um folgende Endung ergänzt:
dtoverlay=w1-gpio,gpiopin=4,pullup=1
sudo nano /etc/modules
#diese Datei wird ebenfalls ergänzt:
w1-gpio pullup=1
w1-therm
