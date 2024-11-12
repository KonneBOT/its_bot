from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return "Hmm, you quiet aren't you?"
    elif 'hello' in lowered:
        return "Hello there!"
    elif 'bye' in lowered:
        return "Goodbye!"
    elif 'roll' in lowered:
        return f"You rolled a {randint(1, 6)}."
    else:
        return choice(['I do not understand.', 'I am not sure what you mean.', 'Could you rephrase that?'])