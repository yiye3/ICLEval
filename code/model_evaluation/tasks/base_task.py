import json
import re

class Base:
    def __init__(self, path) -> None:
        self.data_path = path
        self.data = self.load_data()

        self.batch_size = 1
        self.end_token = None

        self.logs = []
        self.acc_dict = {}
        self.type_num = {}

        self.split_token="\nInput:"
    
    def load_data(self):
        with open(self.data_path, 'r', encoding='utf8') as f:
            res = json.loads(f.read()) 
        return res
    
    def filter_data_by_task_type(self, tag):
        new_data = []
        for item in self.data:
            if item["task_type"] == tag:
                new_data.append(item)
        return new_data

    def get_config(self):
        return {
            "batch_size": self.batch_size,
            "max_gen_len": self.max_gen_len,
            "end_token": self.end_token,
            "is_sample": False,
        }
    
    def make_prompt(self, data_sample):
        if "content" in data_sample:
            return data_sample["content"] + data_sample["prompt"]
        return data_sample["examples"] + data_sample["prompt"]
    
    def construct_requests(self):
        req_gen = []
        for data_sample in self.data:
            prompt = self.make_prompt(data_sample)
            req_gen.append({
                "context": prompt,
            })
            # logs 
            self.logs.append({
                "uid": data_sample["uid"],
                "prompt": prompt,
                "label": data_sample["label"],
                "task": data_sample["task"],
                "task_type": data_sample["task_type"],
            })
            # acc
            tag = data_sample["task"] + "_" + data_sample["task_type"]
            if tag not in self.acc_dict:
                self.acc_dict[tag] = 0.0
                self.type_num[tag] = 1
            else:
                self.type_num[tag] += 1
        return req_gen
    
    def check(self, res, label):
        pred = res.strip().split(self.split_token)[0]
        if pred.strip() == label.strip():
            return True, pred
        else:
            return False, pred

    def process_results(self, results):
        assert len(results) == len(self.logs)
        for res, log in zip(results, self.logs):
            log['response'] = res
            # pred
            is_right, pred = self.check(res, log["label"])

            # acc
            if is_right:
                tag = log["task"] + "_" + log["task_type"]
                self.acc_dict[tag] += 1.0

            # logs 
            log['pred'] = pred
            log['is_right'] = is_right

        self.acc_dict = {key: value / self.type_num[key] for key, value in self.acc_dict.items()}
        return self.acc_dict, self.logs