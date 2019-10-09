from app.helpers.rule_processor import process_rules
from app.rules.v2_to_v3.general_conversions import delete_parent_id, rename_content_key


def block_conversions(all_blocks):

    block_rules = {
        "update_guidance_content_key": update_single_block_questions_key,
        "delete_parent_id": delete_parent_id,
        "update_block_preview_content": update_block_preview_content,
        "update_block_primary_content": update_block_primary_content,
        "update_block_secondary_content": update_block_secondary_content,
        "update_block_interstitial_content": update_block_interstitial_content,
    }

    process_rules(all_blocks, block_rules)


def update_block_secondary_content(item):
    if "secondary_content" in item:
        for content in item["secondary_content"]:
            rename_content_key(content)

            if content.get("title"):
                del content["title"]


def update_block_primary_content(item):
    if "primary_content" in item:
        for content in item["primary_content"]:
            if not content.get("title"):
                content["title"] = "Title missing on migration"
            rename_content_key(content)

            if content.get("type"):
                del content["type"]


def update_block_preview_content(item):
    if "preview_content" in item:
        rename_content_key(item["preview_content"])


def update_single_block_questions_key(item):
    if "questions" in item:
        if len(item["questions"]) == 1:
            item["question"] = item["questions"][0]
            del item["questions"]


def update_block_interstitial_content(item):
    if "type" in item and item["type"] == "Interstitial" and item.get("description"):

        item["content"] = {
            "contents": [{"description": item["description"]}],
            "title": item["title"],
        }
        del item["description"]
        del item["title"]
