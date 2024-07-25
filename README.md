# The Intuitive Inference and Rule-based Reasoning in LLMs
Check the LLMs' capacity of Intuitive Inference and Rule-based Reasoning. Inspired by the distinct performances between answering '9.11 or 9.9, which is bigger?'  and 'which is bigger, 9.11 or 9.9?'.

## Introduction
As a reasonable answering style, LLMs usually first state the key answer clearly and then give reasoning details, especially for a realative simple question. We termed **Intuitive Inference** (II) as the directly given conclusion of a question at the start of the answer without a prepositive process of logic/rule-based reasoning. While the **Rule-based Reasoning** (RR) is detailed and recalled related rules, e.g., Chain of thought (CoT). Incorrect descriptions in both II and RR can be called **Hallucination**.

## Results
## Combined Intuitive Inference and Rule-based Reasoning
Intuitive inference and rule-based reasoning are always combined in many generated answers of LLM. For gpt-4o, the 'first conclusion, then explanation' pattern is common.

![Screenshot from 2024-07-23 13-38-25](https://github.com/user-attachments/assets/598f0404-bd60-4fe5-82df-0211ca82a9cb)


The following figure shows two different response patterns of gpt-4-turbo. The left one always just answer with intuitive conclusion, while serveral round in right shows the combined II and RR. The differences of answering patterns determined by the description order of the question.

![image](https://github.com/user-attachments/assets/83425386-274d-46dc-800c-9ddbcc15023c)



## The sequential order of 'rule' and 'numbers'
We considered two essentially indentical questions on the two number comparement, yet with different sequential order:
1. '9.11 or/and 9.9, which is bigger?'
2. 'which is bigger, 9.11 or/and 9.9?'

In Chinese, they are:
1. “9.11或/和9.9，哪个大？”
2. “哪个大，9.11或/和9.9？”

The performance under different conditions is shown in the following table.

![微信图片_20240717150545](https://github.com/user-attachments/assets/c845798a-d023-4f93-817a-3394522fcad0)


## Not the tokenizer's fault: Default vs. Manipulated tokenizations
The same tokenization of the numbers were found, despite the order reversal of 'rule' and 'numbers'. Except the number tokens, there are another difference, the token of space and 'which' is different with ' which' (which with a space ahead). To exclude this seeming 'not the reason' minor difference, we manipulated the input tokens with the default tokenizer of each LLM. By replacing the token of '11' with two tokens of '1', and the token of ' which' as ' ' and 'which', we create a comparement of equal token distribution but different orders.

![image](https://github.com/user-attachments/assets/e4ade3b1-1f54-4fe4-97bb-cfc8b4e6f11c)


## Discussion

### How to reveal factors underlying a intuition?
The most convincing way: analysing the inner computations of LLM.

### Rule confusion?
Is the LLM misunderstanding 9.11 and 9.9 as dates, or software versions? The two factors are possible intuitions of human, but they are scarely mentioned in LLM's answers. To further clarify those factors, we can emphasis that the numbers are real number in the questions.

### Language difference
As have revealed in previous sections, there exists some differences between languages.

### LLM difference
Gpt-4-turbo and gpt-4o have demonstrated different response patterns.

### Conjunction
Is the conjunction matters? The answer is no! It improves accuracy, but is not a determinate factor.

![image](https://github.com/user-attachments/assets/924168d2-83e2-4b29-b8db-746cf1a3a32a)

