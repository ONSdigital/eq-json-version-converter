from json import load, dump

from app.helpers.parse_schema import QuestionnaireSchema
from app.rules import v2_to_v3


class Converter:
    def __call__(self, file_name):
        with open('schemas/to_convert/' + file_name, encoding='utf8') as schema_data:
            schema = load(schema_data)

        questionnaire_schema = QuestionnaireSchema(schema)
        v2_to_v3.root_conversions(questionnaire_schema.json)
        v2_to_v3.group_conversions(questionnaire_schema.groups)
        v2_to_v3.block_conversions(questionnaire_schema.blocks)
        v2_to_v3.routing_conversions(questionnaire_schema)
        v2_to_v3.question_conversions(questionnaire_schema.questions)
        v2_to_v3.answer_conversions(questionnaire_schema.answers)

        with open('schemas/converted/' + file_name, 'w') as json_file:
            dump(
                questionnaire_schema.json,
                json_file,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )
