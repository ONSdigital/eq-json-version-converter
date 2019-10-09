def delete_parent_id(item):
    if "parent_id" in item:
        del item["parent_id"]


def rename_content_key(content):
    if content.get("content"):
        content["contents"] = content["content"]
        del content["content"]


def update_guidance_content_key(item):
    if "guidance" in item:
        rename_content_key(item["guidance"])
