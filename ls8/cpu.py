"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 25
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, word):
        self.ram[pc] = word
       

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
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            pc += 1
        
        elif op == "PRN":
            print(self.reg[reg_a])
            pc += 1
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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
        self.pc = 0
        running = True
        print("we got to run!")
        while running == True:
            instruction = self.ram_read(self.pc)
            print(f"the instruction is {instruction}")
            if instruction == 0b00000001: #HLT
                print("halting...")
                running = False
                exit
            elif instruction == 0b10000010: #LDI 
                self.pc += 1
                register_to_set = self.ram_read(self.pc)
                self.pc += 1
                int_to_set = self.ram_read(self.pc)
                self.reg[register_to_set] = int_to_set
                print(f"stored {int_to_set} in {register_to_set}")
                self.pc += 1
            elif instruction == 0b01000111: #PRN
                self.pc += 1
                register_to_print = self.ram_read(self.pc)
                print("printing...")
                print(self.reg[register_to_print])
                self.pc += 1
            else:
                print("unknown instruction")
                running = False
