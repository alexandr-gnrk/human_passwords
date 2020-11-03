import string
import random
from functools import partial


def load_passwords_from_file(filepath):
    passwords = list()
    with open(filepath) as file:
        for line in file:
            passwords.append(line.strip())
    return passwords


TOP100K = load_passwords_from_file('./data/common100Kpass.txt')
TOP110 = load_passwords_from_file('./data/common110pass.txt')
WORDS = load_passwords_from_file('./data/common_words.txt')


def get_random_password(
        length, 
        charset=string.ascii_letters+string.digits+string.punctuation):
    return ''.join(random.choices(charset, k=length))


def get_humanlike_password(words, minlen=6, maxlen=16):
    password = str()
    length = random.randint(minlen, maxlen)

    def random_digit():
        return random.choice(string.digits)
    
    def random_word():
        word = random.choice(words)
        if random.random() < 0.35:
            word = word[0].upper() + word[1:]
        return word
    
    def random_punctuation():
        return random.choice('*_.!+-')

    while len(password) < length:
        part = random.choices(
            (random_word, random_digit, random_punctuation),
            (0.65, 0.25, 0.1))[0]()
        password += part

    if len(password) > length:
        password = password[:length]

    return password


def get_password_generator():
    while True:
        yield random.choices(
            (
                partial(random.choice, TOP100K),
                partial(random.choice, TOP110),
                partial(get_random_password, random.randint(6, 16)),
                partial(get_humanlike_password, WORDS)),
            (10, 75, 5, 10))[0]()