"""
本任务旨在测试模型学习新的规律的能力（防止语言能力的干扰，仅通过示例来学习）。
子任务：
1. 对列表元素的处理
2. 抽象推理
"""
import glob
import json
import random
random.seed(42)

def write_to_json(res, path):
    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    res = []
    idx = 0

    path = "../../../data/origin_data/list_functions"
    for sub_path in glob.glob(r"{}/c*/task.json".format(path)):
        with open(sub_path, 'r', encoding='utf8') as f:
            sub_data = json.loads(f.read())
            # used_examples = random.sample(sub_data["examples"][:-1], 5)
            used_examples = sub_data["examples"][:-1]

            examples = ""
            for r in used_examples:
                examples += "Input: {}\nOutput: {}\n\n".format(r["input"], r["target"])
            prompt = "Input: {}\nOutput:".format(sub_data["examples"][-1]["input"])
            label = sub_data["examples"][-1]["target"]
            res.append({
                "uid": idx,
                "task": "list_number",
                "task_type": "list_number",
                "examples": examples,
                "prompt": prompt,
                "label": label,
            })
            idx += 1

    write_to_json(res, "../../../data/tasks_data/generate_list_number.json")