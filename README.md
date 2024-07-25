# The Intuitive Inference and Rule-based Reasoning in LLMs
Check the LLMs' capacity of Intuitive Inference and Rule-based Reasoning. Inspired by the distinct performances between answering '9.11 or/and 9.9, which is bigger?'  and 'which is bigger, 9.11 or/and 9.9?'.

## Introduction
As a reasonable answering style, LLMs usually first state the key answer clearly and then give reasoning details, especially for a realative simple question. We termed **Intuitive Inference** (II) as the directly given answer of a question at the start of the answer without a process of logic/rule-based reasoning. While the **Rule-based Reasoning** (RR) is like Chain of thought (CoT). Incorrect II and RR of LLM can both be called **Hallucination**.

## Results
## Combined Intuitive Inference and Rule-based Reasoning
Intuitive inference and rule-based reasoning are always combined in many generated answers of LLM. For gpt-4o, the 'first conclusion, then explanation' pattern is common.
![Screenshot from 2024-07-23 13-38-25](https://github.com/user-attachments/assets/598f0404-bd60-4fe5-82df-0211ca82a9cb)


The following figure shows two different response patterns of gpt-4-turbo. The left one always just answer with intuitive conclusion, while serveral round in right shows the combined II and RR. The differences of answering patterns determined by the description order of the question.
![image](https://github.com/user-attachments/assets/83425386-274d-46dc-800c-9ddbcc15023c)



## The sequential order of 'rule' and 'numbers'
We considering two essentially indentical questions on number comparing, yet with different sequential order:
1. '9.11 or/and 9.9, which is bigger?'
2. 'which is bigger, 9.11 or/and 9.9?'

In Chinese, they are:
1. “9.11或/和9.9，哪个大？”
2. “哪个大，9.11或/和9.9？”

The performance differences are show in the following table.
![微信图片_20240717150545](https://github.com/user-attachments/assets/c845798a-d023-4f93-817a-3394522fcad0)


## Exclusion of tokenizer's fault: Default vs. Manipulatied Input Tokens
To exclude the effect of tokenizer, we manipulated the input tokens to make input tokens all the same but order, using the corresponding tokenizers.


## Discussion

### How to reveal factors underlying a intuition?

### Rule confusion?
Is the LLM misunderstanding 9.11 and 9.9 as dates, or software versions? The two factors are scarely seem in LLM's answers. To further clarify those factors, we can emphasis them as real number in the questions.

### Language difference
As have revealed in previous sections, there exists some differences between languages.

### LLM difference
Gpt-4-turbo and gpt-4o have demonstrated different response patterns.

