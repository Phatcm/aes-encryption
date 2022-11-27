from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

import os
import os.path
from os import listdir
from os.path import isfile, join
import time
from sys import exit

class Encryptor:
    def __init__(self, key):
        self.key = key
        
    def encrypt(self, key, original_data):
        cipher = AES.new(key, AES.MODE_CBC)
        ciphered_data = cipher.encrypt(pad(original_data, AES.block_size))
        return cipher.iv + ciphered_data
    
    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as f:
            original = f.read()
        encrypted = self.encrypt(self.key, original)
        with open(file_name + ".enc", 'wb') as f:
            f.write(encrypted)
        os.remove(file_name)
        
    def decrypt(self, key, ciphered_data, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size)
        return original_data
    
    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as f:
            iv = f.read(16)
            ciphered = f.read()
        decrypted = self.decrypt(self.key, ciphered, iv)
        with open(file_name[:-4], 'wb') as f:
            f.write(decrypted)
        os.remove(file_name)
    
    def get_all_files(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subDirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if(fname != 'encrypt.py' and fname !='data.txt.enc'):
                    dirs.append(dirName+"\\"+fname)
        return dirs
    
    def encrypt_all_file(self):
        dirs = self.get_all_files()
        for file_name in dirs:
            self.encrypt_file(file_name)
            
    def decrypt_all_file(self):
        dirs = self.get_all_files()
        for file_name in dirs:
            self.decrypt_file(file_name)
   
salt = b'\xa4\xb0\x80H\xae\xaa\xf8\xcbK\x10\x8ej\xcdA\xc3\xf0\xebqtr\x92\x87\x12x/I\xddQ,J\xd3\x16'
password = input('Enter a password that will be used for encryption or decryption: ')
key = PBKDF2(password, salt, dkLen=32)

enc = Encryptor(key)
clear = lambda:os.system('cls')


if os.path.isfile('data.txt.enc'):
    while True:
        enc.decrypt_file("data.txt.enc")
        p = ''
        with open("data.txt", "r") as f:
            p = f.readlines()
        if p[0] == password:
            enc.encrypt_file("data.txt")
            break

    while True:
        choice = int(input(
            "1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to Encrypt all files in the directory.\n4. Press '4' to decrypt all files in the directory.\n5. Press '5' to exit.\n"))
        if choice == 1:
            enc.encrypt_file(str(input("Enter name of file to encrypt: ")))
        elif choice == 2:
            enc.decrypt_file(str(input("Enter name of file to decrypt: ")))
        elif choice == 3:
            enc.encrypt_all_files()
        elif choice == 4:
            enc.decrypt_all_files()
        elif choice == 5:
            exit()
        else:
            print("Please select a valid option!")

else:
    while True:
        repassword = str(input("Confirm password: "))
        if password == repassword:
            break
        else:
            print("Passwords Mismatched!")
    f = open("data.txt", "w+")
    f.write(password)
    f.close()
    enc.encrypt_file("data.txt")
    print("Please restart the program to complete the setup")
    time.sleep(5) 
        
        
        