"""
### markdown format
Table: Customers
| CustomerID | CustomerName | ContactName   | City       |
|------------|--------------|---------------|------------|
| 1          | John Smith   | John's Agent  | New York   |
| 2          | Lisa Johnson | Lisa's Agent  | Los Angeles|
| 3          | Mark Davis   | Mark's Agent  | Chicago    |


### Triple-tuple format
("John", "hasAge", 30)
("John", "inCity", "New York")

### XML format
<person>
  <name>John Smith</name>
  <age>30</age>
  <city>New York</city>
</person>

### CSV format
ID,Name,Age,City
1,John Smith,30,New York
2,Lisa Johnson,25,Los Angeles
3,Mark Davis,35,Chicago

### JSONL format
{"name": "John Smith", "age": 30, "city": "New York"}

### YAML format
person:
  name: John Smith
  age: 30
  city: New York

"""

from generate_format_conversion import *

def check_format(
    uid,
    target_format,
    all_formats,
    task_type,
    task="format_convert"
    ):

    res = []
    if task_type == "normal":
        infos = get_infos("person", 1)
        res.append({
            "input": format_dict[target_format](infos),
            "output": target_format
        })
        for cur_format in all_formats:
            infos = get_infos("person", 1)
            res.append({
                "input": format_dict[cur_format](infos),
                "output": cur_format
            })
       
    elif task_type == "transfer":
        infos = get_infos("company", 1)
        res.append({
            "input": format_dict[target_format](infos),
            "output": target_format
        })
        for cur_format in all_formats:
            infos = get_infos("person", 1)
            res.append({
                "input": format_dict[cur_format](infos),
                "output": cur_format
            })

    examples = ""
    for r in res[1:]:
        examples += "Input:\n{}\nOutput: {}\n\n".format(r["input"].strip(), r["output"].strip())
    prompt = "Input:\n{}\nOutput: ".format(res[0]["input"].strip())
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

    format_keys = list(format_dict.keys())
    for task_type in ["normal", "transfer"]:
        for _ in range(10):
            for i in format_keys:
                res.append(check_format(idx, i, format_keys, task_type))
                idx += 1

    write_to_json(res, "../../../data/tasks_data/classifier_format.json")
