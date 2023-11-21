from private.ciphertools import Sha
from private.menu import Menu
import os


class FileOperator:
    def __init__(self):
        self.menu = Menu()

    def writefile(self, content, output_file_name):
        if content is None:
            print("content is null")
            self.menu.select_option()

        with open(output_file_name, "w") as output_file:
            output_file.write(content)

    def readfile(self, input_file_name):
        if not os.path.exists(input_file_name):
            print(f"File {input_file_name} not found. Please try again.")
            reinput = input("Please re-input the file name: ")
            if reinput.upper() == "Q":
                self.menu.select_option()
            return self.readfile(reinput)

        with open(input_file_name, "r") as input_file:
            return input_file.read()


class Utility:
    def __init__(self, password=str):
        self.sha = Sha()
        self.menu = Menu()
        self.hash_password = self.sha.hash(password)

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

    def pwcheck(self, counter=0):
        counter += 1
        input_pw = input("Enter the Private Key: ")
        if input_pw.upper() == "Q":
            self.menu.select_option()
        else:
            if self.sha.check(input_pw, self.hash_password):
                return
            else:
                print("Private Key incorrect")
                if counter > 3:
                    print(
                        f"Terminal is requesting for matching Private Key\n[Public_Key: {self.hash_password}]"
                    )
                self.pwcheck(counter)

    def sort_linked_list(self, head):
        if not head or not head.nextNode:
            return head

        # Split the list into two halves
        middle = self.get_middle(head)
        next_to_middle = middle.nextNode
        middle.nextNode = None

        # Sort each half
        left = self.sort_linked_list(head)
        right = self.sort_linked_list(next_to_middle)

        # Merge the sorted halves
        sorted_list = self.sorted_merge(left, right)
        return sorted_list

    def get_middle(self, head):
        if head is None:
            return head

        slow = head
        fast = head.nextNode

        # Move fast by two and slow by one
        while fast:
            fast = fast.nextNode
            if fast:
                fast = fast.nextNode
                slow = slow.nextNode

        return slow

    def sorted_merge(self, a, b):
        result = None

        # Base cases
        if a is None:
            return b
        elif b is None:
            return a

        # Pick either a or b and recur using get_comp_key
        if a.get_comp_key() < b.get_comp_key():
            result = a
            result.nextNode = self.sorted_merge(a.nextNode, b)
        else:
            result = b
            result.nextNode = self.sorted_merge(a, b.nextNode)

        return result


class FrequencyNode:
    def __init__(self, letter=None, frequency=0, nextNode=None):
        self.letter = letter
        self.frequency = frequency
        self.nextNode = nextNode

    def get_comp_key(self):
        return self.frequency

    def __lt__(self, other):
        return self.get_comp_key() < other.get_comp_key()


class FileSortNode:
    def __init__(
        self, file_name=None, best_shift=None, decrypted_text=None, nextNode=None
    ):
        self.file_name = file_name
        self.best_shift = best_shift
        self.decrypted_text = decrypted_text
        self.nextNode = nextNode

    def get_comp_key(self):
        return self.best_shift

    def __lt__(self, otherNode):
        return self.get_comp_key() < otherNode.get_comp_key()
