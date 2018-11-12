import time
111111
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import smtplib

# Software SPI configuration:
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def send (content):
    mail = smtplib.SMTP ('smtp.gmail.com', 587)
    #print ("server up")
    mail.ehlo()
    #print ("ehlo")
    mail.starttls()
    #print ("Tls started, data safe")
    mail.login ('jupiterlightning1', '#washcycle')
    mail.sendmail ('jupiterlightning1', '19myersm@fairviewschools.org', content)
    mail.close()
    
print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.
#while True:
    # Read all the ADC channel values in a list.
values = [0]*8
for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
    values[i] = mcp.read_adc(i) - 500
    # Print the ADC values.
    #print('| {0:>4} |'.format(*values))
    #time.sleep (1)
count = 0
while True:    
    if count == 0:
        values [0] = mcp.read_adc(0) - 500
        if values [0] < -10 or values [0] > 10:
            print (values [0], "There is power. No problems.")
            time.sleep(1)
            pass
        if -10 <= values[0] <= 10:
            send ("Power outage at Unit 1")
            print (values [0], "Just sent the mail (distress signal). I shouldn't send any more mail until the power comes back.")
            time.sleep (1)
            count +=1
    if count == 1:
        values [0] = mcp.read_adc(0) -500
        if -10 <= values [0] <= 10:
            print (values [0], "Power is still out")
            time.sleep (1)
        if values [0] < -10 or values [0] > 10:
            send ("Power restored at Unit 1")
            print (values [0], "Just sent the mail (all-clear).")
            time.sleep(1)
            count -=1
            
        
