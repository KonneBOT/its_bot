from random import choice, randint
import codecs
f = codecs.open("zitate.md", "r", "utf-8")
quotes = f.readlines()[2:]

def get_response(user_input: str) -> str:

    lowered: str = user_input.lower()

    match True:
        case _ if lowered == "":
            return None
        case _ if lowered == "asdf":
            return choice(['I do not understand.', 'I am not sure what you mean.', 'Could you rephrase that?'])
        case _ if "hello there" in lowered:
            return "General Kenobi!"
        case _ if "hello" in lowered:
            return "Hello there!"
        case _ if "bye" in lowered:
            return "Goodbye!"
        case _ if "hower" in lowered:
            return choice(quotes).strip("\r\n")
        case _ if "roll" in lowered and "rollen" not in lowered:
            return f"You rolled a {randint(1, 6)}."
        case _:
            return None