from pypdf import PdfReader
import re
import numpy as np

# creating a pdf reader object
def extract_moduls(pdf) -> list:
    reader = PdfReader(pdf)
    modul = {
        "Studiensemester": None,
        "Modul": None,
    }
    moduls = []
    arrays=[]
    for i in range(len(reader.pages)):
        frac = round(100/(len(reader.pages))*i)
        print('\r'"|"+"█"*frac+" "*(100-frac)+"|"+f" page {i}/{len(reader.pages)} - Items {len(arrays)}", end='')
        page = reader.pages[i]
        text = page.extract_text()
        Aarray = text.split('\n')
        arrays = np.concatenate((arrays, Aarray))
    print('\r'"|"+"█"*100+"|"+f" pages complete - Items:{len(arrays)}\n", end='')
    for i in range(len(arrays)):
        if re.search(r"Modul: .*", arrays[i]) is not None:
            modul["Modul"] = arrays[i].split(": ")[1][:-1].strip().replace(" ", "-").lower()
        if arrays[i] == "Studiensemester ":
            modul["Studiensemester"] = arrays[i + 1][0]
            moduls.append(modul)
            modul = {
                "Studiensemester": None,
                "Modul": None,
            }

    print(f"{len(moduls)} Moduls extracted")
    return moduls