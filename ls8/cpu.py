"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xf4
        self.equal = 0b00000000

        self.bin_table = {
            "HLT": 0b00000001,
            "LDI": 0b10000010,
            "PRN": 0b01000111,
            "MUL": 0b10100010,
            "ADD": 0b10100000,
            "PUSH": 0b01000101,
            "POP": 0b01000110,
            "CALL": 0b01010000,
            "RET": 0b00010001,
            "CMP": 0b0100111
        }

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, word):
        self.ram[pc] = word
       

    def load(self):

        import sys
        """Load a program into memory."""

        address = 0

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

        program = []
        with open(sys.argv[1]) as f:
            for line in f:
                try:
                    line = line.split("#",1)[0]
                    line = int(line, 2)
                    program.append(line)
                except ValueError:
                    pass
        
        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
           
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == "ADD":
            self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100 #a is less than b
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010 #a is greater than b
            else:
                self.flag = 0b00000001 #they are equal

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
        while running == True:
            instruction = self.ram_read(self.pc)
            if instruction ==self.bin_table["HLT"]: #HLT
                running = False
                exit
            elif instruction == self.bin_table["LDI"]: #LDI 
                self.pc += 1
                register_to_set = self.ram_read(self.pc)
                self.pc += 1
                int_to_set = self.ram_read(self.pc)
                self.reg[register_to_set] = int_to_set
                self.pc += 1
            elif instruction == self.bin_table["PRN"]: #PRN
                self.pc += 1
                register_to_print = self.ram_read(self.pc)
                
                print(self.reg[register_to_print])
                self.pc += 1
            elif instruction == self.bin_table["MUL"]: #mult
                self.pc += 1
                reg_a = self.ram_read(self.pc)
                self.pc += 1
                reg_b = self.ram_read(self.pc)
                
                self.alu("MUL", reg_a, reg_b)

                self.pc += 1
            elif instruction == self.bin_table["ADD"]: #add
                self.pc += 1
                reg_a = self.ram_read(self.pc)
                self.pc += 1
                reg_b = self.ram_read(self.pc)

                self.alu("ADD", reg_a, reg_b)

                self.pc += 1
            elif instruction == self.bin_table["CMP"]: #cmp
                self.pc += 1
                reg_a = self.ram_read(self.pc)
                self.pc += 1
                reg_b = self.ram_read(self.pc)

                self.alu("CMP", reg_a, reg_b)

                self.pc += 1

            elif instruction == self.bin_table["PUSH"]: #PUSH
                self.reg[self.sp] -= 1
                self.reg[self.sp] &= 0xff

                #what's the value of the register?
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]

                #ok put that in memory
                push_to = self.reg[self.sp]
                self.ram[push_to] = value

                #now move the pc

                self.pc += 2

            elif instruction == self.bin_table["POP"]: #pop
                #grab our value from where the sp is pointing
                pop_from = self.reg[self.sp]
                value = self.ram[pop_from]

                #store it in the register it gave us
                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = value
                
                #increment since we popped
                self.reg[self.sp] += 1
                self.pc += 2

            elif instruction == self.bin_table["CALL"]: #CALL
                return_address = self.pc + 2 #hop after the register, this is where we'll fall back to

                #okay put it on the stack
                self.reg[self.sp] -= 1 #decrement the stack
                push_to = self.reg[self.sp]
                self.ram[push_to] = return_address

                #now set the pc to the sub addy
                reg_number = self.ram[self.pc + 1]
                subroutine_address = self.reg[reg_number]

                self.pc = subroutine_address

            elif instruction == self.bin_table["RET"]: #RETURN
                #grab the return addy from the top of the stack
                add_pop_from = self.reg[self.sp]
                return_address = self.ram[add_pop_from]
                self.reg[self.sp] += 1

                self.pc = return_address

            else:
                print(f"unknown instruction is {instruction}")
                running = False
