# In-Context-Learning-Evaluation

## ICLEval data
We put the data of in-context learning tasks at `../data/tasks_data`

You can also generate these data by yourself using the code from `../code/generate_data` and the raw data from `../data/origin_data`.

## Evaluation

You can evalaute the models' in-context abilities using the code from `../code/model_evaluation`.

1) replace the `your_path` in line 40 of `../code/model_evaluation/run_icl_eval.py` to your own models' path.
2) execute `python run_icl_eval.py`.
