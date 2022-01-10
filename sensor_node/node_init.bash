pip install -r requirements.txt

echo 'AT+DR=EU868' > /dev/ttyUSB0
echo 'AT+MODE=LWOTAA' > /dev/ttyUSB0
echo 'AT+KEY=APPKEY,"numer"' > /dev/ttyUSB0

echo 'AT+JOIN' > /dev/ttyUSB0