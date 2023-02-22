''' xxx '''


import threading
import serial
import minimalmodbus

SLAVE_ID = 1

isRequest = 0

def key_read():
    print("---------------------------------")
    print("b - begin request")
    print("s - stop request")
    k = input()
    return k
    
def uart_task():
    # tmr = threading.Timer(0.5, hello)
    # tmr.start()
    # ser = serial.Serial() 
    # ser.baudrate = 115200
    # ser.port = 'COM10'

    instrument = minimalmodbus.Instrument('COM10', 1)  # port name, slave address (in decimal)
    ser_name = instrument.serial.port                  # this is the serial port name               
    instrument.serial.baudrate = 115200                # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 5.0                   # seconds
    slv_addr = instrument.address                      # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU           # rtu or ascii mode
    instrument.clear_buffers_before_each_transaction = True
    
    print("Open port: "+ser_name)
    print("Connect with: "+str(slv_addr))  
    
    while True:
        Reg41 = instrument.read_register(41)        # Registernumber, number of decimals
        Reg42 = instrument.read_register(42)        # Registernumber, number of decimals
        print("Reade data Register 41"+str(Reg41))
        print("Reade data Register 42"+str(Reg42))
        print()

def keyRead_task():
    key = key_read()
        
    if (key == 'b'):
        isRequest = 1
    elif (key == 's'):
        isRequest = 0

def main():
    # mutex = threading.Lock()

    print("start threads...")
    uart = threading.Thread(target=uart_task)
    # keyrd = threading.Thread(target=keyRead_task)

    uart.start()
    # keyrd.start()
    
    uart.join()
    # keyrd.join()

if __name__ == '__main__':
    main()
