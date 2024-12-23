from .jokes import get_joke


def tell_me():
    joke = get_joke()
    print(f"{joke["preambula"]} ... {joke['punchline']}")
