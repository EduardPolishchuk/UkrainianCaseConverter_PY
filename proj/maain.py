import pymorphy2

morph = pymorphy2.MorphAnalyzer(lang='uk')

def decline_to_genitive(last_name, first_name, patronymic):
    last_name_genitive = morph.parse(last_name)[0].inflect({'gent'}).word.capitalize()
    first_name_genitive = morph.parse(first_name)[0].inflect({'gent'}).word.capitalize()
    patronymic_genitive = morph.parse(patronymic)[0].inflect({'gent'}).word.capitalize()

    return last_name_genitive, first_name_genitive, patronymic_genitive


if __name__ == "__main__":
    last_name_genitive, first_name_genitive, patronymic_genitive = decline_to_genitive("Іванов", "Іван", "Іванович")

    print(f"{last_name_genitive} {first_name_genitive} {patronymic_genitive}")