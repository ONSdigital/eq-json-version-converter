from json import load, dump

from app.rules.v2_to_v3.root_conversions import general_conversions
from app.rules.v2_to_v3.block_conversions import block_conversions
from app.rules.v2_to_v3.question_conversions import question_conversions
from app.rules.v2_to_v3.answer_conversions import answer_conversions
from app.rules.v2_to_v3.group_conversions import group_conversions
from app.rules.v2_to_v3.routing_rules import routing_conversions
from app.helpers.parse_schema import QuestionnaireSchema


class Converter:
    def __init__(self, file_name):
        with open('schemas/to_convert/' + file_name, encoding='utf8') as schema_data:
            self.schema = load(schema_data)
            self.file_name = file_name

    def save_json(self):
        with open('schemas/converted/' + self.file_name, 'w') as json_file:
            dump(
                self.schema, json_file, sort_keys=True, indent=4, separators=(',', ': ')
            )

    def convert_schema(self):

        schema = QuestionnaireSchema(self.schema)

        general_conversions(schema.json)
        group_conversions(schema.groups)
        block_conversions(schema.blocks)
        routing_conversions(schema)
        question_conversions(schema.questions)
        answer_conversions(schema.answers)
