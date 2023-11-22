class Menu:
    options = []

    def __init__(self, author_id=int, author_name=str, author_class=str):
        self.author_id = author_id
        self.author_name = author_name
        self.author_class = author_class
        self.width = 60

    def intro(self):
        print("*" * self.width)
        text = " ST1507 DSAA: Welcome to:"
        print(f"*{text}{' ' * (self.width-len(text)-2)}*")
        print(f"*{' ' * (self.width-2)}*")
        text = "~ Caeser Cipher Encrypted Message Analyzer ~"
        print(
            f"*{' ' * round((self.width-len(text)-2)/2)}{text}{' ' * (self.width - (round((self.width-len(text)-2)/2)+len(text))-2)}*"
        )
        print(f"*{'-' * (self.width-2)}*")
        text = f"    - Done by: {self.author_name}({self.author_id})"
        print(f"*{text}{' ' * (self.width-len(text)-2)}*")
        print(f"*{' ' * (self.width-2)}*")
        text = f"    - Class {self.author_class}"
        print(f"*{text}{' ' * (self.width-len(text)-2)}*")
        print("*" * self.width)
        self.select_option()

    def add(self, redirect, value, message):
        self.options.append((redirect, value, message))

    def print_menu(self):
        valid_choices = ",".join(str(i) for i in range(1, len(self.options) + 1))
        printmenu = f"\nPlease select your choice: ({valid_choices})\n\t"
        for option in self.options:
            _, value, message = option
            printmenu += f"{value}. {message}\n\t"
        print(printmenu)

    def select_option(self):
        input("Press enter key, to continue....")
        self.print_menu()
        choice = input("Enter the number of your choice: ")
        print()
        try:
            choice = int(choice)
            if 1 <= choice <= len(self.options):
                redirect, _, _ = self.options[choice - 1]
                if callable(redirect):
                    redirect()
                else:
                    print(f"Function not callable: {redirect}")
            else:
                print("Invalid choice. Please select a valid option.")
                self.select_option()
        except ValueError:
            print("Invalid input. Please enter a number.")
            self.select_option()

    def exit_menu(self):
        print(
            "Bye, thanks for using ST1507 DSAA: Caesar Cipher Encrypted Message Analyzer"
        )
        return
