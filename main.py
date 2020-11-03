import csv
import hashlib
import uuid
import time
import random
from base64 import b64encode

import bcrypt
from loguru import logger
from progressbar import progressbar

import password_generator as pswd_gen


PASSWORD_AMOUNT = 100000
MD5_PATH = './hashes/md5.csv'
SHA1_PATH = './hashes/sha1.csv'
BCRYPT_PATH = './hashes/bcrypt.csv'

random.seed(time.time())
logger.info('Creating password generator')
pswd_gen = pswd_gen.get_password_generator()

logger.info('{} password hashes will be generated for each type of hashfunc'.format(PASSWORD_AMOUNT))

logger.info('Generating MD5 password hashes and saving into {}'.format(MD5_PATH))
with open(MD5_PATH, 'w') as csvfile:
    hash_row = {'hash': None}
    writer = csv.DictWriter(csvfile, fieldnames=hash_row.keys())
    writer.writeheader()
    for _ in progressbar(range(PASSWORD_AMOUNT)):
        pswd = bytes(next(pswd_gen), encoding='ascii')
        hash_row['hash'] = b64encode(hashlib.md5(pswd).digest()).decode()
        writer.writerow(hash_row)

logger.info('Generating SHA1 password hashes and saving into {}'.format(SHA1_PATH))
with open(SHA1_PATH, 'w') as csvfile:
    hash_row = {'hash': None, 'salt': None}
    writer = csv.DictWriter(csvfile, fieldnames=hash_row.keys())
    writer.writeheader()
    for _ in progressbar(range(PASSWORD_AMOUNT)):
        hash_row['salt'] = uuid.uuid4().hex
        pswd_salt = bytes(next(pswd_gen) + hash_row['salt'], encoding='ascii')
        hash_row['hash'] = b64encode(hashlib.sha1(pswd_salt).digest()).decode()
        writer.writerow(hash_row)

logger.info('Generating bcrypt password hashes and saving into {}'.format(BCRYPT_PATH))
with open(BCRYPT_PATH, 'w') as csvfile:
    hash_row = {'hash': None}
    writer = csv.DictWriter(csvfile, fieldnames=hash_row.keys())
    writer.writeheader()
    for _ in progressbar(range(PASSWORD_AMOUNT)):
        salt = bcrypt.gensalt(rounds=7)
        pswd_salt = bytes(next(pswd_gen), encoding='ascii')
        hash_row['hash'] = bcrypt.hashpw(pswd_salt, salt).decode()
        writer.writerow(hash_row)

logger.success('Done!')