def process_rules(items, rules):
    for item in items:
        for key in rules:
            rules[key](item)
