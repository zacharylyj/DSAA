import string


class Private:
    def writefile(self, content, output_file_name):
        with open(output_file_name, "w") as output_file:
            output_file.write(content)

    def readfile(self, input_file_name):
        with open(input_file_name, "r") as input_file:
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

    def encrypt_key(self, string, key):
        return "".join(self.shift_char(char, key) for char in string)

    def decrypt_key(self, string, key):
        return "".join(self.shift_char(char, -key) for char in string)

    def calculate_letter_frequencies(self, text):
        text = text.lower()
        total_letters = sum(text.count(letter) for letter in string.ascii_lowercase)
        letter_frequencies = {
            letter: text.count(letter) / total_letters
            for letter in string.ascii_lowercase
        }
        return letter_frequencies

    def find_best_shift(self, input_freq_dict, master_freq_dict):
        best_shift = 0
        min_difference = float("inf")

        for shift in range(26):
            shifted_dict = {}
            for letter, freq in input_freq_dict.items():
                shifted_letter = chr(((ord(letter) - ord("a") + shift) % 26) + ord("a"))
                shifted_dict[shifted_letter] = (
                    shifted_dict.get(shifted_letter, 0) + freq
                )

            difference = sum(
                abs(master_freq_dict[letter] - shifted_dict.get(letter, 0))
                for letter in string.ascii_lowercase
            )
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
        lines = string.split("\n")
        for line in lines:
            if line:
                key, value = line.split(",")
                key = key.strip()
                value = float(value)
                input_freq_dict[key] = value
        return input_freq_dict

    def shift_letter(self, letter, shift):
        if letter.isalpha():
            shifted_code = ord(letter) - shift
            if shifted_code < ord("a"):
                shifted_code += 26
            return chr(shifted_code)
        else:
            return letter

    def input_freq_dict(self, string):
        input_freq_dict = {}
        lines = string.split("\n")
        for line in lines:
            if line:
                key, value = line.split(",")
                key = key.strip()
                value = float(value)
                input_freq_dict[key] = value
        return input_freq_dict

    def master_freq_dict(self, string):
        master_freq_dict = {}
        lines = string.split("\n")
        for line in lines:
            if line:
                key, value = line.split(",")
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
        best_chi_squared = float("inf")

        for shift in range(26):
            shifted_text = "".join(
                [self.shift_letter(letter, shift) for letter in encrypted_text.lower()]
            )
            text_freq = self.calculate_letter_frequencies(shifted_text)
            chi_squared = self.calculate_chi_squared(text_freq, master_freq)

            if chi_squared < best_chi_squared:
                best_chi_squared = chi_squared
                best_shift = shift

        return best_shift

    def display_gui(self, array):
        for row in array:
            row_string = ""
            for cell in row:
                row_string += cell
            print(f"{row_string}")
