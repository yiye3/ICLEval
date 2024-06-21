from .base_task import Base
import re
###############################            Order Probelm         ##########################################  

class CheckOrder(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/classifier_order.json")
        self.max_gen_len = 5
        self.split_token="\n"
    
    def check(self, res, label):
        pred = res.strip().split(self.split_token)[0]
        is_ture = pred.strip().lower() == "true"
        if is_ture == label:
            return True, pred
        else:
            return False, pred

class GenerateCharacerOrder(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_order.json")
        self.max_gen_len = 50
        self.split_token="\n"

        self.data = self.filter_data_by_task_type("character")
        
class GenerateWordOrder(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_order.json")
        self.max_gen_len = 50
        self.split_token="\n"

        self.data = self.filter_data_by_task_type("word")

class GenerateSentenceOrder(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_order.json")
        self.max_gen_len = 256

        self.data = self.filter_data_by_task_type("sentence")


###############################            Duplication Probelm         ##########################################   

class CheckDuplication(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/classifier_duplication.json")
        self.max_gen_len = 5
        self.split_token="\n"
    
    def check(self, res, label):
        pred = res.strip().split(self.split_token)[0]
        is_ture = pred.strip().lower() == "true"
        if is_ture == label:
            return True, pred
        else:
            return False, pred

class GenerateCharacterDuplication(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_duplication.json")
        self.max_gen_len = 30
        self.split_token="\n"

        self.data = self.filter_data_by_task_type("character")


class GenerateWordDuplication(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_duplication.json")
        self.max_gen_len = 30
        self.split_token="\n"

        self.data = self.filter_data_by_task_type("word")

class GenerateSentenceDuplication(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_duplication.json")
        self.max_gen_len = 60
        self.split_token="\n"

        self.data = self.filter_data_by_task_type("sentence")

###############################            Statistic Problem        ##########################################
class RelationAnalysis(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_relation_analysis.json")
        self.max_gen_len = 60

    def check(self, res, label):
        pred = res.strip().split("\nInput:")[0]
        pred = pred.strip().split(", ")
        label = label.strip().split(", ")
        if set(pred) == set(label):
            return True, ", ".join(pred)
        else:
            return False, ", ".join(pred)
        
class CountNavigationAnalysis(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_count_or_navigation.json")
        self.max_gen_len = 30
        self.split_token="\n"

class CountNavigationAnalysis_4shot(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/generate_count_or_navigation_4shot.json")
        self.max_gen_len = 30
        self.split_token="\n"

class CountNavigationAnalysis_16shot(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/generate_count_or_navigation_16shot.json")
        self.max_gen_len = 30
        self.split_token="\n"

###############################          Format Problem       ##########################################

class CheckFormat(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/classifier_format.json")
        self.max_gen_len = 5
        self.split_token="\n"

class CheckFormat_12example(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/classifier_format_2shot.json")
        self.max_gen_len = 5
        self.split_token="\n"

class CheckFormat_24example(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/classifier_format_4shot.json")
        self.max_gen_len = 5
        self.split_token="\n"

class CheckFormat_prompt1(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/classifier_format_prompt_1.json")
        self.max_gen_len = 5
        self.split_token="\n"
class CheckFormat_prompt2(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/classifier_format_prompt_2.json")
        self.max_gen_len = 5
        self.split_token="\n"
class CheckFormat_prompt3(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/classifier_format_prompt_3.json")
        self.max_gen_len = 5
        self.split_token="\n"
class CheckFormat_prompt4(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/classifier_format_prompt_4.json")
        self.max_gen_len = 5
        self.split_token="\n"

class CheckFormat_prompt1_24example(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/classifier_format_prompt_1_4shot.json")
        self.max_gen_len = 5
        self.split_token="\n"
class CheckFormat_prompt2_24example(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/classifier_format_prompt_2_4shot.json")
        self.max_gen_len = 5
        self.split_token="\n"
class CheckFormat_prompt3_24example(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/classifier_format_prompt_3_4shot.json")
        self.max_gen_len = 5
        self.split_token="\n"
class CheckFormat_prompt4_24example(Base):
    def __init__(self) -> None:
        super().__init__("../../supplementary_data/classifier_format_prompt_4_4shot.json")
        self.max_gen_len = 5
        self.split_token="\n"

class GenerateOutputFormat(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_output_format.json")
        self.max_gen_len = 196

    def process_results(self, results):
        assert len(results) == len(self.logs)

        for res, log in zip(results, self.logs):
            log['response'] = res
            # pred
            pred = res.strip().split("\nQuestion:")[0]
            
            is_right = False
            tag = log["task"] + "_" + log["task_type"]
            # acc
            if log["task_type"] == "cot-answer":
                pred = pred.replace(",", "")
                xformat = log['label'].replace("value", "(-?\$?\d+)")
                ans = re.findall(r'{}'.format(xformat), pred)
                if len(ans) == 1:
                    is_right = True
                    self.acc_dict[tag] += 1.0
            elif log["task_type"] == "choice-key":
                xformat = log['label'].replace("key", "([A-E])")
                xformat 
                ans = re.findall(r'{}'.format(xformat), pred)
                if len(ans) == 1:
                    is_right = True
                    self.acc_dict[tag] += 1.0
            elif log["task_type"] == "choice-value":
                xformat = log['label'].replace("value", "(.*)")
                ans = re.findall(r'{}'.format(xformat), pred)
                candidates = log["prompt"].split("\nOptions:")[-1].split("\n")[0]
                candidates = [x.split(")", 1)[-1].strip() for x in candidates.split(",")]
                if len(ans) == 1 and ans[0] in candidates:
                    is_right = True
                    self.acc_dict[tag] += 1.0

            # logs 
            log['pred'] = pred
            log['is_right'] = is_right

        self.acc_dict = {key: value / self.type_num[key] for key, value in self.acc_dict.items()}
        return self.acc_dict, self.logs
    
class GenerateFormatConversion(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_format_conversion.json")
        self.max_gen_len = 256


###############################          List Number      ##########################################
class ListNumber(Base):
    def __init__(self) -> None:
        super().__init__("../../data/tasks_data/generate_list_number.json")
        self.max_gen_len = 50
        self.split_token="\n"