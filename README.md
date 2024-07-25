# The Intuitive Inference and Rule-based Reasoning in LLMs
Check the LLMs' capacity of Intuitive Inference and Rule-based Reasoning. Inspired by the distinct performances between answering '9.11 or/and 9.9, which is bigger?'  and 'which is bigger, 9.11 or/and 9.9?'.

## Introduction
As a reasonable answering style, LLMs usually first state clearly the key answer and then give reasoning details, especially for a realative simple question. We termed **Intuitive Inference** as the directly given answer of a question at the start of the answer without a process of logic/rule-based reasoning. While the **Rule-based Reasoning** is like Chain of thought (CoT).

## Results
## The sequential order of 'rule' and 'numbers'
We considering two essentially indentical questions on number comparing, yet with different sequential order:
1. '9.11 or/and 9.9, which is bigger?'
2. 'which is bigger, 9.11 or/and 9.9?'
In Chinese, they are:
1. “9.11或/和9.9，哪个大？”
2. “哪个大，9.11或/和9.9？”

The performance difference.
![微信图片_20240717150545](https://github.com/user-attachments/assets/c845798a-d023-4f93-817a-3394522fcad0)

## Combined Intuitive Inference and Rule-based Reasoning

## Exclusion of tokenizer's fault: Default vs. Manipulatied Input Tokens
To exclude the effect of tokenizer, we manipulate the input tokens to make input tokens all the same but order, using the corresponding tokenizers.



## Other variations of number comparing

### Language difference

### LLM difference



## Discussion

### How to reveal the which factors determine the intuitions?

