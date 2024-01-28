import json
import random
import hashlib
random.seed(42)

def write_to_json(res, path):
    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

def get_sentences():
    sentences = []
    with open("../../../data/origin_data/wiki.jsonl", 'r', encoding='utf8') as f:
        for item in f:
            item = json.loads(item)
            title, paras, count = item["title"], item["content"], item["count"]
            paras = paras.split("\n")
            for para in paras:
                lines = para.split(". ")
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if (len(line.split(" ")) < 5) or (len(line.split(" ")) > 30):
                        continue
                    if line[-1] != ".":
                        line += "."
                    sentences.append(line)
    return sentences

def dict_search_string(uid, sentences):
    new_subl = random.sample(sentences, 20)

    res_dict = {}
    for subl in new_subl:
        sha256 = hashlib.sha256()
        sha256.update(str(subl).encode("utf8"))
        key = sha256.hexdigest()[:6]
        res_dict[key] = subl
    
    search_key = random.sample(list(res_dict.keys()), 1)[0]
    search_value = res_dict[search_key]
    
    return {
        "uid": uid,
        "task": "dict_search",
        "task_type": "hash_string",
        "dict": res_dict,
        "prompt":search_key,
        "label": search_value,
    }

if __name__ == "__main__":
    sentences = get_sentences()

    res = []
    idx = 0

    for _ in range(100):
        res.append(dict_search_string(idx, sentences))
        idx += 1

    write_to_json(res, "../../../data/tasks_data/copy_dict_search_string.json")
