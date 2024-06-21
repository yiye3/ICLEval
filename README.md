# In-Context-Learning-Evaluation

## ICLEval data
We put the data of this benchmark at `../data/tasks_data`

You can also generate these data by yourself using the code from `../code/generate_data` and the raw data from `../data/origin_data`.

## Evaluation

You can evaluate the models' in-context abilities using the code from `../code/model_evaluation`.

1) replace the `your_path` in line 40 of `../code/model_evaluation/run_icl_eval.py` with your own models' path.
2) execute `python run_icl_eval.py`.


## Citation Information

If you find this dataset useful, please consider citing our paper:

```
@misc{,
  title={ICLEval: Evaluating In-Context Learning Ability of Large Language Models},
  author={Wentong Chen, Yankai Lin,  ZhenHao Zhou, HongYun Huang, Yantao Jia, Zhao Cao, Ji-Rong Wen},
  year={2024},
  journal={},
}
```
