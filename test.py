def infer_key():
    # text = self.readfile('Please enter the file to analyze: ')
    # freq_file = self.readfile(
    #     'Please enter the reference frequencies file: ')
    text = 'ABACCC'
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

    print(sorted_letter_counts[0][0])


infer_key()
