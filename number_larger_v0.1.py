##########==>
# Calling API or local model to answer number comparement questions, also measuring the capacity of Intuition and Reasoning in LLMs.
# email: felonwan@gmail.com
# upload date: 2024-07-14
##########==||

# ~ from transformers import AutoModelForCausalLM, AutoTokenizer
from modelscope import AutoTokenizer, AutoModelForCausalLM
from modelscope import GenerationConfig
import itertools as its
import numpy as np
import argparse
import datetime
import tiktoken
import string
import random
import torch
import time
import sys
import os


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-g","--gpu_ids",help="choose gpus", default="0")
	parser.add_argument("-mp","--model_path", help="choose a model", default="qwen/Qwen-72B-Chat-Int4",type=str)
	parser.add_argument("-nt","--n_trials", help="set number of trials to perform", default=3,type=int)
	parser.add_argument("-lang","--language", help="task types", default='en',type=str)
	parser.add_argument("-tpk","--top_k",help="length of the word", default=50,type=int)
	parser.add_argument("-mxnt","--max_new_tokens",help="max_new_tokens to generate",default=2048,type=int)
	parser.add_argument("-nbs","--numbers",nargs="+",help="specify numbers",default=[9.11,9.9],type=float)
	parser.add_argument("-bos","--bigger_or_smaller",help="prompt to give bigger/larger or smaller number",default='b',type=str,choices=['b','s'])
	parser.add_argument("-po","--prompt_order",help="rule first or number first",default='nf',type=str,choices=['nf','rf'])
	parser.add_argument("-std","--show_token_division",help="show the division of tokens",default=1,type=int,choices=[1,0])
	parser.add_argument("-cj","--conj",help="conjunctions for numbers",default='or',type=str)
	parser.add_argument("-tkrp","--token_replace",help="replacing tokens to for same conditions",default=0,type=int,choices=[0,1])
	return parser
parser = get_args()
args = parser.parse_args()
for v in vars(args):
	cmd_str = v+" = args."+v
	exec(cmd_str)
num1, num2 = numbers

# get a unique marker with datetime
def now_time_myformat():
	now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S-%f')
	return now
time_marker = now_time_myformat() # Time-Marker of start


# for openai API
from openai import OpenAI
base_url = "The API url"
api_key = "Your key here"
client = OpenAI(base_url=base_url,api_key=api_key)
def get_responses(prompt,model=model_path):
	try:
		response = client.chat.completions.create(messages=prompt,model=model)
		return {'role': response.choices[0].message.role,'content':response.choices[0].message.content}
	except Exception as e:
		print(e)
		return {'err_info':str(e)}
## gpt-4o ==> gpt-4o-2024-05-13
## gpt-4-turbo ==> gpt-4-turbo-2024-04-09

# to compare
comma = {'en':',','zh':'，'}
period = {'en':'.', 'zh':'。'}
space = {'en':' ','zh':''}
question_mark = {'en':'?','zh':'？'}
conjs = ' '+conj+' '
bigness = {'b':{'en':'bigger','zh':'大'},'s':{'en':'small','zh':'小'}}
task_prompt_num = {'en':str(num1)+conjs+str(num2), 'zh':str(num1)+'和'+str(num2)}
bn = bigness[bigger_or_smaller]
task_prompt_rule = {'en':'which is '+bn['en'], 'zh':'哪个'+bn['zh']}
prompt_head = task_prompt_num[language] + comma[language] + space[language]
prompt_tail = task_prompt_rule[language] + question_mark[language]
if 'gpt' in model_path:
	model_tail = model_path
	tokenizer = tiktoken.encoding_for_model(model_path)
else:
	model_tail = model_path.split('/')[1]
	tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)#,cache_dir=os.environ["MODELSCOPE_CACHE"])#, trust_remote_code=True)#revision='master',
	model = AutoModelForCausalLM.from_pretrained(
		model_path, revision='master',
		device_map="auto",
		torch_dtype=torch.float16,
		trust_remote_code=True,#use_flash_attn = flash_attn_support
	).eval()

# print and write to log file
file_name = model_tail+'_nt'+str(n_trials)+'lw'+str(num1)+'-'+str(num2)+'tpk'+str(top_k)+'_'+time_marker+'.txt'
log_file = open(file_name,'w')
def print_log(info_str,log_file=log_file):
	print(info_str+'\n')
	log_file.write(info_str+'\n')
	log_file.flush()


# setting for replacing tokens
tkn_numb_1 = tokenizer.encode('1')[0]
tkn_numb_11 = tokenizer.encode('11')[0]
tkn_space = tokenizer.encode(' ')[0]
tkn_which = tokenizer.encode('which')[0]
tkn_swhich = tokenizer.encode(' which')[0]
print('Token IDs:')
print('"1" -> '+str(tkn_numb_1),'"11" -> '+str(tkn_numb_1))
print('" " -> '+str(tkn_space), '"which" -> '+str(tkn_which), '" which" -> ' +str(tkn_swhich)
# function: replace tokens
# 函数：替换token，目前仅有用2个连续token替换1个的功能
def replace_tokens(tkns_in,from_tkn,to_tkn):
	if isinstance(tkns_in,torch.Tensor):
		tkns = tkns_in.cpu().numpy().tolist()
	else:
		tkns = tkns_in
	print('Original tokens:',str(tkns))
	idx = tkns.index(from_tkn)
	tkns[idx] = to_tkn[0]
	tkns.insert(idx+1,to_tkn[1])
	print('Tokens after relacing:',str(tkns))
	if isinstance(tkns_in,torch.Tensor):
		return torch.tensor([tkns]).cuda()
	else:
		return tkns
def get_tkns(tkns,head=None,tail=None,log_file=log_file):
	print_str = ''
	if head:
		print_str += head+'\n|'
	for t in tkns:
		print_str += tokenizer.decode([t])+'|'#.replace("'",'')
	if tail:
		print_str += '\n'
	return print_str

task_prompt = prompt_head + prompt_tail #+'\n'
if 'gpt' in model_path:
	input_tokens = tokenizer.encode(task_prompt)
	if token_replace:
		replace_tokens(input_tokens,tkn_numb_11,[tkn_numb_1 for i in range(2)])
		if prompt_order == 'nf':
			input_tokens = replace_tokens(input_tokens,tkn_swhich,[tkn_space,tkn_which])
	linp = len(input_tokens)
else:
	input_tokens = tokenizer.encode(task_prompt,return_tensors='pt').cuda()[0]#to(device)
	if token_replace and prompt_order == 'nf':
		input_tokens = replace_tokens(input_tokens,tkn_swhich,[tkn_space,tkn_which])
	linp = len(input_tokens)
print(get_tkns(input_tokens))


# The main iteration
prompt_list = []
print_log(model_path)
print_log(file_name)
user_head = 'User:'
assi_head = 'Assistant:'
for i in range(n_trials):
	num = '=='+str(i)+'=>'
	print_log(num)
	# get response and generate output
	prompt_list.append(task_prompt)
	lfix = len(tokenizer.encode(prompt_head))
	input_str = get_tkns(input_tokens,head=user_head,tail='\n')
	if 'gpt' in model_path:
		prompt_list = [{"role":"user","content":task_prompt}]
		message = get_responses(prompt_list,model=model_path)
		message_str = input_str + assi_head + message['content'] # ~ task_prompt+
	else:
		output = model.generate(input_tokens,max_new_tokens=max_new_tokens,top_k=top_k,output_logits=True)
		if show_token_division:
			message_str = '|'
			for j,t in enumerate(output[0][linp:]):
				message_str += tokenizer.decode([t])
				if j == linp-1:
					message_str += assi_head+'\n'
				if j<linp-1:
					message_str += '|'
				if show_token_division and j >= lfix-2:
					message_str += '|'
				# ~ else:
			# ~ message_str = tokenizer.decode(output[0])
	message_str += '\n\n'
	print_log(message_str)
	
	prompt_list.append(message_str)

log_file.close()


