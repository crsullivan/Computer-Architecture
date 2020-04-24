"""CPU functionality."""
import time, threading
import sys
from time import sleep
from threading import Timer

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.sp = 7
        self.flg = 1
        print("RAM:", self.ram)
        print ("REGISTER:", self.reg)

    def load(self):
        """Load a program into memory."""
        program_filename = sys.argv[1]
        address = 0
        with open('./examples/'+program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                self.ram[address] = int(line, 2)

                address += 1
        # address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program_filename:
        #     self.ram_write(address, instruction)
        #     address += 1

        print("UPDATED RAM:", self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self, location):
        return self.ram[location]

    def ram_write(self, location, value):
        self.ram[location] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


# I started an out of spec implementation of timer interrupts, it runs and is kind of 
# funny but does not utilize cpu instructions explicitly


    def pause(self):
        print('\nThinking')
        time.sleep(2)
        print('\n...8')
        time.sleep(2)
        print('\n...bit')
        time.sleep(2)
        print('\n...brain')
        time.sleep(2)
        print('\n...hurts')
        time.sleep(8)
        print('\n...ow')
        time.sleep(5)
        print('\n...make it stop')
        time.sleep(5)
        print('\n...Im doing my best')
        time.sleep(5)
        print('\n...Core 0 Maximum Thermal Threshold Reached')
        time.sleep(5)
        print('\n...WARNING')
        time.sleep(5)
        print('\n...OW')
        time.sleep(5)
        print('\n...OW')
        time.sleep(5)
        print('\n...HELP')
        time.sleep(5)
        print('\n...PLEASE')


    
    def run(self):
      
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        # Sprint
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
        JMP = 0b01010100
        # stretch interrupts (unfinished)
        ST = 0b10000100
        IRET = 0b00010011
        PRA = 0b01001000

        running = True
        reg_tracker = 0
        input("\nPress Enter to run " + sys.argv[1])
        # t = Timer(2, self.pause)
        # t.start()
        # sleep(15)
        
        while running == True:
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            inst = self.ram_read(self.pc)
            if inst == LDI:
                # print(time.ctime())
                # threading.Timer(2, self.pause()).start()
                self.reg[operand_a] = operand_b
                reg_tracker += 1
                self.pc += 3
                print("UPDATED REGISTER:", self.reg)
                # time.sleep(2)
            elif inst == MUL:
                print("MULT:", self.reg[operand_a] * self.reg[operand_b])
                self.pc += 3
                # time.sleep(2)
            elif inst == PRN:
                print("PRN:", self.reg[operand_a], "<---------------------------------------------------------------------------------")
                self.pc += 2
                # time.sleep(2)
            elif inst == PUSH:
                print('PUSH')
                # decrement the stack pointer
                self.reg[self.sp] -= 1   # address_of_the_top_of_stack -= 1

                # copy value from register into memory
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]  # this is what we want to push
                print("VALUE:", value, "AT LOCATION:", reg_num)
                address = self.reg[self.sp]
                print('TO RAM ADDRESS:', address)
                self.ram[address] = value   # store the value on the stack
                print("UPDATED RAM:", self.ram)
                self.pc += 2
                # time.sleep(2)
            elif inst == POP: 
                address = self.reg[self.sp]
                print('POP')
                value = self.ram[address]
                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = value
                print("UPDATED REGISTER:", self.reg)
                self.reg[self.sp] += 1 
                self.pc += 2
                # time.sleep(2)
            elif inst == CALL:
                # compute return address
                return_addr = self.pc + 2

                # push on the stack
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = return_addr

                # Set the self.pc to the value in the given register
                reg_num = self.ram[self.pc + 1]
                dest_addr = self.reg[reg_num]

                self.pc = dest_addr
                # time.sleep(2)
            elif inst == ADD:
                self.reg[operand_a] = self.reg[operand_a] + self.reg[operand_b]
                print("UPDATED REGISTER:", self.reg)
                self.pc += 3
                # time.sleep(2)
            elif inst == RET:
                # pop return address from top of stack
                return_addr = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1

                # Set the pc
                self.pc = return_addr
                # time.sleep(2)
            elif inst == CMP:
                if self.reg[operand_a] == self.reg[operand_b]:
                    self.flg = 1    
                if self.reg[operand_a] < self.reg[operand_b]:
                    self.flg = 0 
                if self.reg[operand_a] > self.reg[operand_b]:
                    self.flg = 2 
                self.pc += 3
                # time.sleep(2)
            elif inst == JMP:
                print('JMP from', self.pc, 'TO', self.reg[operand_a])
                return_addr = self.reg[operand_a]
                self.pc = return_addr
                # time.sleep(2)
            elif inst == JEQ:
                return_addr = self.reg[operand_a]
                if self.flg == 1:
                    self.pc = return_addr
                    print("CONDITIONAL JUMP from", self.pc, 'TO', return_addr)
                    # time.sleep(2)
                else:
                    self.pc += 2
                    print("JEQ conditions not met")
                    # time.sleep(2)
            elif inst == JNE:
                return_addr = self.reg[operand_a]
                if not self.flg == 1:
                    self.pc = return_addr
                    print("CONDITIONAL JUMP from", self.pc, 'TO', return_addr)
                    # time.sleep(2)
                else:
                    self.pc += 2
                    print("JNE conditions not met")
                    # time.sleep(2)
            elif inst == PRA:
                print(ascii(self.reg[operand_a]))
                self.pc += 2
            elif inst == IRET:
                print('IRET')
                break
            elif inst == ST:
                print('ST', self.reg)
                self.reg[operand_a] = self.reg[operand_b]
                print("ST UPDATED REGISTER:", self.reg)
                self.pc += 3
            elif inst == HLT:
                running = False
            else:
                print("Unknown instruction:", inst, 'at location', self.pc)
                running = False

        # t.cancel()
