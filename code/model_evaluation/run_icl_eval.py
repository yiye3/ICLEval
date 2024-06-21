import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    LlamaTokenizer,
    AutoModel,
)
from modeling_phi.modeling_mixformer_sequential import MixFormerSequentialForCausalLM
import tasks
from tqdm import tqdm
import json
import os

def _load_tokenizer(tok_path, name):
    tokenizer = AutoTokenizer.from_pretrained(tok_path, trust_remote_code=True)
    print("testing tokenizer...")
    print("hello, world: ", tokenizer.encode("hello\n\nhello"))
    print("bos_token_id: {}, eos_token_id: {}, pad_token_id: {}".format(
        tokenizer.bos_token_id, tokenizer.eos_token_id, tokenizer.pad_token_id))
    
    if "chatglm" in name.lower() or "qwen" in name.lower():
        pass
    else:
        if not tokenizer.pad_token_id:
            tokenizer.pad_token_id = 0
            print("setting pad_token_id to {}, now pad_token is {}".format(0, tokenizer.decode(0)))
        if not tokenizer.bos_token_id:
            tokenizer.bos_token_id = 1
            print("setting bos_token_id to {}, now bos_token is {}".format(1, tokenizer.decode(1)))
        if not tokenizer.eos_token_id:
            tokenizer.eos_token_id = 2
            print("setting eos_token_id to {}, now eos_token is {}".format(2, tokenizer.decode(2)))
    tokenizer.padding_side = 'left'
    print("setting padding_side to left")
    print("vocab length: %d"%len(tokenizer))
    return tokenizer

def load_model_and_tokenizer(model_name):
    device = torch.device("cuda:0")
    model_path = "your_path/%s" % model_name

    print("loading model and tokenizer from <%s>"%model_path)
    # load tokenizer
    tokenizer = _load_tokenizer(model_path, model_name)
    print(model_name)

    # load model
    if "72b" in model_name.lower() or "65b" in model_name.lower() or "70b" in model_name.lower():
        from accelerate import init_empty_weights, load_checkpoint_and_dispatch
        with init_empty_weights():
            model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
        model.tie_weights()
        model = load_checkpoint_and_dispatch(
            model, 
            model_path, 
            device_map="auto", 
            no_split_module_classes=["LlamaDecoderLayer"], 
            dtype=torch.float16)
        model.eval()
    elif "phi" in model_name.lower():
        model = MixFormerSequentialForCausalLM.from_pretrained(model_path, trust_remote_code=True)
        model.eval().half().to(device)
    elif "chatglm" in model_name.lower():
        model = AutoModel.from_pretrained(model_path, trust_remote_code=True)
        model.eval().half().to(device)    
    elif "baichuan" in model_name.lower() or "qwen" in model_name.lower():
        model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
        model.eval().bfloat16().to(device)
    elif "8x7B" in model_name:
        model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
        model.eval().half()
    else:
        model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
        model.eval().half().to(device)

    print("loading model and tokenizer success...")
    return model, tokenizer 


@torch.no_grad()
def greedy_until(requests, model, tokenizer, config, disable_tqdm=False, model_max_length=2048):
    """
    requests -> new_reqs -> chunk, cache_res -> results
    step 0: unpack config
    step 1: sort, from long to short
    step 2: split, chunks
    step 3: padding
    step 4: call model
    """
    # step 0
    batch_size = config['batch_size']
    max_gen_len = config['max_gen_len']
    end_token = config['end_token']
    is_sample = config['is_sample']

    new_reqs = []
    for request in requests:
        context = request['context']
        context_enc = tokenizer.encode(context, add_special_tokens=False)

        key = context
        clean_key = tokenizer.decode(context_enc[-(model_max_length-max_gen_len):])
        length = -len(context_enc)
        new_reqs.append((key, clean_key, length))

    # step 1: sort
    new_reqs.sort(key=lambda x: x[-1])
    print("get %d request, max len: %d, min len %d"%(len(new_reqs), -new_reqs[0][-1], -new_reqs[-1][-1]))

    # step 2: batch
    cache_res = {}
    for i in tqdm(range(0, len(new_reqs), batch_size), disable=disable_tqdm):
        chunk = new_reqs[i:i + batch_size]
        input_texts = [x[0] for x in chunk]
        clean_keys = [x[1] for x in chunk]

        # step 3: padding
        inputs = tokenizer(
            clean_keys,
            return_tensors='pt',
            padding="longest" if tokenizer.pad_token_id else False,
            max_length=model_max_length,
            truncation=True,
            return_attention_mask=True,
            add_special_tokens=True
        )
        # step 4: call model
        kwargs = {
            # 'temperature': 0.8,
            # 'top_p': 0.95,
            # "top_k": 50,
            # "max_length": min(inputs['input_ids'].size(1) + max_gen_len, model_max_length),
            "max_new_tokens": min(max_gen_len, model_max_length - inputs['input_ids'].size(1)),
            "pad_token_id": tokenizer.pad_token_id,
            "eos_token_id": tokenizer.encode(end_token) if end_token else tokenizer.eos_token_id,
            "do_sample": is_sample
        }
        # model.device
        outputs = model.generate(inputs['input_ids'].to(model.device), use_cache=False, **kwargs)
        # import pdb; pdb.set_trace()
        
        # step 5: get answer
        output_texts = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        for in_txt, key_txt, out_txt in zip(input_texts, clean_keys, output_texts):
            # response = out_txt[len(key_txt):]
            response = out_txt.split(key_txt)[-1]
            cache_res[in_txt] = response

    results = []
    for request in requests:
        response = cache_res[request['context']]
        results.append(response)
    print("get %d result, and will back %d result"%(len(cache_res), len(results)))

    return results

def run_one_model(tasks_list, model_name):
    # get dataset
    task_dict = {
        task_name: tasks.TASK_REGISTRY[task_name]()
        for task_name in tasks_list
    }

    # config for tasks
    # batch, max_gen_len, end_token, etc.
    task_config = {}
    for task_name, task in task_dict.items():
        task_config[task_name] = task.get_config()
    
    # get requests
    task_requests = {}
    for task_name, task in task_dict.items():
        task_requests[task_name] = task.construct_requests()
        print("build <%s> requests success."%(task_name))

    # load tokenizer
    model, tokenizer = load_model_and_tokenizer(model_name)


    # model_max_length
    model_max_length = 2048
    if "llama2" in model_name or "baichuan2" in model_name:
        model_max_length = 4096
    elif "qwen" in model_name:
        model_max_length = 8192

    # test
    return_metrics = {}
    for task_name, task in task_dict.items():
        print("test: %s"%task_name)
        results = greedy_until(
            task_requests[task_name], 
            model, 
            tokenizer, 
            task_config[task_name], 
            disable_tqdm=False,
            model_max_length=model_max_length)

        
        metrics, logs = task.process_results(results)
        for key, value in metrics.items():
            print("%s:%.4f"%(key, value), end=", ")
            return_metrics[task_name+"_"+key] = value
        print()

        # write to file for logs
        output_dir = "../../logs/%s"%task_name
        output_path = "../../logs/%s/%s.json"%(task_name, model_name.replace("/", "_"))
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        with open(output_path, 'w', encoding="utf8") as f:
            for log in logs:
                f.write(json.dumps(log, indent=4, ensure_ascii=False) + '\n')

    return return_metrics


if __name__ == "__main__":
    # hyperparameters 
    tasks_list = [
        "dict_search_string",
        "dict_search_number",
        "natural_language_string",

        "check_order",
        "character_order",
        "word_order",
        "sentence_order",

        "check_dedup",
        "character_dedup",
        "word_dedup",
        "sentence_dedup",

        "relation_analysis",
        "navigation_and_count",

        "check_format",
        "output_format",
        "format_convert",

        "list_number", 
    ]

    model_names = [
        # "llama-7B-hf",
        # "llama-13B-hf",
        # "llama3-8B-hf",
        "llama3-70B-hf"
    ]

    all_metrics = []
    for model_name in model_names:
        print("testing model <%s>"%model_name)
        metrics = run_one_model(tasks_list, model_name)
        all_metrics.append(metrics)

    # write all
    import datetime
    time_tag = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    with open("../../y%s.csv"%(time_tag), "w", encoding='utf8') as f:
        for name in model_names:
            f.write(",%s"%name)
        f.write(",\n")
        keys = list(all_metrics[0].keys())
        for k in keys:
            f.write(k + ",")
            for metrics in all_metrics:
                f.write("%.4f,"%(metrics[k]))
            f.write("\n")




            
