#Required Libraries
from machine import Pin, ADC 
import utime 
 
#Initialize Prepherials
POT_Value = ADC(26)
POT_Value2 = ADC(28)
conversion_factor = 3.3/(65536) 
 
#Main Application loop
f=open('/nothing.csv','a')
gesture="left"#Enter gesture here
iteration=2#Increase per iteration
# f.write("POT Value 1,POT Value 2,Gesture,Iteration\n")
start= utime.ticks_ms()
i=0
while (i <280):
    if utime.ticks_diff(utime.ticks_ms(), start) < 1000:
#         print(utime.ticks_diff(utime.ticks_ms(), start)) 
        semg1_value=POT_Value.read_u16()
        semg2_value=POT_Value2.read_u16()
        f.write(str(semg1_value)+","+str(semg2_value)+","+gesture+","+str(iteration)+"\n")
        print(POT_Value.read_u16() * conversion_factor,POT_Value2.read_u16() * conversion_factor)
        print(POT_Value.read_u16() ,POT_Value2.read_u16())
        i= i+1
     #   utime.sleep(0.3)
    else:
        break
f.close()