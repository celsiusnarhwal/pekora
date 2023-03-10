from functools import wraps

from InquirerPy import inquirer


def prompt_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get("multiselect"):
            keybindings = {
                "toggle": [{"key": "c-s"}],
                "toggle-all-true": [{"key": "c-a"}],
                "toggle-all-false": [{"key": "c-z"}],
            }

            long_instruction = (
                "↑/↓: Move up and down\n"
                "Control + S: Toggle selection\n"
                "Control + A: Toggle all on\n"
                "Control + Z: Toggle all off\n"
                "Enter: Confirm\n"
            )

        else:
            keybindings = {
                "answer": [{"key": "enter"}, {"key": "c-z"}],
            }

            long_instruction = ""

        defaults = {
            "keybindings": keybindings,
            "long_instruction": long_instruction,
            "qmark": "•",
            "amark": "✓",
            "mandatory_message": "You can't skip this.",
            "raise_keyboard_interrupt": True,
        }

        for key, value in defaults.items():
            kwargs.setdefault(key, value)

        return func(*args, **kwargs)

    return wrapper


checkbox = prompt_decorator(inquirer.checkbox)
confirm = prompt_decorator(inquirer.confirm)
expand = prompt_decorator(inquirer.expand)
filepath = prompt_decorator(inquirer.filepath)
fuzzy = prompt_decorator(inquirer.fuzzy)
text = prompt_decorator(inquirer.text)
select = prompt_decorator(inquirer.select)
number = prompt_decorator(inquirer.number)
rawlist = prompt_decorator(inquirer.rawlist)
secret = prompt_decorator(inquirer.secret)
