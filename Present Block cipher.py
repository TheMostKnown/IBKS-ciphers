from bitstring import BitArray
import sys

KEY = 0
S = {'0': 'c', '1': '5', '2': '6', '3': 'b', '4': '9', '5': '0', '6': 'a', '7': 'd', '8': '3', '9': 'e', 'a': 'f', 'b': '8', 'c': '4', 'd': '7', 'e': '1', 'f': '2'}

S_rev = {'c': '0', '5': '1', '6': '2', 'b': '3', '9': '4', '0': '5', 'a': '6', 'd': '7', '3': '8', 'e': '9', 'f': 'a', '8': 'b', '4': 'c', '7': 'd', '1': 'e', '2': 'f'}

def addRoundKey(key, block):
  return bytes(a ^ b for a, b in zip(key, block))


def sBoxlayer(block):
  hexed_block = block.hex()
  output = ''
  for i in range(len(hexed_block)):
    output += S[hexed_block[i]]
  return output # in hex format


def sBoxlayer_rev(block):
  hexed_block = block.hex()
  output = ''
  for i in range(len(hexed_block)):
    output += S_rev[hexed_block[i]]
  return output # in hex format


def P_idx(index):
  return (index // 4) + 16 * (index % 4)


def P_idx_rev(index):
  return (index // 16) + 4 * (index % 16)


def pBoxlayer(hexed_block):
  binary_block = BitArray(hex=hexed_block).bin
  output = list(binary_block)
  for i in range(64):
    output[P_idx(i)] = binary_block[i]

  output = str(hex(int(''.join(output), base=2)))
  output = output[2:]
  while len(output) < 16:
    output = '0' + output
  return bytes.fromhex(output)


def pBoxlayer_rev(hexed_block):
  binary_block = BitArray(hex=hexed_block).bin
  output = list(binary_block)
  for i in range(64):
    output[P_idx_rev(i)] = binary_block[i]

  output = str(hex(int(''.join(output), base=2)))
  output = output[2:]
  while len(output) < 16:
    output = '0' + output
  return bytes.fromhex(output)


def round(main_key, block, round_keys, round_num):
  round_key = round_keys[round_num]
  block = addRoundKey(round_key, block)
  block = sBoxlayer(block) # hexed
  block = pBoxlayer(block)
  return block
  

def round_rev(main_key, block, round_keys, round_num):
  round_key = round_keys[round_num]
  block = addRoundKey(round_key, block)
  
  block = pBoxlayer_rev(block.hex())
  block = sBoxlayer_rev(block) # hexed
  block = bytes.fromhex(block)
  return block


def get_round_keys(key, rounds):
  roundkeys = []
  for i in range(1, rounds + 1):
    round_key = hex(key >> 16)[2:]
    while len(round_key) < 16:
      round_key = '0' + round_key
    roundkeys.append(bytes.fromhex(round_key))

    key = ((key & (2 ** 19 - 1)) << 61) + (key >> 19)

    key = (int(S[hex(key >> 76)[2:]], base=16) << 76) + (key & (2 ** 76 - 1))
    key ^= i << 15
  return roundkeys


def encrypt_block(block, main_key):
  round_keys = get_round_keys(main_key, 32)
  for i in range(31):
    block = round(main_key, block, round_keys, i)

  block = addRoundKey(round_keys[-1], block)
  return block

def decrypt_block(block, main_key):
  round_keys = get_round_keys(main_key, 32)
  round_keys.reverse()
  
  for i in range(31):
    block = round_rev(main_key, block, round_keys, i)

  return block

def test():
  block = b'\x00\x00\x00\x00\x00\x00\x00\x00'
  encoded = encrypt_block(block, KEY)
  print('ENC:', encoded.hex())
  decoded = decrypt_block(encoded, KEY)
  print('DEC:', decoded.hex())


def main():
  argv = sys.argv[1:]
  if len(argv) != 3:
    print('Usage: ./script.py -e(-d) sourcename stockname')
    return(1)

  
  source = open(argv[1], 'rb')
  stock = open(argv[2], 'wb')

  if argv[0] == '-d':
    func = decrypt_block
  else:
    func = encrypt_block
    

  block = source.read(8)
  
  while(block):
    if len(block) < 8:
      block = block + b'\x00'*(8 - len(block))

    stock.write(func(block, KEY))
    block = source.read(8)
    
  
  source.close()
  stock.close()

if __name__ == '__main__':
  main()

