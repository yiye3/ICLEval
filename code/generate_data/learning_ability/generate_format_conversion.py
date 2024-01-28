"""
本任务旨在测试模型学习并使用标准化格式的能力，侧重测试模型使用格式的准确性。
子任务：
1. 无格式->有格式
2. 格式1->格式2
涉及的格式或文本有：
数值输出、选项输出、XML格式、YAML格式、CSV格式、Table-markdown格式、JSON格式以及三元组格式
"""
import json
import random
random.seed(42)

def write_to_json(res, path):
    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

def read_file(path):
    res = []
    domain = path.split("_")[-1].split(".jsonl")[0]
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            res.append((domain, json.loads(line)))
    return res


def get_markdown_table(infos):
    table_title = {}
    table_content = {}
    for info in infos:
        info_type, info_content = info
        keys = info_content.keys()
        if info_type not in table_title:
            title = "|Index|" + "|".join(keys) + "|\n"
            title += "|---|" + "---|" * (len(keys)) + "\n"
            table_title[info_type] = title
        if info_type not in table_content:
            table_content[info_type] = []
        
        content = "|{}".format(len(table_content[info_type]) + 1)
        for k in keys:
            content += "|{}".format(info_content[k])
        content += "|\n"
        table_content[info_type].append(content)

    res = ""
    for k in table_title.keys():
        res += table_title[k]
        for line in table_content[k]:
            res += line
        res += "\n"
    return res

def get_triple_tuple(infos):
    res = ""
    for info in infos:
        info_type, info_content = info
        for k, v in info_content.items():
            if k == "name":
                continue
            res += "({}, {}, {})\n".format(info_content["name"], k, v)
    return res

def get_XML(infos):
    res = ""
    for info in infos:
        info_type, info_content = info
        res += "<{}>\n".format(info_type)
        for k, v in info_content.items():
            res += "  <{}>{}</{}>\n".format(k, v, k)
        res += "</{}>\n".format(info_type)
    return res

def get_CSV(infos):
    table_title = {}
    table_content = {}
    for info in infos:
        info_type, info_content = info
        keys = info_content.keys()
        if info_type not in table_title:
            title = "Index," + ",".join(keys) + "\n"
            table_title[info_type] = title
        if info_type not in table_content:
            table_content[info_type] = []
        
        content = "{},".format(len(table_content[info_type]) + 1)
        for k in keys:
            content += "{},".format(info_content[k])
        content = content[:-1] + "\n"
        table_content[info_type].append(content)

    res = ""
    for k in table_title.keys():
        res += table_title[k]
        for line in table_content[k]:
            res += line
        res += "\n"
    return res

def get_jsonl(infos):
    res = ""
    for info in infos:
        info_type, info_content = info
        res += json.dumps(info_content, ensure_ascii=False) + "\n"
    return res

def get_YAML(infos):
    res = ""
    for info in infos:
        info_type, info_content = info
        res += "{}:\n".format(info_type)
        for k, v in info_content.items():
            res += "  {}: {}\n".format(k, v)
        res += "\n"
    return res

person_list = read_file("../../../data/origin_data/virtual_info_person.jsonl")
company_list = read_file("../../../data/origin_data/virtual_info_company.jsonl")
def get_infos(domain, num=5):
    if domain == "person":
        return random.sample(person_list, num)
    else:
        return random.sample(company_list, num)

format_dict = {
    "table": get_markdown_table,
    "csv": get_CSV,
    "tuple": get_triple_tuple,
    "xml": get_XML,
    "yaml": get_YAML,
    "jsonl": get_jsonl,
}

def format_convert(
    uid,
    srouce_format,
    target_format, 
    task_type,
    n_shot=3,
    task="format_convert"
    ):

    res = []
    if task_type == "single":
        for _ in range(n_shot + 1):
            infos = get_infos("person", 1)
            res.append({
                "input": format_dict[srouce_format](infos),
                "output": format_dict[target_format](infos)
            })
    elif task_type == "multi":
        for _ in range(n_shot + 1):
            infos = get_infos("person", random.sample(range(5), 1)[0] + 1)
            res.append({
                "input": format_dict[srouce_format](infos),
                "output": format_dict[target_format](infos)
            })
    elif task_type == "transfer":
        infos = get_infos("company", 1)
        res.append({
            "input": format_dict[srouce_format](infos),
            "output": format_dict[target_format](infos)
        })
        for _ in range(n_shot):
            infos = get_infos("person", 1)
            res.append({
                "input": format_dict[srouce_format](infos),
                "output": format_dict[target_format](infos)
            })
    elif task_type == "mix":
        for _ in range(n_shot + 1):
            infos = get_infos("person", random.sample(range(5), 1)[0] + 1)
            infos += get_infos("company", random.sample(range(5), 1)[0] + 1)
            res.append({
                "input": format_dict[srouce_format](infos),
                "output": format_dict[target_format](infos)
            })

    examples = ""
    for r in res[1:]:
        examples += "Input:\n{}\nOutput:\n{}\n\n".format(r["input"].strip(), r["output"].strip())
    prompt = "Input:\n{}\nOutput:\n".format(res[0]["input"].strip())
    return {
        "uid": uid,
        "task": task,
        "task_type": task_type,
        "examples": examples,
        "prompt": prompt,
        "label": res[0]["output"]
    }

if __name__ == "__main__":
    res = []
    idx = 0

    format_keys = format_dict.keys()
    for task_type in ["single", "multi", "transfer", "mix"]:
        for i in format_keys:
            for j in format_keys:
                if i != j:
                    res.append(format_convert(idx, i, j, task_type))
                    idx += 1

    write_to_json(res, "../../../data/tasks_data/generate_format_conversion.json")
