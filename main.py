import string
import collections


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

    def find_caesar_shift(self, first_char, second_char):
        first_char = first_char.upper()
        second_char = second_char.upper()
        for key in range(26):
            if self.shift_char(first_char, key) == second_char:
                return key
        return None

    def encrypt_key(self, text, key):
        return ''.join(self.shift_char(char, key) for char in text)

    def decrypt_key(self, cipher, key):
        return ''.join(self.shift_char(char, -key) for char in cipher)
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

        def display_gui(array):
            for row in array:
                row_string = ''
                for cell in row:
                    row_string += cell
                print(f"{row_string}")

        display_gui(array)

        input("Press enter key to continue....")
        self.menu()
########################################################################################################################################################
# 4.)

    def infer_key(self):
        # text = self.readfile('Please enter the file to analyze: ')
        # freq_file = self.readfile(
        #     'Please enter the reference frequencies file: ')
        text = 'The Caesar Cipher, used by Julius Caesar around 58 BC, is a substitution cipher that shifts letters in a message to make it unreadable if intercepted. To decrypt, the receiver reverses the shift. Arab mathematician Al-Kindi broke the Caesar Cipher using frequency analysis, which exploits patterns in letter frequencies.'
        text = text.upper()

        letter_counts = {chr(letter): 0 for letter in range(65, 91)}
        for char in text:
            if char.isalpha():
                if char in letter_counts:
                    letter_counts[char] += 1
                else:
                    letter_counts[char] = 1

        sorted_letter_counts = sorted(
            letter_counts.items(), key=lambda item: item[1], reverse=True)

        print(self.find_caesar_shift(sorted_letter_counts[0][0], 'E'))


########################################################################################################################################################
if __name__ == "__main__":
    caesar_cipher_analyzer = CaesarCipherAnalyzer()
    caesar_cipher_analyzer.intro()
