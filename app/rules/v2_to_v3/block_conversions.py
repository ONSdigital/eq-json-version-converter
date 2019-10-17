from app.helpers.rule_processor import process_rules
from app.rules.v2_to_v3.general_conversions import delete_parent_id, rename_content_key


def block_conversions(all_blocks):

    block_rules = {
        'update_guidance_content_key': update_single_block_questions_key,
        'delete_parent_id': delete_parent_id,
        'update_block_preview_content': update_block_preview_content,
        'update_block_primary_content': update_block_primary_content,
        'update_block_secondary_content': update_block_secondary_content,
        'update_block_interstitial_content': update_block_interstitial_content,
    }

    process_rules(all_blocks, block_rules)


def update_block_secondary_content(block):
    for content in block.get('secondary_content', []):
        rename_content_key(content)

        if content.get('title'):
            del content['title']


def update_block_primary_content(block):
    for content in block.get('primary_content', []):
        if not content.get('title'):
            content['title'] = 'Title missing on migration'
        rename_content_key(content)

        if content.get('type'):
            del content['type']


def update_block_preview_content(block):
    if 'preview_content' in block:
        rename_content_key(block['preview_content'])
        for question in block.get('preview_content').get('questions', []):
            rename_content_key(question)


def update_single_block_questions_key(block):
    if 'questions' in block:
        if len(block['questions']) == 1:
            block['question'] = block['questions'][0]
            del block['questions']


def update_block_interstitial_content(block):
    if 'type' in block and block['type'] == 'Interstitial' and block.get('description'):

        block['content'] = {
            'contents': [{'description': block['description']}],
            'title': block['title'],
        }
        del block['description']
        del block['title']
