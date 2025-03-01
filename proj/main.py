import sys

import pymorphy2

morph = pymorphy2.MorphAnalyzer(lang='uk')


def decline_to_genitive(last_name, first_name, patronymic, decliner):
    if not last_name:
        last_name_genitive = last_name
    else:
        parsed = morph.parse(last_name)[0]
        declined = parsed.inflect({decliner})
        last_name_genitive = declined.word.capitalize() if declined else last_name.capitalize()

    if not first_name:
        first_name_genitive = first_name
    else:
        parsed = morph.parse(first_name)[0]
        declined = parsed.inflect({decliner})
        first_name_genitive = declined.word.capitalize() if declined else first_name.capitalise()

    if not patronymic:
        patronymic_genitive = patronymic
    else:
        parsed = morph.parse(patronymic)[0]
        declined = parsed.inflect({decliner})
        patronymic_genitive = declined.word.capitalize() if declined else patronymic.capitalise()

    return last_name_genitive, first_name_genitive, patronymic_genitive


def main():
    # Check if there are any command-line arguments
    if len(sys.argv) > 1:
        file_name = sys.argv[1]  # File to decline
        decliner = sys.argv[2]  # Decliner parameter
        declined_file_name = sys.argv[3]  # Declined file

        # Step 1: Read the original file
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()

        array = []
        for name in content.split("\n"):
            # Step 2: Modify the content (example: replace "old" with "new")
            full_name = name.split(" ")

            if len(full_name) == 2:
                # If there are only two parts, pass them to the decline function with None or an empty string for patronymic
                modified_content = decline_to_genitive(full_name[0], full_name[1], "", decliner)
            elif len(full_name) == 3:
                # If there are three parts (first, last name, and patronymic), pass them all
                modified_content = decline_to_genitive(full_name[0], full_name[1], full_name[2], decliner)
            else:
                # Handle the case where there are fewer than 2 parts (invalid name format)
                modified_content = full_name
            array.append(" ".join(modified_content))

        # Step 3: Write the modified content to a new file
        with open(declined_file_name, "w", encoding="utf-8") as file:
            for line in array:
                file.write(line + "\n")

        print(f"File processed and saved as {declined_file_name}")
    else:
        print("No parameters provided")


if __name__ == "__main__":
    main()
