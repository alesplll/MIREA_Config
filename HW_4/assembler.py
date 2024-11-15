import json
import struct
import sys


def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    binary_code = bytearray()
    log = []

    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue

        opcode = parts[0]
        operand = int(parts[1])

        if opcode == "LOAD_CONST":
            binary_code.extend(struct.pack('<B', 0x20))
        elif opcode == "LOAD_MEM":
            binary_code.extend(struct.pack('<B', 0xC4))
        elif opcode == "STORE_MEM":
            binary_code.extend(struct.pack('<B', 0x40))
        elif opcode == "NEG":
            binary_code.extend(struct.pack('<B', 0x41))
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

        binary_code.extend(struct.pack('<I', operand))
        log.append({"instruction": opcode, "operand": operand})

    with open(output_file, 'wb') as f:
        f.write(binary_code)

    with open(log_file, 'w') as f:
        json.dump(log, f, indent=4)


if __name__ == "__main__":
    assemble(sys.argv[1], sys.argv[2], sys.argv[3])
