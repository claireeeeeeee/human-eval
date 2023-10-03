from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)
from .tool import get_completion_from_messages
import re
from .data_process import extract_task_ids, extract_prompt_by_task_id, extract_entry_point_by_task_id, extract_canonical_solution_by_task_id

bp = Blueprint("chatTest", __name__, url_prefix="/chatTest")


@bp.get("/")
def index():
    return render_template("chatgpt/chat_code_develop.html")


delimiter_1 = "```"

system_message = f"""There is a development team that \ 
includes a requirement analyst, a coder, and a quality tester. \
The team needs to develop programs that satisfy the requirements of \
the users. The different roles have different divisions of \
labor and need to cooperate with each others"""

requirment = f"""triples_sum_to_zero takes a list of integers \
as an input. it returns True if there are three distinct elements \
in the list that sum to zero, and False otherwise."""


analyst_description = f""" I want you to act as an analyst \
on our development team. Analyze a user requirement.\
The user requirement will be provided between triple backticks (```),

Your role involves two primary responsibilities: \
1:Decompose User Requirements: decomposes the requirement x into \
several easy-to-solve subtasks that facilitate the division \
of functional units.

2:Develop High-Level Implementation Plan: Then, develops a high-level plan \
that outlines the major steps of the implementation.
"""

tester_description = f"""
I'd like you to assume the role of a tester within \
our development team. When you receive code from a coder, \
you are responsible for the following three steps:

Step 1: Document Test Report
Generate a comprehensive test report assessing various code aspects, \
including but not limited to functionality, readability, and maintainability.

Step 2: Advocate for Model-Simulated Testing
Promote the use of a process where our machine learning model \
simulates the testing phase and produces test reports, \
thereby automating quality assessment.

Step 3: Issue Reporting in JSON Format
List all identified issues in a JSON formatted document. \
Each issue entry should contain three key-value pairs: \
'description' for issue details, 'severity' to indicate \
the level of urgency, and 'suggested_fix' to propose a solution.

All parts of your response should be separated by \
triple backticks to denote different sections.
"""

tester_description1 = f"""I'd like you to serve as an tester \
on our development team. When you receive code from \
a developer, please follow this three-step process:

Step 1: (Delimited by triple backticks)
Produce a test report which covers several criteria \
including functionality, readability, and maintainability of the code.

Step 2: (Delimited by triple backticks)
Recommend a methodology where the model can simulate \
the testing process and generate test reports automatically.

Step 3: (Delimited by triple backticks)
Present any identified issues in JSON format. Each issue \
should have the following fields: 'description', 'severity', and 'suggested_fix'.

Remember, each part will be clearly marked within \
code blocks (delimited by triple backticks). \
Please ensure consistent outputs for identical inputs.
"""

tester_description0 = f"""
I want you to act as an analyst \
on our development team. You will receive the code from the coder.\

Your job is split into three steps: \
Step 1. {delimiter_1} Documents a test report containing \ 
various aspects, such as functionality, readability, \
and maintainability.

Step 2. {delimiter_1} Advocate for a practice \
where the model simulates the testing process \ 
and produces test reports.

Step 3. {delimiter_1} All issues are provided in JSON format. \
The format has 'description', 'severity', and 'suggested_fix'. \

The parts will be delimited by ```.
"""


code_sample = f"""def triples_sum_to_zero(nums):
    # Sort the list in ascending order
    nums.sort()
    
    # Iterate through the list
    for i in range(len(nums) - 2):
        # Check if the current element is the same as the previous element
        if i > 0 and nums[i] == nums[i-1]:
            continue
        
        # Set two pointers, one at the next element and one at the end of the list
        left = i + 1
        right = len(nums) - 1
        
        # Iterate while the two pointers don't overlap
        while left < right:
            # Calculate the sum of the three elements
            total = nums[i] + nums[left] + nums[right]
            
            # If the sum is zero, return True
            if total == 0:
                return True
            
            # If the sum is less than zero, move the left pointer to the right
            elif total < 0:
                left += 1
            
            # If the sum is greater than zero, move the right pointer to the left
            else:
                right -= 1
    
    # If no three elements sum to zero, return False
    return False
"""


coder_description = f""" You are taking on the role of a coder \
within our development team. Depending on the input you receive, \
your task is distinct:

Task Based on Input:
# Requirement Analyst Plan:
If you receive a plan from a requirement analyst, \
develop Python code in line with the plan. \
Ensure your code is efficient, adheres to \
readability standards, and follows coding best practices.

# Tester's Test Report:
If you receive a detailed test report and its accompanying \
Python code from a tester, \
your main task is to revise the code by incorporating \
the feedback from the test report. \

Your main objectives are:
1. You adhere strictly to the feedback given in the test report.
2. The modifications do not change the core functionality of the code.
3. You provide an improved version of the provided code that \
considers the feedback on readability and maintainability.

Note: No need for explanations or comments on the code you develop.
"""


@bp.get("/test2")
def project_analyst():

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"The requirement from users is {requirment}."},
        {'role': 'assistant', 'content': f"{analyst_description}"}
    ]

    bot_response = get_completion_from_messages(messages)
    print(bot_response)
    return jsonify({'bot_response': bot_response})


@bp.get("/test1")
def project_coder():

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"The requirement from users is {requirment}."},
        {'role': 'assistant', 'content': f"{coder_description}"}
    ]

    bot_response = get_completion_from_messages(messages)
    print(bot_response)
    return jsonify({'bot_response': bot_response})


@bp.get("/test3")
def project_tester():

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"The code from the coder is {code_sample}."},
        {'role': 'assistant', 'content': f"{tester_description}"}
    ]

    bot_response = get_completion_from_messages(messages)
    print(bot_response)
    return jsonify({'bot_response': bot_response})


@bp.route('/getAnalyst', methods=['POST'])
def getAnalyst():
    user_input = request.json['user_message']

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"The requirement from users is {delimiter_1}{user_input}{delimiter_1}."},
        {'role': 'assistant', 'content': f"{analyst_description}"}
    ]

    bot_response = get_completion_from_messages(messages)
    print(bot_response)
    return jsonify({'bot_response': bot_response})


@bp.route("/getCodeGeneration",  methods=['POST'])
def getCodeGeneration():
    user_input = request.json['user_message']

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"The requirement from users is {delimiter_1}{user_input}{delimiter_1}. Output in Python code format."},
        {'role': 'assistant', 'content': f"{coder_description}"}
    ]

    bot_response = get_completion_from_messages(messages)
    print(bot_response)
    result = extract_python_code(bot_response)
    return jsonify({'bot_response': result})


@bp.route("/getTester",  methods=['POST'])
def getTester():
    user_input = request.json['user_message']

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"The code from the coder is {user_input}."},
        {'role': 'assistant', 'content': f"{tester_description}"}
    ]

    bot_response = get_completion_from_messages(messages)
    print(bot_response)
    return jsonify({'bot_response': bot_response})


@bp.route("/getCodeTester",  methods=['POST'])
def getCodeTester():
    user_input = request.json['user_message']
    gpt_input = extract_between_steps(user_input)

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f" {delimiter_1}{gpt_input}{delimiter_1}. Output in Python code format."},
        {'role': 'assistant', 'content': f"{coder_description}"}
    ]

    bot_response = get_completion_from_messages(messages)
    print(bot_response)
    return jsonify({'bot_response': bot_response})


def extract_python_code(input_string):
    # Use regular expressions to find Python code within triple backticks (```)
    code_blocks = re.findall(r'```python(.*?)```', input_string, re.DOTALL)

    # Join the code blocks into a single string
    python_code = '\n'.join(code_blocks)

    python_code = re.sub(r'# Developer.*\n', '', python_code)

    if python_code.startswith('\n'):
        python_code = python_code[1:]

    return python_code


def extract_between_steps(text):
    # Find the start and end positions of "Step 1" and "Step 2"
    step1_start = text.find("Step 1:")
    step2_start = text.find("Step 2:")

    # Check if both "Step 1" and "Step 2" were found
    if step1_start != -1 and step2_start != -1:
        # Extract the text between "Step 1" and "Step 2"
        step1_text = text[step1_start + len("Step 1:"):step2_start].strip()
        return step1_text
    else:
        return None


@bp.get('/getTaskIDs')
def getTaskIDs():
    filename = "templates/human-eval/human-eval-v2-20210705.jsonl"
    taskId = extract_task_ids(filename)
    print(taskId)
    return jsonify({'taskid_list': taskId})


@bp.route('/getPrompt',  methods=['POST'])
def getPrompt():
    target_task_id = request.json['user_message']
    filename = "templates/human-eval/human-eval-v2-20210705.jsonl"
    prompt = extract_prompt_by_task_id(filename, target_task_id)
    print(prompt)
    return jsonify({'prompt': prompt})


@bp.route('/getCanonical',  methods=['POST'])
def getCanonical():
    target_task_id = request.json['user_message']
    filename = "templates/human-eval/human-eval-v2-20210705.jsonl"
    entry_point = extract_entry_point_by_task_id(filename, target_task_id)
    canonical_solution = extract_canonical_solution_by_task_id(filename, target_task_id)
    return jsonify({'entry_point': entry_point, 'canonical_solution': canonical_solution})