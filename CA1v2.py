import string
import collections
import os


class CaesarCipherAnalyzer:
    def __init__(self):
        self.width = 60
########################################################################################################################################################

    def intro(self):
        print('*' * self.width)
        text = ' ST1507 DSAA: Welcome to:'
        print(f"*{text}{' ' * (self.width-len(text)-2)}*")
        print(f"*{' ' * (self.width-2)}*")
        text = '~ Caeser Cipher Encrypted Message Analyzer ~'
        print(f"*{' ' * round((self.width-len(text)-2)/2)}{text}{' ' * (self.width - (round((self.width-len(text)-2)/2)+len(text))-2)}*")
        print(f"*{'-' * (self.width-2)}*")
        text = '    - Done by: Zachary Leong(2201861)'
        print(f"*{text}{' ' * (self.width-len(text)-2)}*")
        print(f"*{' ' * (self.width-2)}*")
        text = '    - Class DAAA/2B/01'
        print(f"*{text}{' ' * (self.width-len(text)-2)}*")
        print('*' * self.width)

        input("Press enter key, to continue....")
        self.menu()
########################################################################################################################################################

    def menu(self):
        print('Please select your choice: (1,2,3,4,5,6,7,8)\n\t1. Encrypt/Decrypt Message\n\t2. Encrypt/Decrypt File\n\t3. Analyze letter frequency distribution\n\t4. Infer caesar cipher key from file\n\t5. Analyze, and sort encrypted files\n\t6. Extra Option One\n\t7. Extra Option Two\n\t8. Exit')
        select = int(input('Enter choice: '))

        if select == 1:
            self.encrypt_decrypt_message()
        elif select == 2:
            self.encrypt_decrypt_file()
        elif select == 3:
            self.letter_frequency()
        elif select == 4:
            self.infer_key()
        elif select == 5:
            self.sort_file()
        elif select == 6:
            self.option1()
        elif select == 7:
            self.option2()
        elif select == 8:
            print(
                'Bye, thanks for using ST1507 DSAA: Caesar Cipher Encrypted Message Analyzer')
        else:
            self.menu()
########################################################################################################################################################
# global.)
    def readfile(self, input_message):
        input_file_name = input(input_message)
        with open(input_file_name, 'r') as input_file:
            return input_file.read()

    def shift_char(self, char, key):
        alphabet = string.ascii_uppercase
        if char.isalpha():
            is_upper = char.isupper()
            char = char.upper()
            if char in alphabet:
                index = (alphabet.index(char) + key) % 26
                encrypted_char = alphabet[index]
                return encrypted_char if is_upper else encrypted_char.lower()
        return char

    def encrypt_key(self, text, key):
        return ''.join(self.shift_char(char, key) for char in text)

    def decrypt_key(self, cipher, key):
        return ''.join(self.shift_char(char, -key) for char in cipher)

    def calculate_letter_frequencies(self, text):
        text = text.lower()
        total_letters = sum(text.count(letter) for letter in string.ascii_lowercase)
        letter_frequencies = {letter: text.count(letter) / total_letters for letter in string.ascii_lowercase}
        return letter_frequencies

    def find_best_shift(self, input_freq_dict, master_freq_dict):
        best_shift = 0
        min_difference = float('inf')

        for shift in range(26):
            shifted_dict = {}
            for letter, freq in input_freq_dict.items():
                shifted_letter = chr(((ord(letter) - ord('a') + shift) % 26) + ord('a'))
                shifted_dict[shifted_letter] = shifted_dict.get(shifted_letter, 0) + freq

            difference = sum(abs(master_freq_dict[letter] - shifted_dict.get(letter, 0)) for letter in string.ascii_lowercase)
            if difference < min_difference:
                min_difference = difference
                best_shift = shift

        return best_shift

    def caesar_cipher_shift(self, encrypted_text, master_freq_dict):
        letter_frequencies = self.calculate_letter_frequencies(encrypted_text)
        best_shift = self.find_best_shift(letter_frequencies, master_freq_dict)
        return best_shift


    def input_freq_dict(self, string):
        input_freq_dict = {}
        lines = string.split('\n')
        for line in lines:
            if line:
                key, value = line.split(',')
                key = key.strip()
                value = float(value)
                input_freq_dict[key] = value
        return input_freq_dict

        
    def shift_letter(self, letter, shift):
        if letter.isalpha():
            shifted_code = ord(letter) - shift
            if shifted_code < ord('a'):
                shifted_code += 26
            return chr(shifted_code)
        else:
            return letter

    def input_freq_dict(self, string):
        input_freq_dict = {}
        lines = string.split('\n')
        for line in lines:
            if line:
                key, value = line.split(',')
                key = key.strip()
                value = float(value)
                input_freq_dict[key] = value
        return input_freq_dict

    def master_freq_dict(self, string):
        master_freq_dict = {}
        lines = string.split('\n')
        for line in lines:
            if line:
                key, value = line.split(',')
                key = key.strip().lower()
                value = float(value)
                master_freq_dict[key] = value
        return master_freq_dict

    def calculate_chi_squared(self, text_freq, master_freq):
        chi_squared = 0
        for letter in string.ascii_lowercase:
            observed = text_freq.get(letter, 0)
            expected = master_freq[letter]
            chi_squared += ((observed - expected) ** 2) / expected
        return chi_squared

    def best_caesar_shift(self, encrypted_text, master_freq):
        best_shift = None
        best_chi_squared = float('inf')

        for shift in range(26):
            shifted_text = ''.join([self.shift_letter(letter, shift) for letter in encrypted_text.lower()])
            text_freq = {letter: shifted_text.count(letter) / len(shifted_text) for letter in string.ascii_lowercase}
            chi_squared = self.calculate_chi_squared(text_freq, master_freq)
            
            if chi_squared < best_chi_squared:
                best_chi_squared = chi_squared
                best_shift = shift

        return best_shift
########################################################################################################################################################
# 1.)

    def encrypt_decrypt_message(self):
        option = input("Enter 'E' for Encrypt or 'D' for Decrypt: ").upper()
        if option == 'E':
            text = str(input('\nPlease type text you want to encrypt:\n'))
            key = int(input('\nEnter the cipher key: '))
            print(f"\nPlaintext:      {text}")
            print(f"Ciphertext:     {self.encrypt_key(text, key)}\n")
            input("Press enter key, to continue....")
            self.menu()
        elif option == 'D':
            cipher = str(input('\nPlease type text you want to decrypt:\n'))
            key = int(input('\nEnter the cipher key: '))
            print(f"\nCiphertext:     {cipher}")
            print(f"Plaintext:      {self.decrypt_key(cipher, key)}\n")
            input("Press enter key, to continue....")
            self.menu()
        elif option == '':
            self.menu()
        else:
            print('Try again')
            self.encrypt_decrypt_message()
########################################################################################################################################################
# 2.)

    def encrypt_decrypt_file(self):
        option = input("Enter 'E' for Encrypt or 'D' for Decrypt: ").upper()
        if option == 'E':
            input_file = input("Please enter the file you want to encrypt: ")
        elif option == 'D':
            input_file = input("Please enter the file you want to decrypt: ")
        elif option == '':
            self.menu()
        else:
            print('Try again')
            self.encrypt_decrypt_file()

        key = int(input('Enter the cipher key: '))

        output_file = input("\nPlease enter a output file: ")

        with open(input_file, 'r') as input_file, open(output_file, 'w') as output:
            for line in input_file:
                if option == 'E':
                    encrypted_line = self.encrypt_key(line.strip(), key)
                else:
                    encrypted_line = self.decrypt_key(line.strip(), key)
                output.write(encrypted_line + '\n')

        print(f"\nOperation completed. File save as '{output_file}'")
        input("Press enter key to continue....")
        self.menu()
########################################################################################################################################################
# 3.)
    def display_gui(self, array):
        for row in array:
            row_string = ''
            for cell in row:
                row_string += cell
            print(f"{row_string}")

    def letter_frequency(self):
        text = self.readfile('Please enter the file to analyze: ')
        rows = 28
        cols = 56
        array = [[' ' for _ in range(cols)] for _ in range(rows)]
        # A-Z
        for i in range(65, 91):
            array[rows-1][((i-64)*2)-1] = chr(i)
        # _
        for i in range(0, 53):
            array[rows-2][i] = '_'
        # ACSII for capital A to Z
        letter_counts = {chr(letter): 0 for letter in range(
            65, 91)}

        text = text.upper()
        text_len = len("".join(text.split()))
        for char in text:
            if char.isalpha():
                if char in letter_counts:
                    letter_counts[char] += 1
                else:
                    letter_counts[char] = 1

        for letter, count in letter_counts.items():
            for i in range((rows - (round((count / text_len) * 26) + 2)), (rows - 2)):
                array[i][((ord(letter) - 64) * 2) - 1] = "*"

        for i in range(0, rows-1):
            array[i][53] = '| '

        for letter, count in letter_counts.items():
            percentage = f"{((count / text_len) * 100):.2f}%"
            space = ' ' * (6-(len(f"{percentage}")))
            array[(ord(letter)-65)][54] = (f"{letter}-{space}{percentage}")

        # right legend
        array[10][55] = ' \tTOP 5 FREQ'
        array[11][55] = ' \t----------'
        sorted_letter_counts = sorted(
            letter_counts.items(), key=lambda item: item[1], reverse=True)

        top_5 = []

        for letter, count in sorted_letter_counts[:5]:
            percentage = f"{((count / text_len) * 100):.2f}%"
            top_5.append((letter, percentage))

        for i, (letter, percentage) in enumerate(top_5, 1):
            space = ' ' * (6-(len(f"{percentage}")))
            array[(i+11)][55] = (f" \t| {letter}-{space}{percentage}")

        print(top_5)

        self.display_gui(array)

        input("Press enter key to continue....")
        self.menu()
########################################################################################################################################################
# 4.)
    def infer_key(self):
        encrypted_text = self.readfile('Please enter the file to analyze: ')
        master_frequency = self.master_freq_dict(self.readfile('\nPlease enter the reference frequencies file: '))
        best_shift = self.best_caesar_shift(encrypted_text, master_frequency)

        print(f"The inferred caesar cipher shift is: {best_shift}")
        if (input('Would you like to decrypt this file using this key? y/n: ').lower() == 'y'):
            output_file = input('\nPlease enter a output file: ')
            with open(output_file, 'w') as output:
                output.write(self.decrypt_key(encrypted_text, best_shift))
                

########################################################################################################################################################
# 5.)       
    def sort_file(self):
        
        folder_path = 'test'

        master_freq_dict(readfile("master"))

        # Create a list to store information about each encrypted message
        message_info = []

        # Loop through the files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):  # Change the file extension as needed
                file_path = os.path.join(folder_path, filename)
                encrypted_text = readfile(f"Reading {filename}... ")
                
                # Find the best Caesar shift for decryption
                best_shift = best_caesar_shift(encrypted_text, master_freq)
                
                # Decrypt the message
                decrypted_message = decrypt_key(encrypted_text, best_shift)
                
                # Save the decrypted message to a file
                output_filename = f"file{len(message_info) + 1}.txt"
                with open(output_filename, 'w') as output_file:
                    output_file.write(decrypted_message)
                
                # Store information about the message for sorting
                message_info.append((filename, best_shift))

        # Sort the messages based on the best_shift
        message_info.sort(key=lambda x: x[1])

        # Print the sorted list of filenames and best shifts
        for index, (filename, best_shift) in enumerate(message_info, start=1):
            print(f"{index}. {filename}: Best Shift = {best_shift}")

        print("Decryption complete.")
########################################################################################################################################################
if __name__ == "__main__":
    caesar_cipher_analyzer = CaesarCipherAnalyzer()
    caesar_cipher_analyzer.intro()