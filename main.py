import tkinter as tk
from tkinter import scrolledtext
import sys
import io

# 동현랭 코드에서 사용할 키워드를 파이썬 코드로 변환하는 함수
def parse_line(line, indent_level):
    indent = '    ' * indent_level  # 파이썬의 들여쓰기 (4 spaces)
    
    # 변수 할당
    if line.startswith('봑 '):
        return indent + line.replace('봑 ', '')

    # 조건문
    elif line.startswith('동현?'):
        condition = line[3:].strip()
        return indent + f"if {condition}:"
    elif line.startswith('동?현'):
        condition = line[3:].strip()
        return indent + f"elif {condition}:"
    elif line.startswith('?동현'):
        return indent + "else:"

    # 반복문
    elif line.startswith('똥똥현현'):
        condition = line[5:].strip()
        return indent + f"while {condition}:"

    # 함수 정의
    elif line.startswith('바아도오'):
        func_def = line[5:].strip()
        return indent + f"def {func_def}:"

    # 함수 호출
    elif line.startswith('도오'):
        func_call = line[2:].strip()
        return indent + f"{func_call}"

    # 반환값
    elif line.startswith('형돈'):
        return indent + f"return {line[2:].strip()}"
    elif '현동' in line:
        output = line[line.index('현동') + 2:].strip()
        return indent + f"print({output})"

    # 그 외
    else:
        return indent + line

def execute_donghyeon_code(code):
    lines = code.split('\n')

    python_code = []
    indent_level = 0
    indent_stack = [0]

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('#'):
            continue

        if stripped_line.startswith('바박') or stripped_line.startswith('도동'):
            continue

        if stripped_line.startswith(('동현?', '똥똥현현', '바아도오')):
            parsed_line = parse_line(stripped_line, indent_level)
            python_code.append(parsed_line)
            indent_level += 1
            indent_stack.append(indent_level)
        elif stripped_line.startswith(('동?현', '?동현')):
            indent_level = max(0, indent_stack[-1] - 1)
            parsed_line = parse_line(stripped_line, indent_level)
            python_code.append(parsed_line)
            indent_level += 1
            indent_stack.append(indent_level)
        elif stripped_line.startswith('도오'):
            indent_level = max(0, indent_stack[-1] - 1)
            parsed_line = parse_line(stripped_line, indent_level)
            python_code.append(parsed_line)
        else:
            parsed_line = parse_line(stripped_line, indent_level)
            python_code.append(parsed_line)

        if stripped_line.startswith('도동'):
            if len(indent_stack) > 1:
                indent_stack.pop()
            indent_level = indent_stack[-1]

    generated_code = '\n'.join(python_code)
    return generated_code
def run_donghyeon_code():
    code = code_entry.get("1.0", tk.END)
    python_code = execute_donghyeon_code(code)
    output_text.insert(tk.END, "\n")
    
    # 기존 stdout 백업
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    try:
        exec(python_code, globals())
    except Exception as e:
        output_text.insert(tk.END, str(e))
    
    # 실행 결과를 tkinter 텍스트 위젯에 표시
    output_text.insert(tk.END, new_stdout.getvalue())
    
    # stdout 복원
    sys.stdout = old_stdout

# tkinter GUI 설정
root = tk.Tk()
root.title("동현랭 실행기")

# 동현랭 코드 입력 창
tk.Label(root, text="동현랭 코드 입력:").pack()
code_entry = scrolledtext.ScrolledText(root, width=50, height=15)
code_entry.pack()

# 실행 버튼
tk.Button(root, text="실행", command=run_donghyeon_code).pack()

# 출력 결과 창
tk.Label(root, text="출력 결과:").pack()
output_text = scrolledtext.ScrolledText(root, width=50, height=10)
output_text.pack()

# GUI 실행
root.mainloop()
