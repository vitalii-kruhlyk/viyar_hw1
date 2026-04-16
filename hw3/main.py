from typing import Callable
import inspect

contacts = {}
dict_keys_type = type({}.keys())


def input_error(func):
    def new_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "ERROR: Contact not found"
        except ValueError:
            return "ERROR: Not enough arguments"
        except IndexError:
            return "ERROR: No name found"

    return new_func


@input_error
def add_contact(name: str, phone: str) -> str:
    contacts[name] = phone
    return f"Contact {name} added."


@input_error
def change_contact(name: str, phone: str) -> str:
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return f"Contact {name} updated."


@input_error
def get_phone(name: str) -> str:
    return contacts[name]


def show_all() -> str:
    return f"Count: {len(contacts)}\n{'\n'.join(f'{name}: {phone}' for name, phone in contacts.items())}"


def hello_command():
    print("How can I help you?")


def parse_command(
    user_input: str, command_keys: dict_keys_type, multiword_commands: list[str]
) -> tuple[str | None, list[str]]:

    parts = user_input.split()
    if not parts:
        return None, []
    command = parts[0]

    if command not in command_keys and len(parts) > 1:
        for multiword_command in multiword_commands:
            if user_input.startswith(multiword_command):
                command = multiword_command
                break

    return command, user_input.removeprefix(command).split()


def exit_command():
    return "Good bye!"


def get_commands() -> dict[str, Callable]:
    return {
        "hello": hello_command,
        "add": add_contact,
        "change": change_contact,
        "phone": get_phone,
        "show all": show_all,
        "good bye": exit_command,
        "close": exit_command,
        "exit": exit_command,
    }


@input_error
def main():
    print("Bot assistant started. Type 'hello' to begin.")
    commands = get_commands()
    multiword_commands = [command for command in commands.keys() if " " in command]
    while True:
        user_input = input(">>> ").strip().lower()

        if not user_input:
            continue

        if user_input in ("good bye", "close", "exit"):
            print("Bye!")
            break

        command, args = parse_command(user_input, commands.keys(), multiword_commands)

        current_action = commands.get(command) if isinstance(command, str) else None
        if not current_action:
            print(f"Unknown command. Available: {', '.join(commands.keys())}.")
            continue

        func_signature = inspect.signature(current_action)
        if len(func_signature.parameters) != len(args):
            print(
                f"Incorrect number of arguments. Needed {len(func_signature.parameters)}, provided: {len(args)}."
            )
            continue

        result = current_action(*args)
        if result:
            print(result)

        if current_action.__name__ == "exit_command":
            break


if __name__ == "__main__":
    main()
