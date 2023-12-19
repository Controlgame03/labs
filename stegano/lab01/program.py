def encryption(text, secret):
    bin_str = ''
    for i in range(len(secret)):
        tmp = str(bin(ord(secret[i])))[2:]
        nulls = ''
        for _ in range(7 - len(tmp)):
            nulls += '0'
        bin_str += nulls + tmp
    text_tmp = [a for a in text]
    signs = ['.', '!', '?']
    end = len(text_tmp)
    i = 0

    count = 0

    for a in text_tmp:
        if a == '.':
            count += 1

    while i != end:
        if text_tmp[i] in signs and text_tmp[i + 1] not in signs:
            if text_tmp[i + 1] != ' ':
                text_tmp.insert(i + 1, ' ')
                end += 1
                i += 1
            else:
                if text_tmp[i + 2] == ' ':
                    while text_tmp[i + 2] == ' ':
                        text_tmp.pop(i + 2)
                        end -= 1
                    continue
        i += 1
    i = 0
    end = len(text_tmp)
    sec_idx = 0
    while i != end:
        if text_tmp[i] in signs and text_tmp[i + 1] not in signs:
            if sec_idx >= len(bin_str):
                break
            if int(bin_str[sec_idx]):
                text_tmp.insert(i + 1, ' ')
                i = i + 2
                end += 1
            sec_idx += 1
        i += 1
    print(count)
    return ''.join(text_tmp)


def decryption(enc_text):
    dec_mes = ''
    signs = ['.', '!', '?']
    tmp_list = ''
    for i in range(len(enc_text)):
        if enc_text[i] in signs:
            if enc_text[i + 2] == ' ':
                tmp_list += '1'
            else:
                tmp_list += '0'
            if len(tmp_list) == 7:
                if tmp_list == '0000000':
                    return dec_mes
                dec_mes += chr(int('0b' + tmp_list, 2))
                tmp_list = ''
    return dec_mes


with open("text.txt", mode='r') as read_file:
    text = read_file.read()
with open("secret.txt", mode='r') as secret_file:
    secret = secret_file.read()

result = encryption(text, secret)

with open("encryption.txt", mode='w') as result_file:
    result_file.write(result)

with open("decryption.txt", mode='w') as dec_file:
    dec_file.write(decryption(result))
