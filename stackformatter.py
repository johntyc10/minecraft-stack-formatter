"""Minecraft stack formatter"""

try:
    import pyperclip
    pyperclip_imported = True
except ImportError:
    print("[WARNING] Module pyperclip not found. Skipping copy.")
    pyperclip_imported = False


def item_count_to_string(item_name: str, count: int) -> str:
    """
    Takes item name (str) and (count): int as argument and returns human interpretable item count (string).
    Eg. input: cobblestone, 149 -> output: 149 (2 stacks + 21) cobblestone
    """

    STACK_SIZE = 64
    SHULKER_BOX_SIZE = 27 * STACK_SIZE

    if count < 0:
        raise ValueError("count cannot be less than 0!")

    if count < STACK_SIZE:
        return f"{count} {item_name}"

    shulker_box_count = count // SHULKER_BOX_SIZE
    remainder_stack_count = (count % SHULKER_BOX_SIZE) // STACK_SIZE
    remainder_count = (count % SHULKER_BOX_SIZE) % STACK_SIZE

    # sample strings
    # string = "count ([9dc + 1sb / 19sb] + 15s + 49) item_name"
    # string = "count (1sb + 15s + 49) item_name"

    quantity_list = []

    if shulker_box_count > 0:
        quantity_list.append(f"{shulker_box_count}sb")
    if remainder_stack_count > 0:
        quantity_list.append(f"{remainder_stack_count}s")
    if remainder_count > 0:
        quantity_list.append(f"{remainder_count}")

    return f"{count} ({" + ".join(quantity_list)}) {item_name}"

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


class StackFormatter:
    def __init__(self, list_input: dict[str, int] = {}) -> None:
        self.material_list = list_input

    def get_material_list(self) -> None:
        while True:
            item_name = input("Enter item name (press enter to stop inputting items): ").strip()

            if not item_name:
                yes = prompt_yes_no("Are you sure you want to stop inputting items?")

                if yes:
                    break
                else:
                    continue

            if item_name in self.material_list:
                yes = prompt_yes_no(f'"{item_name}" already exists.\n'
                    "If you proceed, the previous count will be **overwritten**.\n"
                    "Proceed and overwrite item count?", default_yes=False)

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

            self.material_list[item_name] = item_count

    def sort_material_list_by_count_desc(self) -> None:
        self.material_list = dict(sorted(self.material_list.items(), key=lambda item: item[1], reverse=True))

    def generate_material_list(self) -> str:
        """
        Generate a material list with stacks calculated given a material list input.
        Returns a string of the generated material list.
        """

        self.sort_material_list_by_count_desc()

        generated_material_list = []
        for item in self.material_list:
            item_count = self.material_list[item]
            generated_material_list.append(item_count_to_string(item, item_count))

        return "\n".join(generated_material_list)


if __name__ == "__main__":
    stackformatter = StackFormatter()
    stackformatter.get_material_list()
    generated_material_list = stackformatter.generate_material_list()

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
