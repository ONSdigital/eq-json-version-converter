import re

from app.metadata_substitutions import metadata_substitutions
from app.helpers.rule_processor import process_rules
from app.rules.v2_to_v3.general_conversions import (
    delete_parent_id,
    update_guidance_content_key,
    rename_content_key,
)


def question_conversions(all_questions):

    question_rules = {
        'rename_single_questions_key': rename_single_questions_key,
        'delete_parent_id': delete_parent_id,
        'update_guidance_content_key': update_guidance_content_key,
        'rename_question_definitions_content_key': rename_question_definitions_content_key,
        'update_placeholder_in_question_titles': update_placeholder_in_question_titles,
        'update_em_tags_to_strong': update_em_tags_to_strong,
    }

    process_rules(all_questions, question_rules)


def update_placeholder_in_question_titles(question):

    if 'title' in question:
        placeholders = []
        question_title = question['title']

        placeholders_to_replace = [
            {'pattern': '{{ answers', 'source': 'answers'},
            {'pattern': '{{ metadata', 'source': 'metadata'},
        ]

        for to_replace in placeholders_to_replace:
            to_replace_pattern = to_replace.get('pattern')

            if to_replace_pattern in question_title:
                pattern_matches_in_title = find_pattern_in_title(
                    question_title, to_replace_pattern
                )
                question_title = update_title_with_new_placeholders(
                    pattern_matches_in_title, question_title, to_replace_pattern
                )
                placeholders.extend(
                    create_new_placeholders(
                        pattern_matches_in_title, to_replace.get('source')
                    )
                )

        if placeholders:
            question['title'] = {'placeholders': placeholders, 'text': question_title}


def find_pattern_in_title(question_title, to_replace_pattern):
    # pylint: disable=W1401
    pattern_matches_in_title = re.findall(
        to_replace_pattern + "\['(.*?)'\] }}", question_title
    )
    return pattern_matches_in_title


def update_title_with_new_placeholders(
    pattern_matches_in_title, question_title, to_replace_pattern
):
    for title_match in pattern_matches_in_title:
        question_title = check_metadata_substitutions_to_determine_title(
            title_match, to_replace_pattern, question_title
        )
    return question_title


def check_metadata_substitutions_to_determine_title(
    title_match, pattern, question_title
):
    # pylint: disable=W1401
    string_to_replace = pattern + "\['" + title_match + "'\] }}"

    for substitution in metadata_substitutions:
        if title_match == substitution.get('metadata_name'):

            return re.sub(
                string_to_replace,
                '{' + substitution.get('placeholder_name') + '}',
                question_title,
            )
    return re.sub(
        string_to_replace, '{' + title_match.replace('-', '_') + '}', question_title
    )


def create_new_placeholders(pattern_matches_in_title, source):
    placeholders = []
    for title_match in pattern_matches_in_title:
        placeholder = check_metadata_substitutions_to_determine_which_placeholder(
            source, title_match
        )
        placeholders.append(placeholder)
    return placeholders


def check_metadata_substitutions_to_determine_which_placeholder(source, title_match):
    for replacement in metadata_substitutions:
        if title_match == replacement.get('metadata_name'):

            return {
                'placeholder': replacement.get('placeholder_name'),
                'transforms': [
                    {
                        'transform': replacement.get('transform'),
                        'arguments': {
                            'items': {
                                'source': 'metadata',
                                'identifier': replacement.get('identifier'),
                            }
                        },
                    }
                ],
            }
        return {
            'placeholder': title_match.replace('-', '_'),
            'value': {'identifier': title_match, 'source': source},
        }


def update_em_tags_to_strong(question):
    if question.get('description'):
        question['description'] = question['description'].replace('em>', 'strong>')


def rename_question_definitions_content_key(question):
    for definition in question.get('definitions', []):
        rename_content_key(definition)


def rename_single_questions_key(question):
    if 'questions' in question:
        if len(question['questions']) == 1:
            question['question'] = question['questions'][0]
            del question['questions']
