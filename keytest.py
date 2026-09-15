from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

kb = KeyBindings()


@kb.add("<any>")
def _(event):
    print(f"\nKEY: {event.key_sequence}")
    event.current_buffer.insert_text("")


session = PromptSession(key_bindings=kb)

while True:
    session.prompt("Test: ")
