# task files
from . import copy_task
from . import learning_task


########################################
# All tasks
########################################

TASK_REGISTRY = {
    "dict_search_string": copy_task.DictSearchCopying,
    "dict_search_number": copy_task.NumberStringCopying,
    "natural_language_string": copy_task.NaturalLanguageCopying,

    "check_order": learning_task.CheckOrder,
    "character_order": learning_task.GenerateCharacerOrder,
    "word_order": learning_task.GenerateWordOrder,
    "sentence_order": learning_task.GenerateSentenceOrder,

    "check_dedup": learning_task.CheckDuplication,
    "character_dedup": learning_task.GenerateCharacterDuplication,
    "word_dedup": learning_task.GenerateWordDuplication,
    "sentence_dedup": learning_task.GenerateSentenceDuplication,
    
    "relation_analysis": learning_task.RelationAnalysis,
    "navigation_and_count": learning_task.CountNavigationAnalysis,

    "check_format": learning_task.CheckFormat,
    "output_format": learning_task.GenerateOutputFormat,
    "format_convert": learning_task.GenerateFormatConversion,

    "list_number": learning_task.ListNumber,


    # supplementary_data
    # "check_format_2shot": learning_task.CheckFormat_12example,
    # "check_format_4shot": learning_task.CheckFormat_24example,
    # "navigation_and_count_4shot": learning_task.CountNavigationAnalysis_4shot,
    # "navigation_and_count_16shot": learning_task.CountNavigationAnalysis_16shot,

    # "check_format_prompt1": learning_task.CheckFormat_prompt1,
    # "check_format_prompt2": learning_task.CheckFormat_prompt2,
    # "check_format_prompt3": learning_task.CheckFormat_prompt3,
    # "check_format_prompt4": learning_task.CheckFormat_prompt4,

    # "check_format_prompt1_4shot": learning_task.CheckFormat_prompt1_24example,
    # "check_format_prompt2_4shot": learning_task.CheckFormat_prompt2_24example,
    # "check_format_prompt3_4shot": learning_task.CheckFormat_prompt3_24example,
    # "check_format_prompt4_4shot": learning_task.CheckFormat_prompt4_24example,

}

ALL_TASKS = TASK_REGISTRY.keys()
