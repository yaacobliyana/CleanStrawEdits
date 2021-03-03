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

#display rasp pi
window = tkinter.Tk()
window.title("Straw Cleaning Operation")
window.geometry('800x420')
# window.attributes('-fullscreen', True)

#spacing
label_8= tk.Label(window, text="",font="Times 20 bold" )
label_8.pack()

#logo
r = tkinter.Canvas(window, height=100, width=200)
photo = tkinter.PhotoImage(file= "/home/pi/Downloads/elquator-logo-oval-small-140x122.png")
background_label = tkinter.Label(window, image=photo)
background_label.pack()

#spacing
label_2= tk.Label(window, text="",font="Times 15 bold" )
label_2.pack()

#date
clock_label = tkinter.Label(window, text = "DATE:", font= "Times 18 bold ", )
clock_label.pack()

label_8= tk.Label(window, text="",font="Times 10 bold" )
label_8.pack()

#digital clock
clock_label=tkinter.Label(window, font="arial 14",fg="blue")
clock_label.pack()

def display_time():
    current_time = time.strftime("          %a %d-%m-%Y @ %H:%M:%S")
    clock_label["text"] = current_time
    window.after(800,display_time)
display_time()

label_1 = tk.Label(window, text="",font="Times 15 bold" )
label_1.pack()

#status
label_0 = tk.Label(window, text="STATUS:",font="Times 18 bold" )
label_0.pack()

spi = spidev.SpiDev() # Created an object
spi.open(0,0)

#relay
relay_pins = [23, 24, 22, 27, 25, 26, 16]
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
    GPIO.output(23,0) #Pump close
    GPIO.output(24,1) #Valve A close
    GPIO.output(22,0) #Heating element 1 close
    GPIO.output(27,1) #Valve B close
    GPIO.output(25,0) #Heating element 2 close
    GPIO.output(26,1) #Valve C close
    GPIO.output(16,1) #Valve D close
    
   
def stepi():
    time.sleep(1)
        
    if analogInput(0) >= 800:
       print("Cover lid close")    
       
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        stepi()
        
def step0():
    time.sleep(1)
    
    if analogInput(0) >= 800:
        print("safe to continue operation")
        GPIO.output(23,1) #Pump open
        GPIO.output(24,0) #Valve A open
        GPIO.output(27,0) #Valve B open
        GPIO.output(26,0)#Valve C open
        print("Pump open, Valve A, B and C open")
        time.sleep(30)
        GPIO.output(23,1) #Pump open
        GPIO.output(24,0) #Valve A open
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        print("Pump open, Fill tank 1, Valve A open")
        time.sleep(30)
         
    else:
        print("Please fill the reservoir tank")
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step0()  
                       
def step1():
    time.sleep(1)
   
    if analogInput(0) >= 800:
        print("safe to continue operation")      
        print("Tank 1 is filling up")
        GPIO.output(23,1) #Pump open
        GPIO.output(24,0) #Valve A open
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        time.sleep(20)
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        print("Tank 1 is full, Valve A close, Pump close")
    
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step1() 
            
            
def step2():
    time.sleep(1)
    
    if analogInput(0) >= 800:
        print("safe to continue operation")   
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,1) #Heating element 1 open
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        print("Temperature Tank 1 reach 90 degree Celcius, Heating element 1 open")
        time.sleep(120)
        
        
    else:
        print("Heating element 1 close")
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step2()
          
def step3():
    time.sleep(1)
     
    if analogInput(0) >= 800:
        print("safe to continue operation")
        GPIO.output(23,1) #Pump open
        GPIO.output(24,0) #Valve A open
        GPIO.output(27,0) #Valve B open
        GPIO.output(26,0)#Valve C open
        print("Pump open, Valve A, B and C open")
        time.sleep(30)
        GPIO.output(23,1) #Pump open
        GPIO.output(24,0) #Valve A open
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,0) #Valve B open
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        print("Valve A&B open, Pump open, Valve C close, Filling up Tank 2")
        time.sleep(120)
        
            
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step3()
        
           
def step4():
    time.sleep(1)
    
    if analogInput(0) >= 800:
        print("safe to continue operation")
        print("Tank 2 is full, Valve A&B close, Pump close")
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,1) #Heating element 2 open
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        print(" Heating element 2 open")
        time.sleep(120)      
        print("Heating element 2 close")
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close         
    
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step4()
  
def step5():
    time.sleep(1)
    
    if analogInput(0) >= 800:
        print("safe to continue operation")
        GPIO.output(23,1) #Pump open
        GPIO.output(24,0) #Valve A open
        GPIO.output(27,0) #Valve B open
        GPIO.output(26,0)#Valve C open
        GPIO.output(16,0) #Valve D open
        print("Pump open, all valves open")
        time.sleep(30)
        GPIO.output(26,0) #Valve C open
        GPIO.output(16,0) #Valve D open
        print("Valve C&D open ")
        print("Return to step1")
        time.sleep(30)
                  
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step5()
   
def step6():
    time.sleep(1)
    
    if analogInput(0) >= 800:
        print("safe to continue operation")
        print("Tank 1 is filling up")
        GPIO.output(23,1) #Pump open
        GPIO.output(24,0) #Valve A open
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        time.sleep(20)
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        print("Tank 1 is full, Valve A close, Pump close")
        
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step6()
        
def step7():
    time.sleep(1)
    
    if analogInput(0) >= 800:
        print("safe to continue operation")
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,1) #Heating element 1 open
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        print("Temperature Tank 1 reach 90 degree Celcius, Heating element 1 open")
        time.sleep(30)
        print("Heating element 1 close")
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close            
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step7() 
     
     
def step8():
    time.sleep(1)
    
    if analogInput(0) >= 800:
        print("safe to continue operation")
        GPIO.output(23,1) #Pump open
        GPIO.output(24,0) #Valve A open
        GPIO.output(27,0) #Valve B open
        GPIO.output(26,0)#Valve C open
        print("Pump open, Valve A, B and C open")
        time.sleep(40)
        GPIO.output(23,1) #Pump open
        GPIO.output(24,0) #Valve A open
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,0) #Valve B open
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        print("Valve A&B open, Pump open, Valve C close, Filling up Tank 2")
        time.sleep(120)
        
            
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step8()
      
def step9():
    time.sleep(1)
    
    if analogInput(0) >= 800:
        print("safe to continue operation")
        print("Tank 2 is full, Valve A&B close, Pump close")
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,1) #Heating element 2 open
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        print(" Heating element 2 open")
        time.sleep(80)      
        print("Heating element 2 close")
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close   
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step9() 
             
def step10():
    time.sleep(1)
    
    if analogInput(0) >= 800:
        print("safe to continue operation")
        GPIO.output(23,1) #Pump open
        GPIO.output(24,0) #Valve A open
        GPIO.output(27,0) #Valve B open
        GPIO.output(26,0)#Valve C open
        print("Pump open, valve A, B and C open")
        time.sleep(30)
       
    else:
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Warning cover open")
        root.update()
        step10() 
     
      
def stop_project():
    if analogInput(0) >= 800:
        print("safe to continue operation")
        GPIO.output(23,0) #Pump close
        GPIO.output(24,1) #Valve A close
        GPIO.output(22,0) #Heating element 1 close
        GPIO.output(27,1) #Valve B close
        GPIO.output(25,0) #Heating element 2 close
        GPIO.output(26,1) #Valve C close
        GPIO.output(16,1) #Valve D close
        print("End")
        time.sleep(30)
        root=tk.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Warning", "Available to take straw now")
        root.update()
        
#progressbar
progress = ttk.Progressbar(window, style='text.Horizontal.TProgressbar', length=500, value=0)

style = ttk.Style(window)
style.layout('text.Horizontal.TProgressbar',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': ''})])
              
def bar(): 
    import time 
    progress['value']=0
    window.update_idletasks() 
    style.configure('text.Horizontal.TProgressbar', text='Idle',font="Times 16 bold", background='yellow'  )
    time.sleep(1)
    start_project()
    
    progress['value']=5
    window.update_idletasks() 
    style.configure('text.Horizontal.TProgressbar', text='Preparing for wash...')
    stepi()
    step0()
    step1()
    step2()
    step3()
    step4()
    
   
    progress['value']=20
    window.update_idletasks() 
    style.configure('text.Horizontal.TProgressbar', text='Wash')
    time.sleep(1)
    step5()
    
   
    progress['value']=50
    window.update_idletasks()
    style.configure('text.Horizontal.TProgressbar', text='Preparing for rinse...')
    time.sleep(1)
    step6()
    step7()
    step8()
    
    
    progress['value']=60
    window.update_idletasks()
    style.configure('text.Horizontal.TProgressbar', text='Rinse')
    time.sleep(1)
    step9()
    
    progress['value']=70
    window.update_idletasks()
    style.configure('text.Horizontal.TProgressbar', text='End Operation')
    time.sleep(1)
    step10()
    
    progress['value']=100
    style.configure('text.Horizontal.TProgressbar')
    time.sleep(1)
    stop_project()
    #progress.stop()
  

label_4 = tk.Label(window, text="",font="Times 5 bold" )
label_4.pack()
progress.pack()
label_3 = tk.Label(window, text="",font="Times 5 bold" )
label_3.pack()

#button
def shut_down():
    command = "sudo shutdown -h +0"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]

Button = tkinter.Button(window,text='START',command=bar, font="Times 18 bold", bg="green", fg='white').pack(padx=160, pady=5, side=tkinter.LEFT)
Button = tkinter.Button(window,text='END',command=shut_down, font="Times 18 bold", bg="red", fg='white').pack(padx=140, pady=5, side=tkinter.LEFT)
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


GPIO.cleanup() 

