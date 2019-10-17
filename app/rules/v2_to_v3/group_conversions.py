from app.helpers.rule_processor import process_rules
from app.rules.v2_to_v3.general_conversions import delete_parent_id


def group_conversions(all_groups):
    group_rules = {'delete_parent_id': delete_parent_id}
    process_rules(all_groups, group_rules)
