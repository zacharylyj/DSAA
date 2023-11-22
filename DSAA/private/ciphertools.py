import string
import requests


class Ceaser:
    def __init__(self):
        self.frequency_analysis = FrequencyAnalysis()

    def encrypt_key(self, string, key):
        return "".join(self.shift_char(char, key) for char in string)

    def decrypt_key(self, string, key):
        return "".join(self.shift_char(char, -key) for char in string)

    def caesar_cipher_shift(self, encrypted_text, master_freq_dict):
        letter_frequencies = self.frequency_analysis.calculate_letter_frequencies(
            encrypted_text
        )
        best_shift = self.frequency_analysis.find_best_shift(
            letter_frequencies, master_freq_dict
        )
        return best_shift

    # for all string, predefined
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


# https://en.wikipedia.org/wiki/SHA-1
class Sha:
    def _left_rotate(self, n, b):
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    def hash(self, pkey):
        # init the set values of h0-h4 used by previous dev
        h0 = 0x67452301
        h1 = 0xEFCDAB89
        h2 = 0x98BADCFE
        h3 = 0x10325476
        h4 = 0xC3D2E1F0
        pkey = pkey.strip()
        pkey = bytearray(pkey, "utf-8")
        original_length_in_bits = (8 * len(pkey)) & 0xFFFFFFFFFFFFFFFF
        pkey.append(0x80)

        while len(pkey) % 64 != 56:
            pkey.append(0)

        pkey += original_length_in_bits.to_bytes(8, byteorder="big")

        for chunk_start in range(0, len(pkey), 64):
            chunk = pkey[chunk_start : chunk_start + 64]
            w = [0] * 80
            for i in range(16):
                w[i] = int.from_bytes(chunk[i * 4 : i * 4 + 4], byteorder="big")
            for i in range(16, 80):
                w[i] = self._left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

            a = h0
            b = h1
            c = h2
            d = h3
            e = h4

            for i in range(80):
                if 0 <= i <= 19:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= i <= 39:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= i <= 59:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                elif 60 <= i <= 79:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6

                temp = self._left_rotate(a, 5) + f + e + k + w[i] & 0xFFFFFFFF
                e = d
                d = c
                c = self._left_rotate(b, 30)
                b = a
                a = temp

            h0 = (h0 + a) & 0xFFFFFFFF
            h1 = (h1 + b) & 0xFFFFFFFF
            h2 = (h2 + c) & 0xFFFFFFFF
            h3 = (h3 + d) & 0xFFFFFFFF
            h4 = (h4 + e) & 0xFFFFFFFF
        # conver to hex
        return "%08x%08x%08x%08x%08x" % (h0, h1, h2, h3, h4)

    def check(self, private, public):
        return self.hash(private) == public


class FrequencyAnalysis:
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

    def calculate_chi_squared(self, text_freq, master_freq):
        chi_squared = 0
        for letter in string.ascii_lowercase:
            observed = text_freq.get(letter, 0)
            expected = master_freq[letter]
            chi_squared += ((observed - expected) ** 2) / expected
        return chi_squared

    # for lower case no predefined
    def shift_letter(self, letter, shift):
        if letter.isalpha():
            shifted_code = ord(letter) - shift
            if shifted_code < ord("a"):
                shifted_code += 26
            return chr(shifted_code)
        else:
            return letter

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


from private.utils import BookNode


class BookCipher:
    def __init__(self, book_url):
        self.book_url = book_url
        self.book_content = self._download_book()
        self.word_map = self._create_word_map()
        self.unrecognized_words = None
        self.unique_id_counter = 1

    def _download_book(self):
        response = requests.get(self.book_url)
        return response.text

    def _create_word_map(self):
        word_map = {}
        words = self.book_content.split()
        for index, word in enumerate(words):
            if word in word_map:
                word_map[word].append(index)
            else:
                word_map[word] = [index]
        return word_map

    def _add_unrecognized_word(self, word):
        new_node = BookNode(word, self.unique_id_counter)
        self.unique_id_counter += 1

        if not self.unrecognized_words:
            self.unrecognized_words = new_node
        else:
            # Add to the start for simplicity, but you can modify this as needed
            new_node.nextNode = self.unrecognized_words
            self.unrecognized_words = new_node

        return new_node.unique_id

    def encrypt(self, message):
        encrypted_message = []
        for word in message.split():
            word_positions = self.word_map.get(word, [])
            if word_positions:
                encrypted_message.append(
                    str(word_positions[0])
                )  # Or use any other position logic
            else:
                # Add word to the linked list and use its unique ID for encryption
                unique_id = self._add_unrecognized_word(word)
                encrypted_message.append(
                    f"#{unique_id}"
                )  # Prefix with # to indicate unique ID
        return " ".join(encrypted_message)

    def decrypt(self, encrypted_message):
        decrypted_message = []
        words = self.book_content.split()
        for token in encrypted_message.split():
            if token.startswith("#"):
                # Handle unrecognized word
                unique_id = int(token[1:])
                decrypted_message.append(self._find_word_by_unique_id(unique_id))
            else:
                try:
                    position = int(token)
                    decrypted_message.append(words[position])
                except ValueError:
                    decrypted_message.append("?")  # Indicate unparseable numbers
        return " ".join(decrypted_message)

    def _find_word_by_unique_id(self, unique_id):
        current_node = self.unrecognized_words
        while current_node:
            if current_node.unique_id == unique_id:
                return current_node.word
            current_node = current_node.nextNode
        return "?"
