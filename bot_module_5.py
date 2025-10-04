import json
import os

contacts = {}


def load_contacts():
    global contacts
    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as f:
            contacts = json.load(f)


def save_contacts():
    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)


def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return None, []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def input_error(func):
    def wrapper(args):
        try:
            return func(args)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Not enough arguments. Please try again."
        except KeyError:
            return "This contact does not exist."
        except Exception as e:  # про всяк випадок
            return f"Unexpected error: {e}"
    return wrapper


@input_error
def add_contact(args):
    name, phone = args  # ValueError сам виникне, якщо args не рівно 2
    contacts[name] = phone
    save_contacts()
    return "Contact added."


@input_error
def change_contact(args):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        save_contacts()
        return "Contact updated."
    else:
        raise KeyError


@input_error
def show_phone(args):
    name = args[0]  # IndexError, якщо пусто
    if name in contacts:
        return contacts[name]
    else:
        raise KeyError


@input_error
def show_all(args):
    if not contacts:
        return "No contacts saved."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main():
    load_contacts()
    print("Welcome to Assistant Bot!")
    while True:
        user_input = input(">>> ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args))
        elif command == "change":
            print(change_contact(args))
        elif command == "phone":
            print(show_phone(args))
        elif command == "all":
            print(show_all(args))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
