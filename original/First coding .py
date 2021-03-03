
import spidev # To communicate with SPI devices
from numpy import interp    # To scale values
from time import sleep  # To add delay
import RPi.GPIO as GPIO # To use GPIO pins
import time
import os
import tkinter
import tkinter.messagebox

window = tkinter.Tk()
window.title("Straw Cleaning Operation")
window.geometry('350x200')
label = tkinter.Label(window, text = "DATE:" + str(print(time.strftime("          %a %d-%m-%Y @ %H:%M:%S")))).pack()
label = tkinter.Label(window, text = "STATUS:").pack()

top_frame = tkinter.Frame(window).pack()
bottom_frame = tkinter.Frame(window).pack(side = "bottom")
btn3 = tkinter.Button(bottom_frame, text = "Start", fg = "purple").pack(side = "left") #'side' is used to left or right align the widgets
btn4 = tkinter.Button(bottom_frame, text = "End", fg = "orange").pack(side = "right")



relay_pins = [23, 24, 22, 27, 17]
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pins, GPIO.OUT)
x = 0
#window = tkinter.Tk()
#window.title("Straw Cleaning Operation")
#window.geometry('350x200')

#label = tkinter.Label(window, text = "DATE:" + str(print(time.strftime("          %a %d-%m-%Y @ %H:%M:%S")))).pack()
#label = tkinter.Label(window, text = "STATUS:").pack()



spi = spidev.SpiDev() # Created an object
spi.open(0,0)

# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
  
def stepe():
    print("Start")
    btn3label = tkinter.Label(bottom_frame, text = "Start", fg = "purple").pack(side = "left")
    
def stepi():
    time.sleep(2)
        
    if analogInput(0) >= 1000:
       print("Cover lid close")
       step0() 
    else:
        print("Warning cover open")
        stepi()
       
        top = tkinter.Tk()

        def helloCallBack():
            tkinter.messagebox.showinfo( "Hello Python", "Return to Step i")

        B = tkinter.Button(top, text ="Warning!", command = helloCallBack)

        B.pack()
        top.mainloop()
       
def step0():
    time.sleep(2)
    
    # Function body
    if analogInput(1) >= 1000:
        GPIO.output(23,1) #Pump on
        GPIO.output(24,1) #Valve A on
        print("Pump on, fill tank 1, Valve A open")
        step1() 
    else:
        print("Please fill the reservoir tank")
        top = tkinter.Tk()

        def helloCallBack():
            tkinter.messagebox.showinfo( "Hello Python", "Return to Step 0")

        B = tkinter.Button(top, text ="Warning!", command = helloCallBack)

        B.pack()
        top.mainloop()
        step0()   
                
def step1():
    time.sleep(2)
        
    if analogInput(2) >= 1000:
        GPIO.output(23,0) #Pump off
        GPIO.output(24,0) #Valve A close
        print("Tank 1 is full, Valve A close, Pump off")
        step2()   
    else:
        GPIO.output(23,1) #Pump on
        GPIO.output(24,1) #Valve A on
        print("Tank 1 is filling up")
        top = tkinter.Tk()

        def helloCallBack():
            tkinter.messagebox.showinfo( "Hello Python", "Return to Step 1")

        B = tkinter.Button(top, text ="Warning!", command = helloCallBack)

        B.pack()
        top.mainloop()
        step1()
       
def step2():
    time.sleep(2)
    
    if analogInput(3) >= 1000:
        GPIO.output(22,0) #heating element 1 off
        print("Temperature Tank 1 reach 90 degree Celcius, heating elemen 1 off")
        step3()
    else:
        GPIO.output(22,1) #heating element 1 on
        print("heating element Tank 1 on")
        top = tkinter.Tk()

        def helloCallBack():
            tkinter.messagebox.showinfo( "Hello Python", "Return to Step 2")

        B = tkinter.Button(top, text ="Warning!", command = helloCallBack)

        B.pack()
        top.mainloop()
        step2()   
   
def step3():
    time.sleep(2)
        
    if analogInput(4) >= 1000:
        GPIO.output(23,0) #Pump off
        GPIO.output(27,0) #Valve B close
        GPIO.output(24,0)#Valve A close
        print("Tank 2 is full, valve A&B close, Pump close")
        step4()
        
    else:
        GPIO.output(23,1) #Pump on
        GPIO.output(27,1) #Valve B open
        GPIO.output(24,1)#Valve A open
        print("Valve A&B open, Pump turn on, filling Tank 2")
        top = tkinter.Tk()

        def helloCallBack():
            tkinter.messagebox.showinfo( "Hello Python", "Return to Step 3")

        B = tkinter.Button(top, text ="Warning!", command = helloCallBack)

        B.pack()
        top.mainloop() 
        step3()
            
def step4():
    time.sleep(2)
        
    if analogInput(5) >= 1000:
        GPIO.output(17,0) #heating element 2 off
        print("Heating element 2 off")
        step5()   
    else:
        GPIO.output(17,1) #heating element 2 on
        print("Heating element 2 on")
        top = tkinter.Tk()

        def helloCallBack():
            tkinter.messagebox.showinfo( "Hello Python", "Return to Step 4")

        B = tkinter.Button(top, text ="Warning!", command = helloCallBack)

        B.pack()
        top.mainloop()
        step4()
        
def step5():
    if x >= 1:
        print("Valve C open rinse")
        time.sleep(20)
        
       
    else:
        print("Valve C&D open")
        print("Return to step1")
        time.sleep(20)
        top = tkinter.Tk()

        def helloCallBack():
            tkinter.messagebox.showinfo( "Hello Python", "Return to Step 0")

        B = tkinter.Button(top, text ="Warning!", command = helloCallBack)

        B.pack()
        top.mainloop()

def stepo():
    print("End")
    btn4 = tkinter.Button(bottom_frame, text = "End", fg = "orange").pack(side = "right")
window.mainloop()


print('Reading mcp3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = analogInput(i)
    # Print the ADC values.
    #print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Pause for half a second.
     
    stepe()
    stepi()
    x += 1
    step1()
    stepo()
    break


# Once the frames are created then you are all set to add widgets in both the frames.
GPIO.cleanup() 
