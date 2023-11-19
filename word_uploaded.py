import os, sys

from typing import Dict
import pathlib

from sqlalchemy.exc import IntegrityError

from app.v1.database.models.word import Word
from app.v1.helpers.id_helpers import generate_id
from app import db_manager as db
from app import app

from app.v1.helpers import query_helpers


def read_word_file(words_file):
    with open(words_file, "r") as input_file:
        for line in input_file.readlines():
            words = line.split(",")
            process_words(words)


def process_words(words):
    for word in words:
        word_txt = str(word).strip().replace('\n', '')
        if len(word_txt) == 0:
            continue
        word_id = generate_id()
        worder_id = save_words({
            'word': word_txt.lower(), 'length': len(word_txt),
            'word_id': word_id
        })
        # TODO: Add some other classifiers here


def save_words(word_details: Dict):
    word_id = word_details['word_id']
    with app.app_context():
        try:
            word_obj = Word(
                word_id=word_id, word=word_details['word'], 
                length=word_details['length']
            )
            db.session.add(word_obj)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            found_obj = query_helpers.find_by_params(
                db.session, Word, [{'word': {'$eq': word_details['word']}}])
        
            if found_obj:
                word_id = found_obj.word_id

    return word_id


def main():
    prog_args = sys.argv
    if len(prog_args) < 2:
        print(
            "You need to pass in the name of the file with the new words to "
            "add to the application"
        )
        sys.exit(0)

    # print(f"{prog_args[0]} => {prog_args[1]}")

    file_of_words = pathlib.Path(prog_args[1])

    if not file_of_words.exists():
        print(
            f"The location you specified `{prog_args[2]}` doesn't exists"
        )
        sys.exit(0)

    read_word_file(file_of_words)


if __name__ == "__main__":
    main()
