import json
import struct
import sys


def interpret(input_file, output_file, memory_size=1024):
    memory = [0] * memory_size
    accumulator = 0

    with open(input_file, 'rb') as f:
        code = f.read()

    pc = 0
    while pc < len(code):
        opcode = code[pc]
        operand = struct.unpack('<I', code[pc+1:pc+5])[0]
        pc += 5

        if opcode == 0x20:  # LOAD_CONST
            accumulator = operand
        elif opcode == 0xC4:  # LOAD_MEM
            address = (accumulator + operand) % memory_size
            accumulator = memory[address]
        elif opcode == 0x40:  # STORE_MEM
            address = operand % memory_size
            memory[address] = accumulator
        elif opcode == 0x41:  # NEG
            accumulator = -accumulator
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    with open(output_file, 'w') as f:
        json.dump({"accumulator": accumulator, "memory": memory}, f, indent=4)


if __name__ == "__main__":
    interpret(sys.argv[1], sys.argv[2])
