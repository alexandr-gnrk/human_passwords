with open('generated-sha1.csv') as f1:
    with open('generated-sha1-reverse.csv', 'w') as f2:
        for line in f1:
            hash_, salt = line.split(':')
            f2.write(salt.strip() + ':' + hash_ + '\n')
