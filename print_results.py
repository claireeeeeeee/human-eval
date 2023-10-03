import json
import re
from collections import defaultdict
import jsonlines

def calculate_accuracy(jsonl_file_path):
    total_tasks = 0
    passed_tasks = 0
    
    with open(jsonl_file_path, 'r') as file:
        for line in file:
            total_tasks += 1
            json_data = json.loads(line)
            
            if json_data['result'] == "passed":
                passed_tasks += 1
                
    if total_tasks == 0:
        return 0  # 防止除以零错误
    
    accuracy = (passed_tasks / total_tasks) * 100
    return accuracy

def extract_erroneous_lines(jsonl_file_path, output_jsonl_file_path):
    erroneous_lines = []
    
    with open(jsonl_file_path, 'r') as file:
        for line in file:
            json_data = json.loads(line)
            
            if 'result' in json_data and json_data['passed'] == False:
                erroneous_lines.append(line.strip())

    # Write the erroneous lines to a new jsonl file
    with open(output_jsonl_file_path, 'w') as err_file:
        for err_line in erroneous_lines:
            err_file.write(err_line + '\n')

def extract_function_name(code: str) -> str:
    match = re.search(r'def (\w+)\(', code)
    return match.group(1) if match else ""

def extract_jsonl(input_file_path, output_file_path):
    # 使用字典来存储每个 task_id 对应的 prompt 和 completion
    task_data = defaultdict(dict)

    with open(input_file_path, "r") as infile:
        for line in infile:
            data = json.loads(line)
            task_id = data.get("task_id", None)

            if task_id is not None:
                if "prompt" in data:
                    task_data[task_id]["prompt"] = data
                if "completion" in data:
                    task_data[task_id]["completion"] = data

    # 打开新的文件以写入不匹配的行
    with open(output_file_path, "w") as outfile:
        for task_id, data in task_data.items():
            prompt_data = data.get("prompt", None)
            completion_data = data.get("completion", None)

            if prompt_data is None or completion_data is None:
                # 如果缺少 prompt 或 completion，输出错误
                if prompt_data:
                    outfile.write('E')
                #    outfile.write(json.dumps(prompt_data))
                    outfile.write('\n')
                if completion_data:
                    outfile.write('E')
                #    outfile.write(json.dumps(completion_data))
                    outfile.write('\n')
                continue

            prompt_function_name = extract_function_name(prompt_data["prompt"])
            completion_function_name = extract_function_name(completion_data["completion"])

            if prompt_function_name != completion_function_name:
                # 输出不匹配的 prompt 和 completion
                outfile.write(json.dumps(prompt_data))
                outfile.write('\n')
                #outfile.write(json.dumps(completion_data))
                #outfile.write('\n')

def print_id(input_file_path):
    task_ids = set()

    # 打开并读取文件
    with open(input_file_path, "r") as infile:
        for line in infile:
            data = json.loads(line)
            task_id = data.get("task_id", None)  # 获取task_id，如果不存在则返回None

            if task_id is not None:
                task_ids.add(task_id)

    return task_ids

def sorted_numbers(task_ids):
    task_ids = print_id("/home/cli776/human-eval/pair2/pair3_mismatched.jsonl")
    extracted_numbers = [int(task_id.split('/')[1]) for task_id in task_ids]
    sorted_numbers = sorted(extracted_numbers)
    return sorted_numbers

def select_lines(selected_ids):
    selected_lines = []

    # 打开并读取文件
    with open('/home/cli776/1/HumanEval.jsonl', 'r') as f:
        for line in f:
            # 将每一行转化为 JSON 对象
            json_obj = json.loads(line.strip())
            
            # 提取 task_id
            task_id = int(json_obj.get('task_id', '').split('/')[-1])  # 假设 task_id 是 "HumanEval/数字" 的格式
            
            # 检查是否在选定的 ID 列表中
            if task_id in selected_ids:
                selected_lines.append(line)

    # 将选定的行写入新的文件
    with open('/home/cli776/1/newHumanEval.jsonl', 'w') as f:
        for line in selected_lines:
            f.write(line)

def filter_out_assertion_error(filepath: str, new_filepath: str):
    with open(filepath, 'r') as infile, open(new_filepath, 'w') as outfile:
        for line in infile:
            data = json.loads(line.strip())
            if 'result' in data and 'AssertionError' not in data['result']:
                outfile.write(line)

def process_jsonl(file_path):
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]

    # 初始化一个空列表来存储所有的数字
    numbers_list = []

    # 定义一个正则表达式来匹配HumanEval/字段后面的数字
    pattern = re.compile(r'HumanEval/(\d+)')

    # 遍历文件中的每一行
    for item in data:
        for key in item.keys():
            match = pattern.search(key)
            if match:
                number = match.group(1)  # group(1)表示提取第一个捕获组的内容，也就是数字
                numbers_list.append(int(number))

    # 打印找到的数字
    print(numbers_list)

    # 检查数字列表中的元素是否为连续的数字
    is_consecutive = all(b - a == 1 for a, b in zip(numbers_list, numbers_list[1:]))
    print(is_consecutive)  # 打印是否连续


# Example usage
input_jsonl_file_path = "/home/cli776/human-eval/new_pair/samples_loop3.jsonl_results.jsonl"
output_jsonl_file_path = "/home/cli776/human-eval/new_pair/samples_loop3.jsonl_erroneous.jsonl"

# 用文件路径替换 'your_file.jsonl'
file_path = '/home/cli776/human-eval/new_pair/recoding_loop1.jsonl'
result = process_jsonl(file_path)
print(result)

#extract_erroneous_lines(input_jsonl_file_path, output_jsonl_file_path)
#print(calculate_accuracy(input_jsonl_file_path))

#task_ids = print_id("/home/cli776/human-eval/samples_pair3.jsonl")
#sorted_numbers = sorted_numbers(task_ids)
#print(len(sorted_numbers))
#select_lines(sorted_numbers)

#filter_out_assertion_error(output_jsonl_file_path, "/home/cli776/human-eval/new_pair/samples4.jsonl_AssertionError.jsonl")
#extract_jsonl(output_jsonl_file_path, "/home/cli776/human-eval/new_pair/samples4.jsonl_Extract.jsonl")