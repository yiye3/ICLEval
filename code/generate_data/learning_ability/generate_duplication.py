"""
本任务旨在测试模型调整识别文本重复内容的能力
粒度：
1. 字符级
2. 词汇级
3. 句子级
方式：
1. 单组重复查询或去除
2. 两组重复查询或去除
"""
import json
import random
random.seed(42)

def write_to_json(res, path):
    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

def get_characters():
    return "0 1 2 3 4 5 6 7 8 9 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z".split()

def get_words():
    with open("../../../data/origin_data/words.txt", "r", encoding="utf8") as f:
        res = f.read()
        lines = res.split("\n")[1:]
        words = [line.split("\t")[0] for line in lines]
    return words

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

def remove_repeated_content(
    candidates,
    uid,
    task_type,
    n_shot=5,
    task="remove_repeated_content"
    ):
    res = []
    for _ in range(n_shot + 1):
        # 3 ~ 6
        elements = random.sample(candidates, random.sample(range(3, 7), 1)[0])
        in_list = random.choices(elements, k=random.sample(range(10, 20), 1)[0])
        out_dict = {}
        for c in in_list:
            if c in out_dict:
                out_dict[c] += 1
            else:
                out_dict[c] = 1
        res.append({
            "input": ", ".join(in_list),
            "output": ", ".join(list(out_dict.keys()))
        })
    examples = ""
    for r in res[1:]:
        examples += "Input: {}\nOutput: {}\n\n".format(r["input"], r["output"])
    prompt = "Input: {}\nOutput:".format(res[0]["input"])
    return {
        "uid": uid,
        "task": task,
        "task_type": task_type,
        "examples": examples,
        "prompt": prompt,
        "label": res[0]["output"]
    }

def find_repeated_content(
    candidates,
    uid,
    task_type,
    n_shot=5,
    task="find_repeated_content"
    ):
    res = []
    for _ in range(n_shot + 1):
        # 3 ~ 6
        elements = random.sample(candidates, random.sample(range(3, 7), 1)[0])
    
        tag_sent = elements[0]
        in_list = elements + [tag_sent] * 2
        random.shuffle(in_list)

        res.append({
            "input": "\n".join(in_list),
            "output": tag_sent
        })
    examples = ""
    for r in res[1:]:
        examples += "Input: {}\nOutput: {}\n\n".format(r["input"], r["output"])
    prompt = "Input: {}\nOutput:".format(res[0]["input"])
    return {
        "uid": uid,
        "task": task,
        "task_type": task_type,
        "examples": examples,
        "prompt": prompt,
        "label": res[0]["output"]
    }


if __name__ == "__main__":
    characters = get_characters()
    words = get_words()
    sentences = get_sentences()

    res = []
    idx = 0

    for _ in range(100):
        res.append(remove_repeated_content(characters, idx, "character"))
        idx += 1

    for _ in range(100):
        res.append(remove_repeated_content(words, idx, "word"))
        idx += 1

    for _ in range(100):
        res.append(find_repeated_content(sentences, idx, "sentence"))
        idx += 1

    write_to_json(res, "../../../data/tasks_data/generate_duplication.json")