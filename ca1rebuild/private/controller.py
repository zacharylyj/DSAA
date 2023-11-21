from private.ciphertools import Ceaser, FrequencyAnalysis, Sha
from private.utils import FileOperator, Utility
from private.menu import Menu
import os


class Controller:
    ########################################################################################################################################################
    # 1.)
    def __init__(self):
        self.ceaser = Ceaser()
        self.freqanalysis = FrequencyAnalysis()
        self.file = FileOperator()
        self.utils = Utility('pang')
        self.menu = Menu()
        self.sha = Sha()

    def encrypt_decrypt_message(self):
        option = input("Enter 'E' for Encrypt or 'D' for Decrypt: ").upper()
        if option == "E":
            text = str(input("\nPlease type text you want to encrypt:\n"))
            key = int(input("\nEnter the cipher key: "))
            print(f"\nPlaintext:      {text}")
            print(f"Ciphertext:     {self.ceaser.encrypt_key(text, key)}\n")
            self.menu.select_option()
        elif option == "D":
            cipher = str(input("\nPlease type text you want to decrypt:\n"))
            key = int(input("\nEnter the cipher key: "))
            print(f"\nCiphertext:     {cipher}")
            print(f"Plaintext:      {self.ceaser.decrypt_key(cipher, key)}\n")
            self.menu.select_option()
        elif option == "Q":
            self.menu.select_option()
        else:
            print("Try again")
            self.encrypt_decrypt_message()

    ########################################################################################################################################################
    # 2.)

    def encrypt_decrypt_file(self):
        option = input("Enter 'E' for Encrypt or 'D' for Decrypt: ").upper()
        if option == "E":
            input_file = input("Please enter the file you want to encrypt: ")
        elif option == "D":
            input_file = input("Please enter the file you want to decrypt: ")
        elif option == "Q":
            self.menu.select_option()
        else:
            print("Try again")
            self.encrypt_decrypt_file()

        key = int(input("Enter the cipher key: "))

        output_file = input("\nPlease enter a output file: ")
        with open(input_file, "r") as input_file, open(output_file, "w") as output:
            for line in input_file:
                if option == "E":
                    encrypted_line = self.ceaser.encrypt_key(line, key)
                elif option == "D":
                    encrypted_line = self.ceaser.decrypt_key(line, key)
                else:
                    print("Try Again")
                output.write(encrypted_line + "\n")

        print(f"\nOperation completed. File save as '{output_file}'")
        self.menu.select_option()

    ########################################################################################################################################################
    # 3.)

    def letter_frequency(self):
        text = self.file.readfile(input("Please enter the file to analyze: "))
        rows = 28
        cols = 56
        array = [[" " for _ in range(cols)] for _ in range(rows)]
        # A-Z
        for i in range(65, 91):
            array[rows - 1][((i - 64) * 2) - 1] = chr(i)
        # _
        for i in range(0, 53):
            array[rows - 2][i] = "_"
        # ACSII for capital A to Z
        letter_counts = {chr(letter): 0 for letter in range(65, 91)}

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

        for i in range(0, rows - 1):
            array[i][53] = "| "

        for letter, count in letter_counts.items():
            percentage = f"{((count / text_len) * 100):.2f}%"
            space = " " * (6 - (len(f"{percentage}")))
            array[(ord(letter) - 65)][54] = f"{letter}-{space}{percentage}"

        # right legend
        array[10][55] = " \tTOP 5 FREQ"
        array[11][55] = " \t----------"
        sorted_letter_counts = sorted(
            letter_counts.items(), key=lambda item: item[1], reverse=True
        )

        top_5 = []

        for letter, count in sorted_letter_counts[:5]:
            percentage = f"{((count / text_len) * 100):.2f}%"
            top_5.append((letter, percentage))

        for i, (letter, percentage) in enumerate(top_5, 1):
            space = " " * (6 - (len(f"{percentage}")))
            array[(i + 11)][55] = f" \t| {letter}-{space}{percentage}"

        self.utils.display_gui(array)
        self.menu.select_option()

    ########################################################################################################################################################
    # 4.)

    def infer_key(self):
        encrypted_text = self.file.readfile(input("Please enter the file to analyze: "))
        master_frequency = self.utils.master_freq_dict(
            self.file.readfile(input("\nPlease enter the reference frequencies file: "))
        )
        best_shift = self.freqanalysis.best_caesar_shift(
            encrypted_text, master_frequency
        )

        print(f"The inferred caesar cipher shift is: {best_shift}")
        if (
            input("Would you like to decrypt this file using this key? y/n: ").lower()
            == "y"
        ):
            output_file = input("\nPlease enter a output file: ")
            self.file.writefile(
                self.ceaser.decrypt_key(encrypted_text, best_shift), output_file
            )
        self.menu.select_option()

    ########################################################################################################################################################
    # 5.)

    def sort_file(self):
        printstr = ""
        folder_name = input("Please enter the folder name: ")
        # Replace with your master frequency dictionary
        master_freq_dict = self.utils.master_freq_dict(
            self.file.readfile(input("Please enter the frequency file: "))
        )
        # Get a list of files in the specified folder
        files = [
            file
            for file in os.listdir(folder_name)
            if os.path.isfile(os.path.join(folder_name, file))
        ]

        # Create a list to store file names and their corresponding Caesar shift values
        file_shift_pairs = []

        # Process each file in the folder
        for file_name in files:
            # Read the contents of the file
            file_path = os.path.join(folder_name, file_name)
            with open(file_path, "r") as file:
                encrypted_text = file.read()

            # Find the best Caesar shift for the file
            best_shift = self.freqanalysis.best_caesar_shift(
                encrypted_text, master_freq_dict
            )

            # Decrypt the file using the best shift
            decrypted_text = self.ceaser.decrypt_key(encrypted_text, best_shift)

            # Append the file name and shift value to the list
            file_shift_pairs.append((file_name, best_shift, decrypted_text))

        # Sort the list based on the Caesar shift values
        file_shift_pairs.sort(key=lambda x: x[1])

        # Create and write the arranged files
        for i, (file_name, best_shift, decrypted_text) in enumerate(file_shift_pairs):
            # Generate the new file name as per your specified format
            output_file = os.path.join(f"{folder_name}", f"file{i + 1}.txt")

            self.file.writefile(decrypted_text, output_file)

            printstr += (
                f"Decrypting: {file_name} with key: {best_shift} as: {output_file}\n"
            )
        print(printstr)
        log_file = os.path.join(f"{folder_name}", "log.txt")
        self.file.writefile(printstr, log_file)
        print(f"Files are stored in <{folder_name}> folder")
        self.menu.select_option()

    def option1(self):
        option = input("Enter 'E' for Encrypt or 'C' to Check if Private Key is verified: ").upper()
        if option == "E":
            public_key = self.sha.hash(input("Enter and Remember the Private Key(password): "))
            print(f"Your Public Key is: {public_key}")
            self.file.writefile(public_key, "Public_Key.txt")
            print(f"Saved in <Public_Key.txt>")
        elif option == "C":
            if self.sha.check(input("Enter the Private Key: "), input("Enter the Public Key: ")):
                print("Private Key is Verified ✔")
            else:
                print("Private Key is does not match ✘")
        elif option == "Q":
            self.menu.select_option()
        else:
            print("Try again")
        self.menu.select_option()

    def option2(self):
        self.utils.pwcheck()
        print("suck")
        self.menu.select_option()