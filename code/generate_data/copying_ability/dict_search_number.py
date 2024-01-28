import json
import hashlib
import random
random.seed(42)

def write_to_json(res, path):
    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

opt_dict = {
    "+": "☀",
    "-": "☽",
    "*": "⚝",
    "=": "⛱"
}

def get_similar_number(number):
    number = [x for x in str(number)]
    pos_id = random.sample(range(len(number)), 1)[0]
    number[pos_id] = str(random.sample(range(10), 1)[0])
    return int("".join(number))

def load_one_sample(sim_num=10, mode="long"):
    if mode == "short":
        length = 11
        opt = ["+", "+", "+", "+", "-", "-", "-", "-", "*", "*"]
    else:
        length = 23
        opt = ["+", "+", "+", "+", "+", "+", "+", "+", "+", "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "*", "*"]
    
    meta_list = random.sample(random.sample(range(100, 1000), 100) + list(range(1, 100)), length)
    random.shuffle(opt)
    opt.append("=")

    samples = []

    sample = ""
    for x, y in zip(meta_list, opt):
        sample += str(x) + " " + y + " "
    samples.append(sample)

    for _ in range(sim_num-1):
        new_list = [x for x in meta_list]
        replace_num = random.sample(range(1, 3), 1)[0]
        replace_pos = random.sample(range(length), replace_num)
        for pos in replace_pos:
            new_list[pos] = get_similar_number(meta_list[pos])
        
        sample = ""
        for x, y in zip(new_list, opt):
            sample += str(x) + " " + y + " "
        samples.append(sample)

    res = []
    for sample in samples:
        ans = eval(sample[:-2])
        for k, v in opt_dict.items():
            sample = sample.replace(k, v)
        res.append({
            "prompt": sample,
            "label": str(ans),
        })
    
    return res

def dict_search_number(uid, task_type):
    if task_type == "number-all_similar":
        res = load_one_sample(10)
        target = random.sample(res, 1)[0]

    elif task_type == "number-half_similar":
        res = load_one_sample(5)
        target = random.sample(res, 1)[0]
        for _ in range(5):
            res += load_one_sample(1)
        random.shuffle(res)

    elif task_type == "number-non_similar":
        res = []
        for _ in range(10):
            res += load_one_sample(1)
        target = random.sample(res, 1)[0]

    examples = ""
    for r in res:
        examples += r["prompt"] + r["label"] + "\n"

    return {
        "uid": uid,
        "task": "dict_search",
        "task_type": task_type,
        "examples": examples,
        "prompt":target["prompt"].rstrip(),
        "label": target["label"],
    }

if __name__ == "__main__":
    res = []
    idx = 0

    for _ in range(30):
        res.append(dict_search_number(idx, "number-all_similar"))
        idx += 1
    
    for _ in range(30):
        res.append(dict_search_number(idx, "number-half_similar"))
        idx += 1

    for _ in range(30):
        res.append(dict_search_number(idx, "number-non_similar"))
        idx += 1

    write_to_json(res, "../../../data/tasks_data/copy_dict_search_number.json")

