import re

rom_address_size = 10
rom_size = 1 << rom_address_size

output: list[list[str, int]] = []
labels = {}


def to_hex(x: int, max=None):
    return hex(x)[2:].zfill(max) if max else hex(x)[2:]


op_codes = {
    "nop": 0x0,
    "add": 0x1,
    "sub": 0x2,
    "mul": 0x3,
    "div": 0x4,
    "mod": 0x5,
    "not": 0x6,
    "and": 0x7,
    "or": 0x8,
    "xor": 0x9,
    "rsh": 0xA,
    "ldi": 0xB,
    "mov": 0xC,
    "cnd": 0xD,
    "cal": 0xE,
    "ret": 0xF,
}

op_args = {
    "nop": 0,
    "add": 2,
    "sub": 2,
    "mul": 2,
    "div": 2,
    "mod": 2,
    "not": 1,
    "and": 2,
    "or": 2,
    "xor": 2,
    "rsh": 2,
    "ldi": 2,
    "mov": 2,
    "cnd": 2,
    "cal": 1,
    "ret": 0,
    "cmp": 2,
    "jmp": 1,
    "jeq": 1,
    "jne": 1,
    "jgt": 1,
    "jlt": 1,
    "jge": 1,
    "jle": 1,
    "ext": 0,
}

cnd_ops = ["eq", "ne", "gt", "lt", "ge", "le", "j"]


def get_assembly(op: str, args: list[str]):
    if op not in op_args:
        raise Exception("Invalid instruction: " + op)

    if len(args) != op_args[op]:
        raise Exception("Invalid number of arguments for instruction: " + op)

    new_args = []

    if op == "cal" or op == "jmp":
        arg = args[0]

        if (
            not arg[0].isnumeric()
            and arg[0] != "."
            and (arg[0] not in ["+", "-"] or not arg[1:].isnumeric())
        ):
            raise Exception(
                "Expected call argument to be in the format: +<line> or -<line> or .<label> or <line>: "
                + arg
            )

        if op == "jmp":
            return [to_hex(op_codes["cnd"]) + to_hex(6, 4) + "$(" + arg + ")"]

        return [to_hex(op_codes[op]) + "$(" + arg + ")" + to_hex(0, 4)]

    for i, arg in enumerate(args):
        if isinstance(arg, int):
            new_args.append(to_hex(arg, 4))
            continue

        if op == "cnd" and i == 0:
            if arg not in cnd_ops:
                raise Exception("Invalid condition: " + arg)

            arg = str(cnd_ops.index(arg))
            args[i] = arg

        if not re.match(r"\$?[0-9]+", arg):
            raise Exception("Invalid argument: " + arg)

        if arg.startswith("$"):
            arg = arg[1:]

        if not arg.isnumeric():
            raise Exception("Invalid argument: " + arg)

        new_args.append(to_hex(int(arg), 4))

    if op == "cmp":
        return [
            *get_assembly("mov", ["0", args[0]]),
            *get_assembly("sub", ["0", args[1]]),
        ]

    if op == "ext":
        return [to_hex(op_codes["cnd"]) + to_hex(6, 4) + "$(+0)"]

    if len(args) > 1 and args[1][0] == "$" and op == "mov":
        return get_assembly("ldi", args)

    return [
        to_hex(op_codes[op])
        + "".join([to_hex(int(x.replace("$", "")), 4) for x in args])
        + "".join(["0000"] * (2 - len(args)))
    ]


def get_assembly_by_line(line: str, index: int):
    line = line.split(";")[0].replace(",", " ").strip().lower()
    spl = line.split()

    if len(spl) < 1:
        return None

    if line[0] == "." and len(spl) == 1:
        labels[line[1:]] = index
        return None

    op = spl[0]

    return get_assembly(op, spl[1:])


assembly_indices = {}

with open("program.asm") as f:
    lines = f.readlines()

    index = 0

    for i, line in enumerate(lines):
        assemblies = get_assembly_by_line(line, index)

        if assemblies is None:
            continue

        assembly_indices[i] = index

        for assembly in assemblies:
            output.append([i, assembly.replace("%", to_hex(index, 4))])

            index += 1


for i, (ind, asm) in enumerate(output):
    if "$(" in asm:
        pos1 = asm.index("$(")
        pos2 = asm.index(")") + 1

        val = asm[pos1 + 2 : pos2 - 1]
        val_temp = val

        if val[0] == ".":
            if val[1:] not in labels:
                raise Exception("Invalid jumping point: " + str(val_temp))

            val = to_hex(labels[val[1:]], 4)
        else:
            if val[0] in ["+", "-"]:
                val = ind + int(val)
            else:
                val = int(val) - 1

            if val not in assembly_indices:
                raise Exception("Invalid jumping point: " + str(val_temp))

            val = to_hex(assembly_indices[val], 4)

        output[i] = [ind, asm[:pos1] + val + asm[pos2:]]

output_text = "v3.0 hex words plain\n"

for i in range(rom_size - len(output)):
    output.append([0, "000000000"])

for i in range(0, len(output), 8):
    output_text += " ".join(map(lambda x: x[1], output[i : i + 8])) + "\n"

with open("program_rom", "w") as f:
    f.write(output_text)
