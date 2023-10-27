from utils.private_class import Private
from utils.menu import Menu
import os


class Controller:
    ########################################################################################################################################################
    # 1.)
    def __init__(self):
        self.privateclass = Private()
        self.menu = Menu()

    def encrypt_decrypt_message(self):
        option = input("Enter 'E' for Encrypt or 'D' for Decrypt: ").upper()
        if option == "E":
            text = str(input("\nPlease type text you want to encrypt:\n"))
            key = int(input("\nEnter the cipher key: "))
            print(f"\nPlaintext:      {text}")
            print(f"Ciphertext:     {self.privateclass.encrypt_key(text, key)}\n")
            self.menu.select_option()
        elif option == "D":
            cipher = str(input("\nPlease type text you want to decrypt:\n"))
            key = int(input("\nEnter the cipher key: "))
            print(f"\nCiphertext:     {cipher}")
            print(f"Plaintext:      {self.privateclass.decrypt_key(cipher, key)}\n")
            self.menu.select_option()
        elif option == "Q":
            self.menu.select_option()
        else:
            print("Try again")
            self.privateclass.encrypt_decrypt_message()

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
            self.privateclass.encrypt_decrypt_file()

        key = int(input("Enter the cipher key: "))

        output_file = input("\nPlease enter a output file: ")
        with open(input_file, "r") as input_file, open(output_file, "w") as output:
            for line in input_file:
                if option == "E":
                    encrypted_line = self.privateclass.encrypt_key(line, key)
                else:
                    encrypted_line = self.privateclass.decrypt_key(line, key)
                output.write(encrypted_line + "\n")

        print(f"\nOperation completed. File save as '{output_file}'")
        self.menu.select_option()

    ########################################################################################################################################################
    # 3.)

    def letter_frequency(self):
        text = self.privateclass.readfile(input("Please enter the file to analyze: "))
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

        print(top_5)

        self.privateclass.display_gui(array)

        self.menu.select_option()

    ########################################################################################################################################################
    # 4.)

    def infer_key(self):
        encrypted_text = self.privateclass.readfile(
            input("Please enter the file to analyze: ")
        )
        master_frequency = self.privateclass.master_freq_dict(
            self.privateclass.readfile(
                input("\nPlease enter the reference frequencies file: ")
            )
        )
        best_shift = self.privateclass.best_caesar_shift(
            encrypted_text, master_frequency
        )

        print(f"The inferred caesar cipher shift is: {best_shift}")
        if (
            input("Would you like to decrypt this file using this key? y/n: ").lower()
            == "y"
        ):
            output_file = input("\nPlease enter a output file: ")
            self.privateclass.writefile(
                self.privateclass.decrypt_key(encrypted_text, best_shift), output_file
            )
        self.menu.select_option()

    ########################################################################################################################################################
    # 5.)

    def sort_file(self):
        folder_name = input("Please enter the folder name: ")
        # Replace with your master frequency dictionary
        master_freq_dict = self.privateclass.master_freq_dict(
            self.privateclass.readfile(input("fict "))
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
            best_shift = self.privateclass.best_caesar_shift(
                encrypted_text, master_freq_dict
            )

            # Decrypt the file using the best shift
            decrypted_text = self.privateclass.decrypt_key(encrypted_text, best_shift)

            # Append the file name and shift value to the list
            file_shift_pairs.append((file_name, best_shift, decrypted_text))

        # Sort the list based on the Caesar shift values
        file_shift_pairs.sort(key=lambda x: x[1])

        # Create and write the arranged files
        for i, (file_name, best_shift, decrypted_text) in enumerate(file_shift_pairs):
            # Generate the new file name as per your specified format
            output_file = os.path.join("decrypted", f"file{i + 1}.txt")

            self.privateclass.writefile(decrypted_text, output_file)

            print(f"Decrypting: {file_name} with key: {best_shift} as: {output_file}")
        print("Files are stored in <decrypted> folder")
        self.menu.select_option()

    def option1(self):
        self.menu.select_option()

    def option2(self):
        self.menu.select_option()