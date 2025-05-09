from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == "":
        return
    elif lowered == 'asdf':
        choice(['I do not understand.', 'I am not sure what you mean.', 'Could you rephrase that?'])
    elif 'hello there' in lowered:
        return "General Kenobi!"
    elif 'hello' in lowered:
        return "Hello there!"
    elif 'bye' in lowered:
        return "Goodbye!"
    elif 'hower' in lowered:
        return choice(['Der VDI wird Sie nicht retten!', 'Ja ne, das ist falsch', 'Denkste das ist richtig?', 
                       "Sehen und Hören Sie mich?", "Was mein Sie dahinten im Lovechair?", "Grüße an das Reha Zentrum!",
                       "Sie kommen nie in den 05er!", "Dreimal durch die Brust geschossen!", "Das ist der gängige Fehler!",
                       "Das brauchen Sie sich nicht auf die Sprudelflasche schreiben", "Danach ist Apfelmus!", 
                       "Danach ist Französische Revolution!", "Wenn der Index außerhalb der Liste ist, fährt ja der Computer runter 🫠",
                       "Also man kann es ja verkacken, aber so???", "Jetzt mach ich erstmal Sie fertig!"])
    elif 'roll' in lowered and not "rollen" in lowered:
        return f"You rolled a {randint(1, 6)}."