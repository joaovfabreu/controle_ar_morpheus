#!/usr/bin/env python3
"""
Análise de Padrões - Códigos IR AC UNKNOWN
Analisa os códigos de temperatura para identificar padrões
"""

# Códigos capturados (temperatura : código hex 128 bits)
# Mostrando apenas os primeiros 32 bits (4 bytes) que o IRrecvDumpV2 exibe
codigos = {
    30: 0x1713C7A5,
    29: 0x3E4856FE,
    28: 0x39E985BC,
    27: 0x22604B1A,
    26: 0x87F9B868,
    25: 0x3946E0AA,
    24: 0xDF56E3B8,
    23: 0xEDBC0F6A,
    22: 0x279643B0,
    21: 0x7D7DB941,
    20: 0x791EE7FF,
    19: 0xC25C99D3,
    18: 0xB9B2F605,
    17: 0xD6DDFFB5,
    16: 0xCF6E6873,
}

print("="*80)
print("ANÁLISE DE PADRÕES - CÓDIGOS IR AC")
print("="*80)
print()

# Análise 1: Códigos em Hexadecimal
print("1. CÓDIGOS EM HEXADECIMAL (primeiros 32 bits / 4 bytes)")
print("-"*80)
for temp in sorted(codigos.keys(), reverse=True):
    codigo = codigos[temp]
    print(f"{temp}°C: 0x{codigo:08X}")
print()

# Análise 2: Códigos em Binário
print("2. CÓDIGOS EM BINÁRIO (primeiros 32 bits / 4 bytes)")
print("-"*80)
for temp in sorted(codigos.keys(), reverse=True):
    codigo = codigos[temp]
    binario = format(codigo, '032b')
    # Quebra em bytes para facilitar leitura
    bytes_bin = [binario[i:i+8] for i in range(0, 32, 8)]
    print(f"{temp}°C: {' '.join(bytes_bin)}")
print()

# Análise 3: Análise Byte a Byte
print("3. ANÁLISE BYTE A BYTE")
print("-"*80)
for byte_pos in range(4):
    print(f"\nBYTE {byte_pos} (bits {byte_pos*8}-{byte_pos*8+7}):")
    valores = {}
    for temp in sorted(codigos.keys(), reverse=True):
        codigo = codigos[temp]
        byte_val = (codigo >> (24 - byte_pos*8)) & 0xFF
        valores[temp] = byte_val
        print(f"  {temp}°C: 0x{byte_val:02X} = {byte_val:3d} = {format(byte_val, '08b')}")
    
    # Verifica se há padrão
    vals = list(valores.values())
    if len(set(vals)) == 1:
        print(f"  → CONSTANTE! Todos = 0x{vals[0]:02X}")
    elif len(set(vals)) == len(vals):
        print(f"  → TODOS DIFERENTES - pode ser relacionado à temperatura")
    else:
        print(f"  → {len(set(vals))} valores únicos de {len(vals)} temperaturas")

# Análise 4: XOR entre temperaturas consecutivas
print("\n4. DIFERENÇAS (XOR) ENTRE TEMPERATURAS CONSECUTIVAS")
print("-"*80)
temps = sorted(codigos.keys(), reverse=True)
for i in range(len(temps)-1):
    t1, t2 = temps[i], temps[i+1]
    c1, c2 = codigos[t1], codigos[t2]
    diff = c1 ^ c2
    bits_diferentes = bin(diff).count('1')
    print(f"{t1}°C → {t2}°C: {bits_diferentes:2d} bits diferentes | XOR = 0x{diff:08X}")
print()

# Análise 5: Busca por padrões de checksum
print("5. POSSÍVEIS CHECKSUMS")
print("-"*80)
print("Testando soma simples dos bytes:")
for temp in sorted(codigos.keys(), reverse=True):
    codigo = codigos[temp]
    bytes_vals = [(codigo >> (24 - i*8)) & 0xFF for i in range(4)]
    soma = sum(bytes_vals) & 0xFF
    print(f"{temp}°C: bytes={bytes_vals} → soma%256 = {soma} (0x{soma:02X})")
print()

# Análise 6: Correlação bit a bit
print("6. BITS QUE MUDAM SEMPRE")
print("-"*80)
# Para cada posição de bit, verifica quantas vezes muda
bit_changes = [0] * 32
temps_sorted = sorted(codigos.keys(), reverse=True)
for i in range(len(temps_sorted)-1):
    c1 = codigos[temps_sorted[i]]
    c2 = codigos[temps_sorted[i+1]]
    diff = c1 ^ c2
    for bit_pos in range(32):
        if diff & (1 << (31-bit_pos)):
            bit_changes[bit_pos] += 1

print("Bits que mudam com frequência (podem estar relacionados à temperatura):")
for bit_pos in range(32):
    changes = bit_changes[bit_pos]
    if changes > len(temps_sorted) // 3:  # Muda em mais de 1/3 das transições
        byte_num = bit_pos // 8
        bit_in_byte = bit_pos % 8
        print(f"  Bit {bit_pos:2d} (Byte {byte_num}, bit {bit_in_byte}): muda {changes}/{len(temps_sorted)-1} vezes")
print()

# Análise 7: Estatísticas gerais
print("7. ESTATÍSTICAS GERAIS")
print("-"*80)
all_codes = list(codigos.values())
print(f"Total de códigos: {len(all_codes)}")
print(f"Códigos únicos: {len(set(all_codes))}")
print(f"Menor código: 0x{min(all_codes):08X} ({min(codigos.keys())}°C)")
print(f"Maior código: 0x{max(all_codes):08X} ({max(codigos.keys())}°C)")
print()

# Análise 8: Busca por nibbles (4 bits) que podem codificar temperatura
print("8. ANÁLISE POR NIBBLES (4 bits)")
print("-"*80)
print("Buscando nibbles que possam codificar temperatura (16-30 = 15 valores):")
for nibble_pos in range(8):  # 8 nibbles em 32 bits
    print(f"\nNIBBLE {nibble_pos} (bits {nibble_pos*4}-{nibble_pos*4+3}):")
    valores = {}
    for temp in sorted(codigos.keys(), reverse=True):
        codigo = codigos[temp]
        nibble_val = (codigo >> (28 - nibble_pos*4)) & 0x0F
        valores[temp] = nibble_val
        print(f"  {temp}°C: 0x{nibble_val:X} = {nibble_val:2d} = {format(nibble_val, '04b')}")
    
    # Verifica se valores estão na faixa esperada
    vals = list(valores.values())
    unique_vals = set(vals)
    if min(vals) >= 0 and max(vals) <= 14:  # 15 valores possíveis (0-14)
        print(f"  → POSSÍVEL! Valores na faixa 0-14, encontrados: {sorted(unique_vals)}")
    elif len(unique_vals) == len(vals):
        print(f"  → Todos diferentes mas fora da faixa ideal")

print("\n" + "="*80)
print("ANÁLISE CONCLUÍDA")
print("="*80)
