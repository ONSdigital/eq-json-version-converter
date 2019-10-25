from app.helpers.rule_processor import process_rules
from app.rules.v2_to_v3.general_conversions import (
    delete_parent_id,
    update_guidance_content_key,
)


def answer_conversions(all_answers):

    answer_rules = {
        'delete_parent_id': delete_parent_id,
        'update_guidance_content_key': update_guidance_content_key,
    }
    process_rules(all_answers, answer_rules)
