wget https://github.com/aperepel/raspberrypi-ch340-driver/releases/download/4.4.11-v7/ch34x.ko
#Treiber installieren
sudo insmod ch34x.ko
#Treiber/Modul in den Kernel einspeisen
ls /lib/modules/$(uname -r)/kernel/drivers/usb/serial
#sichergehen, dass der Treiber isntalliert wurde
sudo reboot
#erst beim reboot werden die Änderungen vorgenommen
