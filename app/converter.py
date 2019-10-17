from json import load, dump

from app.rules.v2_to_v3.root_conversions import general_conversions
from app.rules.v2_to_v3.block_conversions import block_conversions
from app.rules.v2_to_v3.question_conversions import question_conversions
from app.rules.v2_to_v3.answer_conversions import answer_conversions
from app.rules.v2_to_v3.group_conversions import group_conversions
from app.rules.v2_to_v3.routing_rules import routing_conversions
from app.helpers.parse_schema import QuestionnaireSchema


class Converter:
    def __call__(self, file_name):
        with open('schemas/to_convert/' + file_name, encoding='utf8') as schema_data:
            schema = load(schema_data)

        questionnaire_schema = QuestionnaireSchema(schema)
        general_conversions(questionnaire_schema.json)
        group_conversions(questionnaire_schema.groups)
        block_conversions(questionnaire_schema.blocks)
        routing_conversions(questionnaire_schema)
        question_conversions(questionnaire_schema.questions)
        answer_conversions(questionnaire_schema.answers)

        with open('schemas/converted/' + file_name, 'w') as json_file:
            dump(
                questionnaire_schema.json,
                json_file,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )
