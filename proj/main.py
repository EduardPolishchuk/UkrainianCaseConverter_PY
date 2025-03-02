import sys

import pymorphy2

morph = pymorphy2.MorphAnalyzer(lang='uk')


def _decline_full_name(full_name):
    full_name_list = full_name.split(" ")

    if len(full_name_list) == 2:
        # If there are only two parts, pass them to the decline function with None or an empty string for patronymic
        modified_content = decline(full_name_list[0], full_name_list[1], "")
    elif len(full_name_list) == 3:
        # If there are three parts (first, last name, and patronymic), pass them all
        modified_content = decline(full_name_list[0], full_name_list[1], full_name_list[2])
    else:
        # Handle the case where there are fewer than 2 parts (invalid name format)
        modified_content = full_name_list

    return modified_content

def decline(last_name, first_name, patronymic):
    last_name_nomn = _decline_with(last_name, 'nomn')
    first_name_nomn = _decline_with(first_name, 'nomn')
    patronymic_nomn = _decline_with(patronymic, 'nomn')

    last_name_gentv = _decline_with(last_name, 'gent')
    first_name_gentv = _decline_with(first_name, 'gent')
    patronymic_gentv = _decline_with(patronymic, 'gent')

    last_name_datv = _decline_with(last_name, 'datv')
    first_name_datv = _decline_with(first_name, 'datv')
    patronymic_datv = _decline_with(patronymic, 'datv')

    full_name_nomn = f"{last_name_nomn} {first_name_nomn} {patronymic_nomn}"
    full_name_genitive = f"{last_name_gentv} {first_name_gentv} {patronymic_gentv}"
    full_name_dative = f"{last_name_datv} {first_name_datv} {patronymic_datv}"

    return full_name_nomn, full_name_genitive, full_name_dative

def _decline_with(name, decliner):
    if not name:
        name_result = name
    else:
        parsed = morph.parse(name)[0]
        declined = parsed.inflect({decliner})
        name_result = declined.word.capitalize() if declined else f"*{name.capitalize()}"

    return name_result

def main():
    # Check if there are any command-line arguments
    if len(sys.argv) > 1:
        file_name = sys.argv[1]  # File to decline
        declined_file_name = sys.argv[2] # Declined file

        # Step 1: Read the original file
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()

        array = []
        for name in content.split("\n"):
            # Step 2: Modify the content (example: replace "old" with "new")
            array.append("\t".join(_decline_full_name(name)))

        # Step 3: Write the modified content to a new file
        with open(declined_file_name, "w", encoding="utf-8") as file:
            for line in array:
                file.write(line + "\n")

        print(f"File processed and saved as {declined_file_name}")
    else:
        print("No parameters provided")

if __name__ == "__main__":
    main()

