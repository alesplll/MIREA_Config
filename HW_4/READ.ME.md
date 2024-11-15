1. **Ассемблер**: принимает читаемый текстовый файл с исходным кодом УВМ и преобразует его в бинарный файл.
2. **Интерпретатор**: выполняет бинарные команды и сохраняет результат в выходном файле.

### Структура системы команд:

1. **Загрузка константы (0x20)**:
   - Команда: `LOAD_CONST B`
   - Формат: `[0x20][B (4 байта)]`
   
2. **Чтение значения из памяти (0xC4)**:
   - Команда: `LOAD_MEM B`
   - Формат: `[0xC4][B (4 байта)]`
   
3. **Запись значения в память (0x40)**:
   - Команда: `STORE_MEM B`
   - Формат: `[0x40][B (4 байта)]`

4. **Унарный минус (0x41)**:
   - Команда: `NEG B`
   - Формат: `[0x41][B (4 байта)]`

### Ассемблер:
```python
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
```

### Интерпретатор:
```python
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
```

### Пример тестовой программы:

**Ассемблерный код (`input.txt`)**:
```
LOAD_MEM 0   ; Загрузка значения из памяти по адресу 0
NEG 0        ; Применение унарного минуса
STORE_MEM 100 ; Сохранение результата по адресу 100
LOAD_MEM 1
NEG 1
STORE_MEM 101
LOAD_MEM 2
NEG 2
STORE_MEM 102
LOAD_MEM 3
NEG 3
STORE_MEM 103
LOAD_MEM 4
NEG 4
STORE_MEM 104
```
### Запуск
```bash
python assembler.py input.txt output.bin log.json
python interpreter.py output.bin result.json
```

### Результат:
`log.json`
```json
[
{
"instruction": "LOAD_MEM",
"operand": 0
},
{
"instruction": "NEG",
"operand": 0
},
{
"instruction": "STORE_MEM",
"operand": 100
},
{
"instruction": "LOAD_MEM",
"operand": 1
},
{
"instruction": "NEG",
"operand": 1
},
{
"instruction": "STORE_MEM",
"operand": 101
},
{
"instruction": "LOAD_MEM",
"operand": 2
},
{
"instruction": "NEG",
"operand": 2
},
{
"instruction": "STORE_MEM",
"operand": 102
},
{
"instruction": "LOAD_MEM",
"operand": 3
},
{
"instruction": "NEG",
"operand": 3
},
{
"instruction": "STORE_MEM",
"operand": 103
},
{
"instruction": "LOAD_MEM",
"operand": 4
},
{
"instruction": "NEG",
"operand": 4
},
{
"instruction": "STORE_MEM",
"operand": 104
}
]
```

`result.json`
```json
{

"accumulator": 0,

"memory": [
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,

0,
0,
0,
0,
0,
0,
0,
0,
0,

,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,

,
0,
0,
0,
0,
0,
0,
0,

,
0,
0,
0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0,

0

]

}

```