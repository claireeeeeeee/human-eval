import json

# 初始化行数计数器
line_number = 0

with open('/home/cli776/human-eval/samples_multi_2.jsonl', 'r') as f:
    for line in f:
        # 更新行数计数器
        line_number += 1
        try:
            # 尝试将行解析为JSON
            json_data = json.loads(line)
        except json.JSONDecodeError:
            # 打印出问题所在的行数和该行的内容
            print(f"JSON Decode Error at line {line_number}: {line}")
