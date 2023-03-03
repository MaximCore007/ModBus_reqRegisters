''' xxx '''

import threading
import serial
import serial.tools.list_ports
import minimalmodbus

SLAVE_ID = 1

isRequest = 0
isExit = 0
    
def uart_task(event, com, num_smpl, time):
    # tmr = threading.Timer(0.5, hello)
    # tmr.start()
    # ser = serial.Serial() 
    # ser.baudrate = 115200
    # ser.port = 'COM10'

    instrument = minimalmodbus.Instrument(com, 1)  # port name, slave address (in decimal)
    ser_name = instrument.serial.port                  # this is the serial port name               
    instrument.serial.baudrate = 115200                # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 0.5                   # seconds
    slv_addr = instrument.address                      # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU           # rtu or ascii mode
    instrument.clear_buffers_before_each_transaction = True
 
    if instrument.serial.is_open:
        print("Open port: "+ser_name)
        print("Connect with slave ID: " + str(slv_addr))

        # full_name = "heap/D-13_"+name+"_{}.bin".format(self.n_files)
        full_name = "registers_41and42.csv"
        file1 = open(full_name, 'w', encoding="utf-8")
        print("Open file: "+full_name)
        print()
        for i in range(num_smpl):
            Reg41 = instrument.read_register(41)        # Registernumber, number of decimals
            Reg42 = instrument.read_register(42)        # Registernumber, number of decimals
            values_reg = f"%1d;%1d\n" %(Reg41, Reg42) 
            print(f"Reade data Register 41: %1d" %Reg41)
            print(f"Reade data Register 42: %1d" %Reg42)
            print()
            file1.write(values_reg)
            event.wait(time)
            
        file1.close()
    else:
        print("Serial port is not open :(")

    print(f"Данные записаны в файл {full_name}, количество выборок {num_smpl}, с интервалом {time} с.")

# def key_read():
#     print("---------------------------------")
#     print("b - begin request")
#     print("s - stop request")
#     print("x - exit")
#     k = input()
#     return k
#
# def keyRead_task():
#     key = key_read()
#
#     while True:
#         if (key == 'b'):
#             isRequest = 1
#         elif (key == 's'):
#             isRequest = 0
#         elif (key == 'x'):
#             isExit = 1


def main():
    mutex = threading.Lock()
    event = threading.Event()
    
    ports = serial.tools.list_ports.comports()
    print("Доступные COM-порты:")
    for port, desc, hwid in sorted(ports):
        print("Имя: {}; Описание: {}.".format(port, desc))
    print("Введите номер COM-порта:")
    com_port = f"COM{input()}"
    print("Введите кол-во выборок:")
    num_samples = int(input())
    print("Введите задержку между выборками, мс.:")
    timeout = float(input()) / 1000.0

    # print("start threads...")
    uart = threading.Thread(target=uart_task, args=(event, com_port, num_samples, timeout))
    # keyrd = threading.Thread(target=keyRead_task)
    
    uart.start()
    # keyrd.start()
    
    uart.join()
    # keyrd.join()

    input('Press ENTER to exit')
    
if __name__ == '__main__':
    main()
