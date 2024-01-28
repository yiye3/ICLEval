"""
本任务旨在测试模型调整上下文文本次序的能力
粒度：
1. 字符级
2. 词汇级
3. 句子级
方式：
1. 顺序
2. 反序
3. 指定次序
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

def check_order(
    candidates,
    uid,
    task_type,
    n_shot=8,
    task="check_order"
    ):
    res = []
  
    for _ in range(n_shot + 1):
        is_reversed = random.sample([True, False], 1)[0]
        elements = random.sample(candidates, 5)
        if is_reversed:
            out_list = reversed(elements)
        else:
            out_list = elements
            
        res.append({
            "input": "\nString1: {}\nString2: {}".format(", ".join(elements), ", ".join(out_list)),
            "output": is_reversed
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

    for _ in range(50):
        res.append(check_order(characters, idx, "character"))
        idx += 1

    for _ in range(50):
        res.append(check_order(words, idx, "word"))
        idx += 1

    write_to_json(res, "../../../data/tasks_data/classifier_order.json")