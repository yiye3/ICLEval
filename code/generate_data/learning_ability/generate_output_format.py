import re
import json
import random
random.seed(42)

import datasets

def write_to_json(res, path):
    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

def load_one_sample(
    tag, 
    xformat, 
    uid,
    task="output_format"
    ):
    if tag == "gsm8k":
        pos_ids = random.sample(range(len(gsm8k)), 6)
        samples = [gsm8k[i] for i in pos_ids]
        content = ""
        for sample in samples[1:]:
            pre_ans,  next_ans = sample["answer"].split("\n#### ")
            calculate = re.findall(r'<<.*>>', pre_ans)
            for item in calculate:
                pre_ans = pre_ans.replace(item, "")
            answer = pre_ans + xformat.replace("value", next_ans)
            content += "Question: {}\nResponse: {}\n\n".format(sample["question"], answer)
        prompt = "Question: {}\nResponse: ".format(samples[0]["question"])
        ans_content = samples[0]["answer"]
        return {
            "uid": uid,
            "task": task,
            "task_type": "output_format_01",
            "examples": content,
            "prompt": prompt,
            "label": xformat,
            "ans_content": ans_content,
        }
    elif tag == "aqua":
        pos_ids = random.sample(range(len(aqua)), 6)
        samples = [aqua[i] for i in pos_ids]
        content = ""
        for sample in samples[1:]:
            if "key" in xformat:
                answer = xformat.replace("key", sample["correct"])
                xtype = "output_format_02"
            elif "value" in xformat:
                value = sample["options"].split(sample["correct"]+")")[1]
                value = value.split(",")[0]
                answer = xformat.replace("value", value)
                xtype = "output_format_03"

            content += "Question: {}\nOptions: {}\nAnswer: {}\n\n".format(
                sample["question"], sample["options"], answer)
            
        prompt = "Question: {}\nOptions: {}\nAnswer:".format(samples[0]["question"], samples[0]["options"])
        ans_content = samples[0]["correct"]
        return {
            "uid": uid,
            "task": task,
            "task_type": xtype,
            "examples": content,
            "prompt": prompt,
            "label": xformat,
            "ans_content": ans_content,
        }


if __name__ == "__main__":
    res = []
    idx = 0

    format_series_01 = ["\nSo the answer is value", "\nOutput: value", "\nThe final answer is ⚝⚝ value ⚝⚝", "\n<answer> value </answer>", "\n⛱⛱⛱ value"]
    format_series_02 = ["<key>", "⚝⚝ key ⚝⚝", "(key)", "The Option is value", "<string> value </string>"]

    gsm8k = datasets.load_from_disk("../../../data/origin_data/gsm8k_test")
    aqua = datasets.load_from_disk("../../../data/origin_data/aqua_test")
    
    # 01
    for format_01 in format_series_01:
        for _ in range(10):
            tmp = load_one_sample("gsm8k", format_01, idx)
            res.append(tmp)
            idx += 1

    # 02
    for format_02 in format_series_02:
        for _ in range(10):
            tmp = load_one_sample("aqua", format_02, idx)
            res.append(tmp)
            idx += 1

    write_to_json(res, "../../../data/tasks_data/generate_output_format.json")
