ROUND_KEY_LEN = 5
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ '


def fit_to_alphabet(val):
  return val % len(ALPHABET)


def get_round_key(key, round, round_len=ROUND_KEY_LEN):
  round_key = [fit_to_alphabet(key) + round]
  for i in range(round_len-1):
    round_key.append(fit_to_alphabet(round_key[i] * 1103515245 + 12345 * round))
  return round_key


def encrypt(key, phrase):
  result = ''
  round = 0
  total_index = 0
  while len(result) < len(phrase):
    round_key = get_round_key(key, round)
    for i in range(len(round_key)):
      if ALPHABET.find(phrase[total_index]) == - 1:
        result += phrase[total_index]
        total_index += 1
        if len(result) >= len(phrase):
          break
        continue

      new_letter_idx = fit_to_alphabet(ALPHABET.find(phrase[total_index]) ^ round_key[i])
      result += ALPHABET[new_letter_idx]
      total_index += 1
      if len(result) >= len(phrase):
        break
    round += 1
  
  return(result)


def decrypt(key, phrase):
  return encrypt(key, phrase)    

def main():
  print('Welcome! You are going to encrypt/decrypt the phrase!')
  print('To encrypt the phrase print "0" below. To decrypt - "1"')
  mode = int(input())
  print('Please enter the key (integer):')
  key = int(input())
  print('Please enter the phrase:')
  phrase = str(input())

  if mode == 0:
    print(encrypt(key, phrase))
  elif mode == 1:
    print(decrypt(key, phrase))


if __name__ == '__main__':
  main()
