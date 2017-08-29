#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import spidev
import time
import os
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  #sends 00000001 10000000 00000000 to the device.
  #The device then sends back 3 bytes in response. 
  #The “data=” line extracts 10 bits from that response and this represents the measurement.
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
 
# 1-Wire Slave-Liste lesen
file = open('/sys/devices/w1_bus_master1/w1_master_slaves')
w1_slaves = file.readlines()
file.close()

# Fuer jeden 1-Wire Slave aktuelle Temperatur ausgeben
for line in w1_slaves:
  # 1-wire Slave extrahieren
  w1_slave = line.split("\n")[0]
  # 1-wire Slave Datei lesen
  file = open('/sys/bus/w1/devices/' + str(w1_slave) + '/w1_slave')
  filecontent = file.read()
  file.close()

  # Temperaturwerte auslesen und konvertieren
  stringvalue = filecontent.split("\n")[1].split(" ")[9]
  temperature = float(stringvalue[2:]) / 1000

  # Temperatur ausgeben
  print(str(w1_slave) + ': %6.2f °C' % temperature)
 
 
# Define sensor channels
temp_channel  = 1
 
# Define delay between readings
delay = 5
 
