"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        print("RAM:", self.ram)
        print ("REGISTER:", self.reg)

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram_write(address, instruction)
            address += 1

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


    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        running = True
        reg_tracker = 0
        while running == True:
            inst = self.ram_read(self.pc)
            if inst == LDI:
                self.reg[self.pc] = self.ram_read(self.pc+1)
                self.pc += 1
                self.reg[self.pc] = self.ram_read(self.pc+1)
                self.pc += 2
                reg_tracker += 1
            elif inst == PRN:
                print("UPDATED REGISTER:", self.reg)
                print("PRINT LS8:", self.reg[reg_tracker])
                self.pc += 2
            elif inst == HLT:
                running = False
            else:
                print("Unknown instruction")

                running = False
