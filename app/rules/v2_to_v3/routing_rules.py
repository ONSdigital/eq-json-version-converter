def routing_conversions(schema):

    all_blocks = schema.blocks

    for block in all_blocks:
        update_radio_question_condition_in_routing_rules(block, schema)


def update_radio_question_condition_in_routing_rules(item, schema):

    for rule in item.get('routing_rules', []):
        for when in rule.get('goto').get('when', []):
            answer = schema.get_answer(when.get('id'))
            if (
                answer
                and answer.get('type') == 'Radio'
                and when.get('condition') == 'contains any'
            ):
                when['condition'] = 'equals any'
