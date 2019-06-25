## gotACall ##

This repo has got two barely useful things.

- callOnly, which writes calls and messages received (no content) to a log. 
- callAndWhatsapp, which does same as above but logging to a different location + send whatsapps to a given number with the number that is calling you.

They rely on few things:
 - raspberry pi
 - GSM module (SIM900)
 - yowsup api, to get registered with whastapp, to send whastapps

#### callOnly.py ####

- needs a pin for the sim
- uses tx and rx from raspberry pi (ttyAMA0)
- write messages to syslog (messages)
- sticks number and message received there.
- to see content need to validate and check AT commands in TTYAMA0.


#### callAndWhatsapp.py ####

- needs a pin for the sim
- uses tx and rx from raspberry pi (ttyAMA0)
- write messages to syslog (messages)
- sticks number and message received there.
- to see content need to validate and check AT commands in TTYAMA0.
- requires to modify script to change from, to and whastapp auth code.


### how to generate auth code with whatsapp ### 

```yowsup-cli registration --requestcode sms --config-phone 44XXXXXXXXX --config-cc 44 --config-mcc 234 --config-mnc 002```
- Check https://en.wikipedia.org/wiki/Mobile_country_code for *mnc and mcc* codes
