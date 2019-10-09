import re

from app.helpers.rule_processor import process_rules
from app.rules.v2_to_v3.general_conversions import (
    delete_parent_id,
    update_guidance_content_key,
    rename_content_key,
)


def question_conversions(all_questions):

    question_rules = {
        "rename_single_questions_key": rename_single_questions_key,
        "delete_parent_id": delete_parent_id,
        "update_guidance_content_key": update_guidance_content_key,
        "rename_question_definitions_content_key": rename_question_definitions_content_key,
        "update_placeholder_in_question_titles": update_placeholder_in_question_titles,
    }

    process_rules(all_questions, question_rules)


def update_placeholder_in_question_titles(question):

    if "title" in question:
        placeholders = []
        question_title = question["title"]

        placeholders_to_replace = [
            {"pattern": "{{ answers", "source": "answers"},
            {"pattern": "{{ metadata", "source": "metadata"},
        ]

        for pattern in placeholders_to_replace:
            if pattern.get("pattern") in question_title:
                pattern_matches_in_title = find_pattern_in_title(
                    question_title, pattern.get("pattern")
                )
                question_title = update_title_with_new_placeholders(
                    pattern_matches_in_title, question_title, pattern.get("pattern")
                )
                placeholders.extend(
                    create_new_placeholders(
                        pattern_matches_in_title, pattern.get("source")
                    )
                )

        if placeholders:
            question["title"] = {"placeholders": placeholders, "text": question_title}


def find_pattern_in_title(question_title, pattern):
    pattern_matches_in_title = re.findall(pattern + "\['(.*?)'\] }}", question_title)
    return pattern_matches_in_title


def update_title_with_new_placeholders(pattern_matches_in_title, question_title, pattern):
    for match in pattern_matches_in_title:
        question_title = re.sub(
            pattern + "\['" + match + "'\] }}",
            "{" + match.replace("-", "_") + "}",
            question_title,
        )
    return question_title


def create_new_placeholders(pattern_matches_in_title, source):

    placeholders = []
    for match in pattern_matches_in_title:
        placeholder = {
            "placeholder": match.replace("-", "_"),
            "value": {"identifier": match, "source": source},
        }
        placeholders.append(placeholder)
    return placeholders


def rename_question_definitions_content_key(question):
    if "definitions" in question:
        for definition in question["definitions"]:
            rename_content_key(definition)


def rename_single_questions_key(question):
    if "questions" in question:
        if len(question["questions"]) == 1:
            question["question"] = question["questions"][0]
            del question["questions"]
