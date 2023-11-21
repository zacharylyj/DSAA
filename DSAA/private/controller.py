from private.ciphertools import Ceaser, FrequencyAnalysis, Sha
from private.utils import FileOperator, Utility, FileSortNode, FrequencyNode
from private.menu import Menu
import os
import math


class Controller:
    ########################################################################################################################################################
    # 1.)
    def __init__(self):
        self.ceaser = Ceaser()
        self.freqanalysis = FrequencyAnalysis()
        self.file = FileOperator()
        self.utils = Utility("password")
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
                output.write(encrypted_line)

        print(f"\nOperation completed. File save as '{output_file}'")
        self.menu.select_option()

    ########################################################################################################################################################
    # 3.)

    def letter_frequency(self):
        text = self.file.readfile(input("Please enter the file to analyze: "))
        rows = 28
        cols = 56
        array = [[" " for _ in range(cols)] for _ in range(rows)]

        # convert asciic
        for i in range(65, 91):
            array[rows - 1][((i - 64) * 2) - 1] = chr(i)
        for i in range(0, 53):
            array[rows - 2][i] = "_"

        # freq count
        letter_counts = {chr(letter): 0 for letter in range(65, 91)}
        text = text.upper()
        text_len = len("".join(text.split()))
        for char in text:
            if char.isalpha():
                letter_counts[char] += 1

        # init and populate ll
        head = None
        last_node = None
        for letter, count in letter_counts.items():
            new_node = FrequencyNode(letter, count)
            if not head:
                head = new_node
                last_node = head
            else:
                last_node.nextNode = new_node
                last_node = last_node.nextNode

        # Sort ll
        sorted_head = self.utils.sort_linked_list(head)

        # Reverse ll
        reversed_head = self.utils.reverse_linked_list(sorted_head)

        current = reversed_head
        while current:
            letter = current.letter
            count = current.frequency
            percentage = ((count / text_len) * 100) if text_len > 0 else 0
            perc_str = f"{percentage:.2f}%"
            space = " " * (6 - len(perc_str))

            # Fill in the freq 2d array
            for i in range((rows - (math.ceil(percentage * 0.26) + 2)), (rows - 2)):
                array[i][((ord(letter) - 64) * 2) - 1] = "*"
            array[(ord(letter) - 65)][54] = f"{letter}-{space}{perc_str}"

            current = current.nextNode

        # Right legend for top 5 freq
        array[10][55] = " \tTOP 5 FREQ"
        array[11][55] = " \t----------"
        current = reversed_head
        for i in range(5):
            if current:
                letter = current.letter
                count = current.frequency
                percentage = ((count / text_len) * 100) if text_len > 0 else 0
                perc_str = f"{percentage:.2f}%"
                space = " " * (6 - len(perc_str))
                array[(i + 12)][55] = f" \t| {letter}-{space}{perc_str}"
                current = current.nextNode

        # Wall
        for i in range(0, rows - 1):
            array[i][53] = "| "

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
        master_freq_dict = self.utils.master_freq_dict(
            self.file.readfile(input("Please enter the frequency file: "))
        )
        files = [
            file
            for file in os.listdir(folder_name)
            if os.path.isfile(os.path.join(folder_name, file))
        ]

        # Create the head of the linked list
        head = None
        last_node = None

        for file_name in files:
            file_path = os.path.join(folder_name, file_name)
            with open(file_path, "r") as file:
                encrypted_text = file.read()

            best_shift = self.freqanalysis.best_caesar_shift(
                encrypted_text, master_freq_dict
            )
            decrypted_text = self.ceaser.decrypt_key(encrypted_text, best_shift)

            # linked list intilise
            if not head:
                head = FileSortNode(file_name, best_shift, decrypted_text)
                last_node = head
            else:
                last_node.nextNode = FileSortNode(file_name, best_shift, decrypted_text)
                last_node = last_node.nextNode

        # Sort ll
        sorted_head = self.utils.sort_linked_list(head)

        # loop to get content
        current = sorted_head
        index = 0
        while current:
            output_file = os.path.join(folder_name, f"file{index + 1}.txt")
            self.file.writefile(current.decrypted_text, output_file)
            printstr += f"Decrypting: {current.file_name} with key: {current.best_shift} as: {output_file}\n"

            current = current.nextNode
            index += 1

        log_file = os.path.join(folder_name, "log.txt")
        self.file.writefile(printstr, log_file)
        print(f"Files are stored in <{folder_name}> folder")
        print(printstr)
        self.menu.select_option()

    def option1(self):
        option = input(
            "Enter 'E' for Encrypt or 'C' to Check if Private Key is verified: "
        ).upper()
        if option == "E":
            public_key = self.sha.hash(
                input("Enter and Remember the Private Key(password): ")
            )
            print(f"Your Public Key is: {public_key}")
            self.file.writefile(public_key, "Public_Key.txt")
            print("Saved in <Public_Key.txt>")
        elif option == "C":
            if self.sha.check(
                input("Enter the Private Key: "), input("Enter the Public Key: ")
            ):
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
