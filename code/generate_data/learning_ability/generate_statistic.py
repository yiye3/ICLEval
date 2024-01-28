"""
本任务旨在测试模型从上下文中提取、汇总和分析有效信息的能力
子任务：
# 1. 个人信息提取，侧重点：关键信息提取
# 2. 布尔值判断，侧重点：信息逻辑分析
1. 长上下文集成 LongContextIntegration，侧重点: 信息提取和信息汇总
2. 导航，侧重点：信息分析与汇总 （需要一点点10以内计算）
"""
import json
import random
random.seed(42)

def write_to_json(res, path):
    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

########################### count ############################
## up down left right
def build_count_sample_easy():
    up_num = random.sample(range(5), 1)[0]
    down_num = random.sample(range(5), 1)[0]
 
    res = "up: {}, down: {}".format(up_num, down_num)

    action_list = ["up"] * up_num + ["down"] * down_num
    random.shuffle(action_list)
    return action_list, res

def build_count_sample_middle():
    up_num = random.sample(range(5), 1)[0]
    down_num = random.sample(range(5), 1)[0]
    left_num = random.sample(range(5), 1)[0]
    right_num = random.sample(range(5), 1)[0]
 
    res = "up: {}, down: {}, left: {}, right: {}".format(up_num, down_num, left_num, right_num)

    action_list = ["up"] * up_num + ["down"] * down_num + ["left"] * left_num + ["right"] * right_num
    random.shuffle(action_list)
    return action_list, res

########################### navigation ############################
## up down left right
def build_navigate_sample_easy():
    res = ""
    up_num = random.sample(range(5), 1)[0]
    down_num = random.sample(range(5), 1)[0]

    up_down = up_num - down_num
    if up_down >= 0:
        res += "up: {}".format(up_down)
    elif up_down < 0:
        res += "down: {}".format(-up_down)

    action_list = ["up"] * up_num + ["down"] * down_num
    random.shuffle(action_list)
    return action_list, res

def build_navigate_sample_middle():
    res = ""
    up_num = random.sample(range(5), 1)[0]
    down_num = random.sample(range(5), 1)[0]
    left_num = random.sample(range(5), 1)[0]
    right_num = random.sample(range(5), 1)[0]

    up_down = up_num - down_num
    left_right = left_num - right_num
    if up_down >= 0:
        res += "up: {}".format(up_down)
    elif up_down < 0:
        res += "down: {}".format(-up_down)
    res += ", "
    if left_right >= 0:
        res += "left: {}".format(left_right)
    elif left_right < 0:
        res += "right: {}".format(-left_right)

    action_list = ["up"] * up_num + ["down"] * down_num + ["left"] * left_num + ["right"] * right_num
    random.shuffle(action_list)
    return action_list, res

def count_or_navigation(
    uid,
    task_type,
    n_shot=8,
    task="count_or_navigation"
    ):
    res = []
    for _ in range(n_shot + 1):
        if task_type == "count-easy":
            action_list, label = build_count_sample_easy()

        elif task_type == "count-middle":
            action_list, label = build_count_sample_middle()

        elif task_type == "navigation-easy":
            action_list, label = build_navigate_sample_easy()

        elif task_type == "navigation-middle":
            action_list, label = build_navigate_sample_middle()
        
        res.append({
            "input": action_list,
            "output": label
        })

    examples = ""
    for r in res[1:]:
        examples += "Input: {}\nOutput: {}\n\n".format(", ".join(r["input"]), r["output"])
    prompt = "Input: {}\nOutput: ".format(", ".join(res[0]["input"]))
    return {
        "uid": uid,
        "task": task,
        "task_type": task_type,
        "examples": examples,
        "prompt": prompt,
        "label": res[0]["output"]
    }

########################### LongContextIntegration ############################
import numpy as np
import scipy

colors = [
    "green", "red", "blue", "grey", "yellow", "pink", "magenta", "chartreuse", "cyan", "alabaster", "aqua", "azure", "beige", "brown", "maroon", "bronze", "carmine", "carnelian", "copper", "chestnut", "dandelion", "violet", "tan", "taupe", "fuchsia", "viridian", "lavender", "periwinkle", "mauve", "purple", "orange", "violet", "silver", "turquoise", "taupe", "umber",
]
animals = [
    "raccoon", "cow", "pig", "goose", "dolphin", "albatross", "koala", "octopus", "squirrel", "rabbit", "alpaca", "ant", "anteater", "baboon", "gorilla", "bonobo", "sloth", "bat", "bear", "bison", "buffalo", "bobcat", "cougar", "lion", "dog", "cat", "ferret", "cobra", "coyote", "zebra", "gnu", "ocelot", "owl", "penguin", "crab", "lobster", "yak", "whale", "walrus", "vulture", "mantis", "duck", "seagull", "cuttlefish", "mollusk", "seahorse", "jellyfish", "tarantula", "fly", "goose", "horse", "mule", "narwhale", "orca", "humpback", "human", "macaque", "hydra", "emu", "deer", "reindeer", "wolf", "coyote", "snail", "flea", "bee", "ladybug", "termite", "shrimp",
]

public_content = "Input:\nblue_mantis_362 and taupe_bonobo_396 are friends.\nQuery: Who are the frinds of lavender_lion_728?\nOutput: None\n\nInput:\nbeige_bat_678 and yellow_ladybug_906 are friends.\ndandelion_dog_108 and maroon_cow_234 are friends.\nQuery: Who are the frinds of dandelion_dog_108?\nOutput: maroon_cow_234\n\nInput:\nfuchsia_bear_15 and turquoise_narwhale_975 are friends.\nbrown_duck_771 and fuchsia_bear_15 are friends.\nfuchsia_bear_15 and chartreuse_pig_243 are friends.\nbrown_duck_771 and turquoise_narwhale_975 are friends.\nQuery: Who are the frinds of chartreuse_pig_243?\nOutput: fuchsia_bear_15\n\nInput:\ndandelion_coyote_628 and grey_bear_225 are friends.\ndandelion_coyote_628 and purple_bee_959 are friends.\ndandelion_coyote_628 and blue_cougar_546 are friends.\nblue_cougar_546 and green_bonobo_963 are friends.\ndandelion_coyote_628 and maroon_seahorse_996 are friends.\ngreen_bonobo_963 and grey_bear_225 are friends.\nblue_cougar_546 and grey_bear_225 are friends.\nblue_cougar_546 and purple_bee_959 are friends.\npurple_bee_959 and maroon_seahorse_996 are friends.\ngrey_bear_225 and maroon_seahorse_996 are friends.\nQuery: Who are the frinds of maroon_seahorse_996?\nOutput: dandelion_coyote_628, purple_bee_959, grey_bear_225\n\nInput:\norange_ocelot_187 and purple_jellyfish_432 are friends.\ntaupe_hydra_858 and chestnut_goose_453 are friends.\nQuery: Who are the frinds of taupe_hydra_858?\nOutput: chestnut_goose_453\n\n"

def generate_individual_names(num):
    """Return a list of num unique names. """

    # we're not using more than half of the possible names
    assert num < 1000 * len(animals) * len(colors) * 0.5

    names = []
    while len(names) < num:
        new_name = f"{np.random.choice(colors)}_{np.random.choice(animals)}_{np.random.randint(1, 1000)}"
        if not new_name in names:
            names.append(new_name)
    return names

def generate_relationship_matrix(num_individuals, num_connections):
    """
    Generate a num_individuals by num_individuals sparse matrix, with ones for all pairs of
    individuals that are friends with each other, and ones along the diagonal.
    """

    # populate off diagonals, to make sure the network is all-to-all-connected
    o = np.ones((num_individuals,))
    # C = scipy.sparse.diags(
    #     (o[[0]], o[:-1], o, o[:-1], o[[0]]),
    #     [-num_individuals + 1, -1, 0, 1, num_individuals - 1],
    #     format="lil",
    # )
    C = scipy.sparse.diags(o, 0, format="lil")

    n = 0
    while n < num_connections:
        i = np.random.randint(num_individuals)
        j = np.random.randint(num_individuals)
        if C[i, j] == 0:
            C[i, j] = 1
            C[j, i] = 1
            n += 1

    return C

def relationships_to_string(names, C):
    """Turn the relationship matrix into a string listing all the friendships."""
    s = []
    for i, j, v in zip(*scipy.sparse.find(C)):
        # upper triangular entries only
        if j > i:
            s.append(f"{names[i]} and {names[j]} are friends.")
    s = np.random.permutation(s)
    return "\n".join(s)

def get_sample(idx):
    num = random.sample(range(5,10), 1)[0]
    num_connections = random.sample(range(num, (num-1) * num // 2), 1)[0]
    names = generate_individual_names(num)
    C = generate_relationship_matrix(num, num_connections)
    in_text =  relationships_to_string(names, C)
    query_name_id = random.sample(range(len(names)), 1)[0]
    query = "Who are the frinds of {}?".format(names[query_name_id])
    answers = []
    for i in range(len(names)):
        if query_name_id != i and C[query_name_id, i] == 1.0:
            answers.append(names[i])
    label = ", ".join(answers) if answers else "None"
    prompt = "Input:\n{}\nQuery: {}\nOutput:".format(in_text, query)

    return {
        "uid": idx,
        "task": "generate_statistic",
        "exmaples": public_content,
        "prompt": prompt,
        "label": label,
        "task_type": "relation"
    }

if __name__ == "__main__":
    ### count and navigation
    res = []
    idx = 0

    for _ in range(30):
        res.append(count_or_navigation(idx, "count-easy"))
        idx += 1
    for _ in range(30):
        res.append(count_or_navigation(idx, "count-middle"))
        idx += 1
    for _ in range(30):
        res.append(count_or_navigation(idx, "navigation-easy"))
        idx += 1
    for _ in range(30):
        res.append(count_or_navigation(idx, "navigation-middle"))
        idx += 1

    write_to_json(res, "../../../data/tasks_data/generate_count_or_navigation.json")


    res = []
    idx = 0

    for _ in range(100):
        res.append(get_sample(idx))
        idx += 1

    write_to_json(res, "../../../data/tasks_data/generate_relation_analysis.json")