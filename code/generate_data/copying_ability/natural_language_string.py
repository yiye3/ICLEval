import json
import random
import hashlib
random.seed(42)

def write_to_json(res, path):
    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

def natural_language_string(uid, line):
    title, para, count = line["title"], line["content"], line["count"]

    sha256 = hashlib.sha256()
    sha256.update(str(title).encode("utf8"))
    placeholder = sha256.hexdigest()[-16:]

    pre_para, next_para = para.rsplit(title, 1)
    pre_para = pre_para.replace(title, placeholder)

    return {
        "uid": uid,
        "task": "natural_language",
        "task_type": "hash_string_copying",
        "content": pre_para,
        "prompt": placeholder[:8],
        "label": placeholder[8:],
        "ext_content": next_para,
        "count": count-1,
    }

if __name__ == "__main__":
    lines = []
    with open("../../../data/origin_data/wiki.jsonl", 'r', encoding='utf8') as f:
        for line in f:
            line = json.loads(line)
            lines.append(line)

    res = []
    for idx, line in enumerate(lines):
        res.append(natural_language_string(idx, line))

    write_to_json(res, "../../../data/tasks_data/copy_natural_language_string.json")
