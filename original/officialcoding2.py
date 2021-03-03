#!/usr/bin/env python3
import spidev # To communicate with SPI devices
from numpy import interp    # To scale values
from time import sleep  # To add delay
import RPi.GPIO as GPIO # To use GPIO pins
import time
import os
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter.font
import time
import glob
from PIL import ImageTk, Image
from threading import *
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


#display rasp pi
window = tkinter.Tk()
window.title("Straw Cleaning Operation")
#window.geometry('800x420')
window.attributes('-fullscreen', True)


label_2= tk.Label(window, text=" ",font="Times 22 bold" )
label_2.grid(row=1, column=200)
#logo
r = tkinter.Canvas(window, height=100, width=200)
photo = tkinter.PhotoImage(file= "/home/pi/Downloads/elquator-logo-oval-small-140x122.png")
background_label = tkinter.Label(window, image=photo)
background_label.grid(row=2, column=200)

canv = tkinter.Canvas(window, width=200, height=104)
canv.grid(row=2, column=205)

img = ImageTk.PhotoImage(Image.open("/home/pi/Downloads/CLEAN.STRAW.LOGO.png"))  # PIL solution
canv.create_image(100, 52, image=img)

#spacing
label_2= tk.Label(window, text=" ",font="Times 14 bold" )
label_2.grid(row=7, column=205)

label_2= tk.Label(window, text=" ",font="Times 12 bold" )
label_2.grid(row=10, column=205)
#date
clock_label = tkinter.Label(window, text = "DATE:", font= "Verdana 18 bold  ", )
clock_label.grid(row=50, column=200)

#label_8= tk.Label(window, text="",font="Courier 10 bold" )
#label_8.pack()

#digital clock
clock_label=tkinter.Label(window, font="Verdana 14 bold",fg="blue")
clock_label.grid(row=50, column=205)

def display_time():
    current_time = time.strftime("%a %d-%m-%Y <> %H:%M:%S %p")
    clock_label["text"] = current_time
    window.after(800,display_time)
display_time()

label_1 = tk.Label(window, text="",font="Times 20 bold" )
label_1.grid(row=60, column=100)

#status
label_0 = tk.Label(window, text="STATUS:",font="Verdana 18 bold" )
label_0.grid(row=80, column=200)
label_9 = tk.Label(window, font="Times 16 bold" )
label_9.grid(row=85, column=205)

 
label_2= tk.Label(window, text="TEMPERATURE:",font="Verdana 14 bold" )
label_2.grid(row=90, column=200)


label=tkinter.Label(window, font="Helvetica 20 bold",fg="purple")
label.grid(row=90, column=205)


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def display_temp():
    lines = read_temp_raw()
    while (len(lines) < 1 or lines[0].strip()[-3:] != 'YES' or "00 00 00 00 00 00 00 00 00" in lines[0]):
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_c = round(temp_c)
        label.config(text= str(temp_c)+" °C")
        window.after(800,display_temp)
display_temp()  


            
           
 
def temp():
    lines = read_temp_raw()
    while (len(lines) < 1 or lines[0].strip()[-3:] != 'YES' or "00 00 00 00 00 00 00 00 00" in lines[0]):
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_c = round(temp_c)
        label.config(text= str(temp_c)+" °C")
        if temp_c >= 120:
            print("Heating element 2 close")
        
        
        else:
            print("Heating element 2 open")
            print("Reading Temperature")
            temp()
            
def threading(): 
    # Call work function 
    t1=Thread(target=bar) 
    t1.start()         
 

spi = spidev.SpiDev() # Created an object
spi.open(0,0)
     
#relay
relay_pins = [23, 25, 22, 27, 26, 16]
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pins, GPIO.OUT)
x = 0

# Read MCP3008 data
def analogInput(channel):
    spi.max_speed_hz = 13260000
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

#step start_project - stop_project       
def start_project():
    print("START")
    GPIO.output(23,0) #Pump water close
    GPIO.output(22,0) #Heating element 1 close
    GPIO.output(27,1) #Valve B close
    GPIO.output(25,0) #Heating element 2 close
    GPIO.output(26,0) #Valve C close
    GPIO.output(16,0) #Pump soap close
    boot=tkinter.messagebox.showwarning("Warning", "Please check the reservoir tank is filled")
    boot1=tkinter.messagebox.showwarning("Warning", "Please check the soap tank is filled")
    boot2=tkinter.messagebox.showwarning("Warning", "Please ensure the waste tank is empty")
   
   
def stepi():
    if analogInput(4) <= 900 :
        print("Cover lid close")    
        time.sleep(5)
    else:
        GPIO.output(23,0) #Pump water close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close 
        GPIO.output(26,0) #Valve C close
        GPIO.output(16,0) #Pump soap close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        stepi()
        
def step0():
    if analogInput(4) <= 900 :
        print("Safe to continue")
        if analogInput(4) <= 900 :
            GPIO.output(23,1) #Pump water open
            GPIO.output(22,0) #Heating element 1 close
            GPIO.output(27,0) #Valve B open
            GPIO.output(26,0) #Valve C close
            print("Pump open, Valve A and B open and C close")
            time.sleep(1)
            GPIO.output(22,1) #Heating element 1 OPEN
            time.sleep(70)
        else:
            GPIO.output(23,0) #Pump water close
            GPIO.output(22,0) #Heating element 1 close
            GPIO.output(27,1) #Valve B close
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(26,0) #Valve C close
            GPIO.output(16,0) #Pump soap close      
      

    else:
        GPIO.output(23,0) #Pump water close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,0) #Valve C close
        GPIO.output(16,0) #Pump soap close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step0()
       
def step1():
    
    if analogInput(4) <= 900 :
        print("safe to continue operation")
        
        if analogInput(5) >= 700:
            print("Continue Next Step")
            GPIO.output(22,0) #Heating element 1 close

            
        else:
            print("Warning Heating element 1 high")
            GPIO.output(22,0) #Heating element 1 close           
    else:
        GPIO.output(23,0) #Pump water close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,0) #Valve C close
        GPIO.output(16,0) #Pump soap close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step1() 


                   
def step2():
    if analogInput(4) <= 900 :
        print("Safe to continue")
        if analogInput(4) <= 900 :
            GPIO.output(23,1) #Pump water open
            GPIO.output(22,0) #Heating element 1 close
            GPIO.output(27,0) #Valve B open
            GPIO.output(26,0) #Valve C close
            GPIO.output(25,1) #Heating element 2 open
            print("Pump water, Heating element 2 and Valve B open, Valve C close")
            time.sleep(10)
            
            GPIO.output(23,0) #Pump water close
            GPIO.output(27,1) #Valve B close
            GPIO.output(26,0) #Valve C close
             
        else:
            GPIO.output(23,0) #Pump water close
            GPIO.output(22,0) #Heating element 1 close
            GPIO.output(27,1) #Valve B close
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(26,0) #Valve C close
            GPIO.output(16,0) #Pump soap close
    else:
        GPIO.output(23,0) #Pump water close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,0) #Valve C close
        GPIO.output(16,0) #Pump soap close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step2()


        

def step3():
    if analogInput(4) <= 900 :
        print ("Safe to continue") 
        if analogInput(6) <=700:
            print ("Continue Next Step")
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(23,0) #Pump water close
            GPIO.output(27,1) #Valve B close
        else:
            print("Warning Heating Element 2 high !")
            GPIO.output(23,0) #Pump water close
            GPIO.output(22,0) #Heating element 1 close
            GPIO.output(27,1) #Valve B open
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(26,0) #Valve C open
            GPIO.output(16,0) #Pump soap close
            temp()
    
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,0) #Valve C close
        GPIO.output(16,0) #Pump soap close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step3()
        
        
def step4():
    if analogInput(4) <= 900 :
        print ("Safe to continue") 
        if analogInput(4) <= 900 :
            GPIO.output(16,1) #Pump soap open
            time.sleep(3)
            GPIO.output(16,1) #Pump soap open
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(26,1) #Valve C open
            print("Valve C and Pump soap open")
            time.sleep(18)                                     
            GPIO.output(23,0) #Pump water close
            GPIO.output(22,0) #Heating element 1 close
            GPIO.output(27,1) #Valve B close
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(26,0) #Valve C close
            GPIO.output(16,0) #Pump soap close
            print("Valve C and Pump soap close")
        
        else:
            GPIO.output(23,0) #Pump close
            GPIO.output(22,0) #Heating element 1 close
            GPIO.output(27,1) #Valve B close
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(26,0) #Valve C close
            GPIO.output(16,0) #Pump soap close
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,0) #Valve C close
        GPIO.output(16,0) #Pump soap close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step4()


        
def step5():
    
    if analogInput(4) <= 900 :
        print("safe to continue operation")
        if analogInput(4) <= 900 :
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(26,1) #Valve C open
            print("Valve C open")
            time.sleep(28)
            GPIO.output(27,0) #Valve B open
        else:
            GPIO.output(23,0) #Pump water close
            GPIO.output(22,0) #Heating element 1 close
            GPIO.output(27,1) #Valve B close
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(26,0) #Valve C close
            GPIO.output(16,0) #Pump soap close
       
    else:
        GPIO.output(23,0) #Pump water close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,0) #Valve C close
        GPIO.output(16,0) #Pump soap close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step5() 
     
     
      
def stop_project():
    if analogInput(4) <= 900 :
        
        if analogInput(4) <= 900 :
            GPIO.output(23,0) #Pump water close
            GPIO.output(22,0) #Heating element 1 close
            GPIO.output(27,0) #Valve B open
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(26,0) #Valve C close
            GPIO.output(16,0) #Pump soap close
            print("End")
        else:
            GPIO.output(23,0) #Pump water close
            GPIO.output(22,0) #Heating element 1 close
            GPIO.output(27,1) #Valve B close
            GPIO.output(25,0) #Heating element 2 close
            GPIO.output(26,0) #Valve C close
            GPIO.output(16,0) #Pump soap close
    else:
        GPIO.output(23,0) #Pump water close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,0) #Valve C close
        GPIO.output(16,0) #Pump soap close
#         root=tk.Tk()
#         root.withdraw()
#         tkinter.messagebox.showwarning("Warning", "Warning cover open")
#         root.update()
        stop_project()
            
           
def take_straw():
    if analogInput(4) <= 900 :
        GPIO.output(23,0) #Pump water close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,0) #Valve B open
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,0) #Valve C close
        GPIO.output(16,0) #Pump soap close
#         top = tkinter.Toplevel()
#         top.title('Message')
#         Message=tkinter.Label(top, font='Times 15 bold', text='Please wait the straw to cool down ', padx=40, pady=40).pack()
#         start = time.time()
#         i = 130
#         label00 = tkinter.Label (top, text=str(int(i)) + 'sec' ,fg='green')
#         while (i>0):
#             i = 140 - (time.time() -start)
#             if i==130:
#                 break 
#         top.after(4000, top.destroy)
        
        root1=tkinter.messagebox.showinfo(title='Message', message="Please take the straw now ")
        
#progressbar
progress = ttk.Progressbar(window, style='text.Horizontal.TProgressbar', length=350, value=0)

style = ttk.Style(window)
style.layout('text.Horizontal.TProgressbar',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': ''})])
def restart():
    os.system("sudo reboot")
    
def bar(): 
    import time
    style.configure('text.Horizontal.TProgressbar', text='Idle',font="Times 16 bold", background='yellow'  )
    progress['value']=0
    window.update_idletasks()
    start_project()
    
    style.configure('text.Horizontal.TProgressbar', text=' Preparing for wash...')
    progress['value']=5
    window.update_idletasks() 
    stepi()
    
    progress['value']=10
    window.update_idletasks() 
    style.configure('text.Horizontal.TProgressbar', text='Preparing for wash...')
    step0()
    
    progress['value']=20
    window.update_idletasks() 
    style.configure('text.Horizontal.TProgressbar', text='Preparing for wash...')
    step1()
    
    progress['value']=25
    window.update_idletasks() 
    style.configure('text.Horizontal.TProgressbar', text='Preparing for wash...')
    step2()
    
    style.configure('text.Horizontal.TProgressbar', text='Preparing for wash...')
    progress['value']=30
    window.update_idletasks() 
    temp()
    
    
    style.configure('text.Horizontal.TProgressbar', text='Preparing for wash...')
    progress['value']=40
    window.update_idletasks() 
    step3()
    
    style.configure('text.Horizontal.TProgressbar', text='Wash')
    progress['value']=45
    window.update_idletasks() 
    step4()
    
    
    style.configure('text.Horizontal.TProgressbar', text='Preparing for rinse...')
    progress['value']=55
    window.update_idletasks() 
    step0()
    
   
    progress['value']=65
    window.update_idletasks()
    style.configure('text.Horizontal.TProgressbar', text='Preparing for rinse...')
    step1()
    
    
    progress['value']=70
    window.update_idletasks()
    style.configure('text.Horizontal.TProgressbar', text='Preparing for rinse...')
    step2()
    
    
    
    progress['value']=80
    window.update_idletasks()
    style.configure('text.Horizontal.TProgressbar', text='Preparing for rinse...')
    temp()
    
    progress['value']=85
    window.update_idletasks()
    style.configure('text.Horizontal.TProgressbar', text='Preparing for rinse...')
    step3()
    
    progress['value']=90
    window.update_idletasks()
    style.configure('text.Horizontal.TProgressbar', text='Rinse')
    step5()
    
    
    progress['value']=100
    window.update_idletasks()
    style.configure('text.Horizontal.TProgressbar', text='Please wait the straw to cool down') 
    time.sleep(400)
    stop_project()
    

    progress['value']
    window.update_idletasks()
    style.configure('text.Horizontal.TProgressbar', text='End operation')
    take_straw()
    restart()
    
    

progress.grid(row=80, column=205)
#label_3 = tk.Label(window, text="",font="Times 5 bold" )
#label_3.pack()

#button
def shut_down():
    command = "sudo shutdown -h +0"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]

label_3 = tk.Label(window, text="",font="Times 16 bold" )
label_3.grid(row=95,column=200)
Button1 = tkinter.Button(window,text='START',command =threading, font="Times 22 bold", bg="green", fg='white').grid(row=100, column=204)
 
Button = tkinter.Button(window,text='QUIT',command=shut_down, font="Times 22 bold", bg="red", fg='white').grid(row=100, column=206)
window.mainloop()


# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = analogInput(i)
    # Print the ADC values.
    #print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {26:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Pause for half a second.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                              
