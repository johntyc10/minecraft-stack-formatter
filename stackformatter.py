"""Minecraft stack formatter"""

try:
    import pyperclip
    pyperclip_imported = True
except ImportError:
    print("[WARNING] Module pyperclip not found. Skipping copy.")
    pyperclip_imported = False


STACK_SIZE = 64


def prompt_yes_no(message: str, *, default_yes: bool = True):
    """
    Prompts yes / no with format {message} [y/n]:.
    Returns True if the answer is yes.
    Returns False if the answer is no.
    default_yes: if unset, the default answer is yes, otherwise if default_yes=False, set the default answer to no
    """

    while True:
        try:
            resp = input(f"{message} [{'Y' if default_yes else 'y'}/{'N' if not default_yes else 'n'}]: ").strip().lower()
        except EOFError:
            return default_yes

        if not resp:
            return default_yes

        if resp in ["y", "yes"]:
            return True
        elif resp in ["n", "no"]:
            return False
        print('Invalid input, please answer "yes" or "no".')

def get_material_list() -> dict:
    material_list = {}

    while True:
        item_name = input("Enter item name (press enter to stop inputting items): ").strip()

        if not item_name:
            yes = prompt_yes_no("Are you sure you want to stop inputting items?")

            if yes:
                break
            else:
                continue

        if item_name in material_list:
            yes = prompt_yes_no(f'"{item_name}" already exists.\n'
                'If you proceed, the previous count will be **permanently overwritten**.\n'
                'Proceed and overwrite item count?', default_yes=False)

            if not yes:
                continue

        item_count = input("Enter item count: ")
        try:
            item_count = int(item_count)
        except ValueError:
            print("[ERROR] Please enter an integer.")
            continue

        if item_count <= 0:
            print("Please enter a positive integer.")
            continue

        material_list[item_name] = item_count

    return material_list

def sort_by_count_desc(material_list: dict[str, int]) -> dict:
    return dict(sorted(material_list.items(), key=lambda item: item[1], reverse=True))

def generate_material_list(material_list: dict) -> str:
    """
    Generate a material list with stacks calculated given a material list input.
    Returns a string of the generated material list.
    """
    generated_material_list = []
    for item in material_list:
        item_count = material_list[item]
        if item_count < STACK_SIZE:
            generated_material_list.append(f"{item_count} {item}")
        else:
            generated_material_list.append(f"{item_count} ({item_count // STACK_SIZE}s + {item_count % STACK_SIZE}) {item}")

    return "\n".join(generated_material_list)


if __name__ == "__main__":
    material_list = get_material_list()
    sorted_material_list = sort_by_count_desc(material_list)
    generated_material_list = generate_material_list(sorted_material_list)

    print("Generated material list:")
    print(generated_material_list)

    if pyperclip_imported:
        try:
            pyperclip.copy(generated_material_list)
            print("Generated material list copied to clipboard.")
        except Exception as e:
            print("If you are on ARCH BTW or ARCH BTW based os, installing the following packages may help:")
            print("X11: install xsel AND xclip.")
            print("Wayland: install wl-clipboard.")
            print(f"Copying generated material list to clipboard failed: {e}")
