from datetime import datetime, timedelta
import pickle

# Decorator to handle input errors gracefully
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please enter valid data."
        except IndexError:
            return "Invalid number of arguments. Please check usage."
        except KeyError:
            return "Contact not found. Please check the name."
    return wrapper

# Class to handle birthdays
class Birthday:
    def __init__(self, date):
        self.date = datetime.strptime(date, "%d.%m.%Y").date()

# Class to represent a contact record
class Record:
    def __init__(self, phone, birthday=None):
        self.phone = phone
        self.birthday = birthday

    def add_birthday(self, date):
        self.birthday = Birthday(date)
        return "Birthday added."

# Class to handle the address book
class AddressBook:
    def __init__(self):
        self.contacts = {}

    @input_error
    def add_contact(self, username, phone):
        if username in self.contacts:
            return "Contact already exists. Use 'change' command to update the phone number."
        self.contacts[username] = Record(phone)
        return "Contact added."

    @input_error
    def change_contact(self, username, phone):
        if username in self.contacts:
            self.contacts[username].phone = phone
            return "Contact updated."
        else:
            return "Contact not found."

    @input_error
    def show_phone(self, username):
        return f"{username}'s phone number is: {self.contacts[username].phone}"

    def show_all(self):
        if not self.contacts:
            return "No contacts available."
        else:
            result = "All contacts:\n"
            for username, record in self.contacts.items():
                result += f"{username}: {record.phone}"
                if record.birthday:
                    result += f", Birthday: {record.birthday.date.strftime('%d.%m.%Y')}"
                result += "\n"
            return result.strip()  # Strip trailing newline

    @input_error
    def add_birthday(self, username, date):
        return self.contacts[username].add_birthday(date)

    @input_error
    def show_birthday(self, username):
        return f"{username}'s birthday is on {self.contacts[username].birthday.date.strftime('%d.%m.%Y')}"

    def birthdays_per_week(self):
        today = datetime.now().date()
        next_week = today + timedelta(days=(7 - today.weekday()))
        upcoming_birthdays = [username for username, record in self.contacts.items()
                              if record.birthday and record.birthday.date <= next_week]
        return upcoming_birthdays

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.contacts, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.contacts = pickle.load(file)
            return "Address book loaded successfully."
        except FileNotFoundError:
            return "No saved address book found."

# Main function to handle user input and interact with the contact book
if __name__ == "__main__":

    def main():
        book = AddressBook()

        print("Welcome to the assistant bot!")

        while True:
            user_input = input("Enter a command: ").strip().lower()
            command, *args = user_input.split()

            if command in ["close", "exit"]:
                print("Goodbye!")
                book.save_to_file("address_book.pkl")  # Save address book before exiting
                break

            elif command == "add":
                if len(args) == 2:
                    username, phone = args
                    print(book.add_contact(username, phone))
                else:
                    print("Invalid command. Usage: add username phone")

            elif command == "change":
                if len(args) == 2:
                    username, phone = args
                    print(book.change_contact(username, phone))
                else:
                    print("Invalid command. Usage: change username phone")

            elif command == "phone":
                if len(args) == 1:
                    username = args[0]
                    print(book.show_phone(username))
                else:
                    print("Invalid command. Usage: phone username")

            elif command == "all":
                print(book.show_all())

            elif command == "add-birthday":
                if len(args) == 2:
                    username, date = args
                    print(book.add_birthday(username, date))
                else:
                    print("Invalid command. Usage: add-birthday username DD.MM.YYYY")

            elif command == "show-birthday":
                if len(args) == 1:
                    username = args[0]
                    print(book.show_birthday(username))
                else:
                    print("Invalid command. Usage: show-birthday username")

            elif command == "birthdays":
                upcoming_birthdays = book.birthdays_per_week()
                if upcoming_birthdays:
                    print(f"Upcoming birthdays to celebrate: {', '.join(upcoming_birthdays)}")
                else:
                    print("No upcoming birthdays in the next week.")

            elif command == "hello":
                print("Hello! How can I assist you today?")

            else:
                print("Invalid command")

    main()
