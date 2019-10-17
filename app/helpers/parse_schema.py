from collections import OrderedDict


class QuestionnaireSchema:
    def __init__(self, questionnaire_json):
        self.json = questionnaire_json
        self._parse_schema()

    @property
    def sections(self):
        return self._sections_by_id.values()

    @property
    def groups(self):
        return self._groups_by_id.values()

    @property
    def blocks(self):
        return self._blocks_by_id.values()

    @property
    def questions(self):
        return self._questions_by_id.values()

    @property
    def answers(self):
        return self._answers_by_id.values()

    def get_section(self, section_id):
        return self._sections_by_id.get(section_id)

    def get_group(self, group_id):
        return self._groups_by_id.get(group_id)

    def get_block(self, block_id):
        return self._blocks_by_id.get(block_id)

    def get_question(self, question_id):
        return self._questions_by_id.get(question_id)

    def get_answer(self, answer_id):
        return self._answers_by_id.get(answer_id)

    def _parse_schema(self):
        self._sections_by_id = self._get_sections_by_id()
        self._groups_by_id = get_nested_schema_objects(self._sections_by_id, 'groups')
        self._blocks_by_id = get_nested_schema_objects(self._groups_by_id, 'blocks')
        self._questions_by_id = get_nested_schema_objects(
            self._blocks_by_id, 'questions'
        )
        self._answers_by_id = get_nested_schema_objects(
            self._questions_by_id, 'answers'
        )

    def _get_sections_by_id(self):
        return OrderedDict(
            (section['id'], section) for section in self.json.get('sections', [])
        )


def get_nested_schema_objects(parent_object, list_key):
    nested_objects = OrderedDict()

    for parent_id, child_object in parent_object.items():
        for child_list_object in child_object.get(list_key, []):
            child_list_object['parent_id'] = parent_id
            nested_objects[child_list_object['id']] = child_list_object

    return nested_objects
