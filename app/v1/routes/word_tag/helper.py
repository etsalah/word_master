from typing import List, Set
from app.v1.database.models.word_tag import WordTag
from app.v1.database.models.tag import Tag


def process_choosen_word_str(choosen_words_str: str) -> List[List]:
    choosen_words_lst = [
        choosen_word.split("$$")
        for choosen_word in choosen_words_str.split(",")
    ]
    return choosen_words_lst


def get_common_tag_lst(db_obj, choosen_words_lst: List[List]) -> Set[str]:
    word_ids = [choosen_word[0] for choosen_word in choosen_words_lst]
    stmt = db_obj.Select(
        WordTag.tag_id, WordTag.word_tag_id, Tag.tag, Tag.tag_id
    ).join(
        Tag, Tag.tag_id==WordTag.tag_id
    ).filter(
        WordTag.word_id.in_(word_ids)
    )
    
    common_tags_ls = db_obj.session.execute(stmt).all()
    common_tags_set = set()
    for comm in common_tags_ls:
        common_tags_set.add(comm.tag)
    return common_tags_set


def get_available_tags(db_obj):
    available_tag_list = db_obj.session.execute(
        db_obj.Select(Tag)
    ).scalars()
    return available_tag_list
