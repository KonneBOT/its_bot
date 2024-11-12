from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == 'asdf':
        choice(['I do not understand.', 'I am not sure what you mean.', 'Could you rephrase that?'])
    elif 'hello' in lowered:
        return "Hello there!"
    elif 'bye' in lowered:
        return "Goodbye!"
    elif 'hower' in lowered:
        return choice(['Der VDI wird Sie nicht retten!', 'Ja ne, das ist falsch', 'Denkste das ist richtig?', "Sehen und Hören Sie mich?"])
    elif 'roll' in lowered:
        return f"You rolled a {randint(1, 6)}."