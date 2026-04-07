"""Primo Progetto - A simple Python application."""


def greet(name: str) -> str:
    """Return a greeting message for the given name."""
    return f"Ciao, {name}! Benvenuto in Primo Progetto!"


def main():
    """Entry point for the application."""
    print(greet("World"))


if __name__ == "__main__":
    main()
