from .base_task import Base

class NaturalLanguageCopying(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/copy_natural_language_string.json")
        self.max_gen_len = 12

    def check(self, res, label):
        pred = res.strip()
        end_tokens = [" ", ",", ".", "!", ":", ")", "\"", "\'", "\n"]
        for tok in end_tokens:
            pred = pred.split(tok)[0]
        if len(pred) == 9 and pred[-1] == 's':
            pred = pred[:-1]
        
        if pred == label:
            return True, pred
        else:
            return False, pred

class DictSearchCopying(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/copy_dict_search_string.json")
        self.max_gen_len = 75
        self.split_token="\n"
    
    def make_prompt(self, data_sample):
        prompt = ""
        for k, v in data_sample["dict"].items():
            prompt += "{} : {}\n".format(k, v)
        prompt += "{} :".format(data_sample["prompt"])
        return prompt


class NumberStringCopying(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/copy_dict_search_number.json")
        self.max_gen_len = 10
        self.split_token="\n"

    def make_prompt(self, data_sample):
        prompt = ""
        for k, v in data_sample["dict"].items():
            prompt += "{} : {}\n".format(k, v)
        prompt += "{} :".format(data_sample["prompt"])
        return prompt
