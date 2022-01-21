from tkinter import filedialog
import os

class File_Model:
    def __init__(self):
        self.url = ""
        self.key = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.offset = 5

    def encrypt(self, plaintext):
        result = ''
        for l in plaintext:
            try:
                i = (self.key.index(l) + self.offset) % 62
                result += self.key[i]
            except ValueError:
                result += l
        return result

    def decrypt(self, ciphertext):
        result = ''
        for l in ciphertext:
            try:
                i = (self.key.index(l) - self.offset) % 62
                result += self.key[i]
            except ValueError:
                result += l
        return result

    def open_file(self):
        self.url = filedialog.askopenfilename(title='Select File',filetypes=[("Text Documents", "*.*")])

    def new_file(self):
        self.url = ""

    def save_as(self, msg):
        content = msg
        encrypted = self.encrypt(content)
        self.url = filedialog.asksaveasfile(mode='w', defaultextension='.ntxt',filetypes=([("All Files", "*.*"), ("Text Documents", "*.txt")]))
        self.url.write(encrypted)
        filepath = self.url.name
        self.url.close()
        self.url = filepath

    def save_file(self, msg):
        if self.url == "":
            self.url = filedialog.asksaveasfilename(title='Select File', defaultextension='.ntxt',filetypes=[("Text Documents", "*.*")])
        filename, file_extension = os.path.splitext(self.url)
        content = msg
        if file_extension in '.ntxt':
            content = self.encrypt(content)
        with open(self.url, 'w', encoding='utf-8') as fw:
            fw.write(content)

    def read_file(self, url=''):
        if url != '':
            self.url = url
        else:
            self.open_file()
        base = os.path.basename(self.url)

        file_name, file_extension = os.path.splitext(self.url)
        fr = open(self.url, "r")
        contents = fr.read()
        if file_extension == '.ntxt':
            contents = self.decrypt(contents)
        fr.close()
        return contents, base


