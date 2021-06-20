import os, sys
import pathlib
from app.database.models.v1.word import Word


def read_word_file():pass

def process_words():pass

def save_words():pass


def main():
    prog_args = sys.argv
    if len(prog_args) < 3:
        print(
            "You need to pass in the name of the file with the new words to "
            "add to the application"
        )
        sys.exit(0)

    file_of_words = pathlib.path(prog_args[2])

    if not file_of_words.exists():
        print(
            f"The location you specified `{prog_args[2]}` doesn't exists"
        )
        sys.exit(0)

    read_word_file(file_of_words)


if __name__ == "__main__":
    pass
