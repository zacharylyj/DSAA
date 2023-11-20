from private.menu import Menu
from private.controller import Controller

menu = Menu(2201861, "Zachary Leong", "DAAA/2B/01")
controller = Controller()


def main():
    menu.add(controller.encrypt_decrypt_message, 1, "Encrypt/Decrypt Message")
    menu.add(controller.encrypt_decrypt_file, 2, "Encrypt/Decrypt File")
    menu.add(controller.letter_frequency, 3, "Analyze letter frequency distribution")
    menu.add(controller.infer_key, 4, "Infer caesar cipher key from file")
    menu.add(controller.sort_file, 5, "Analyze, and sort encrypted files")
    menu.add(controller.option1, 6, "Extra Option One")
    menu.add(controller.option2, 7, "Extra Option Two")
    menu.add(menu.exit_menu, 8, "Exit")

    menu.intro()


if __name__ == "__main__":
    main()
