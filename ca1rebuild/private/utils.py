from private.menu import Menu


class FileOperator:
    def __init__(self):
        self.menu = Menu()

    def writefile(self, content, output_file_name="?"):
        if output_file_name == "?":
            print("File is not found")
            Menu().select_option()

        with open(output_file_name, "w") as output_file:
            output_file.write(content)

    def readfile(self, input_file_name="?"):
        if input_file_name == "?":
            print("File is not found")
            Menu().select_option()

        with open(input_file_name, "r") as input_file:
            return input_file.read()


class Utility:
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

    def display_gui(self, array):
        for row in array:
            row_string = ""
            for cell in row:
                row_string += cell
            print(f"{row_string}")
