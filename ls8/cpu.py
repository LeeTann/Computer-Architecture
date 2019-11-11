"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory and 8 general-purpose registers.
        self.ram = [0] * 256 # 256 bytes of memory for instructions
        self.reg = [0] * 8 # 8 general-purpose registers
        self.pc = 0 # helps distinguish between operands and instructions
        self.reg[7] = 255
        self.sp = self.reg[7]

    #     self.ops = {
    #         LDI: self.op_ldi,
    #         HLT: self.op_hlt,
    #         PRN: self.op_prn,
    #         MUL: self.op_mul
    #     }

    # def op_ldi(self, address, value):
    #     self.reg[address] = value

    # def op_prn(self, address, operand_b):
    #     print(self.reg[address])

    # def op_hlt(self, operand_a, operand_b):
    #     self.hlt = True

    # def op_mul(self, address1, address2):
    #     self.alu('MUL', address1, address2)

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename) as file:
            for line in file:
                command_split = line.split('#')
                instruction = command_split[0]

                if instruction == "":
                    continue

                first_bit = instruction[0]

                if first_bit == '0' or first_bit == '1':
                    self.ram[address] = int(instruction[:8], 2) # convert instructions to binary
                    address += 1

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

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations. Arithetic logic unit"""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        """Run the CPU."""
        LDI = 0b10000010 # LDI R0,8   
        PRN = 0b01000111 # PRN R0     
        HLT = 0b00000001 # HLT
        MUL = 0b10100010      
        PUSH = 0b01000101
        POP = 0b01000110

        running = True

        while running:
            command = self.ram_read(self.pc) # get instructions

            operand_a = self.ram_read(self.pc + 1) # reg location
            operand_b = self.ram_read(self.pc + 2) # value

            # operand_size = command >> 6 # get operand size by shifting 6
            # instruction_set = ((command >> 4) & 0b1) == 1

            if command == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif command == PRN:
                operand_a = self.ram[self.pc + 1]
                print(self.reg[operand_a])
                self.pc += 2
            elif command == MUL:

                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif command == HLT:
                running = False

            elif command == PUSH:
                self.sp -= 1
                self.ram[self.sp] = self.reg[operand_a]
                self.pc += 2
            
            elif command == POP:
                self.reg[operand_a] = self.ram[self.sp]
                self.sp += 1
                self.pc += 2