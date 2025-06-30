import ast
import re
import matplotlib.pyplot as plt
import numpy as np

async def check_file(files):
    results = []

    for file in files:
        result = {
            "filename": file.filename,
            "Long Function": 0,
            "Missing Docstring": 0,
            "Long File": 0,
            "Unused Variables": 0,
            "Total Lines": 0,
            "Function Lengths": []
        }
        print("Reading file:", file.filename)
        content = await file.read()
        code = content.decode('utf-8')

        file_extension = file.filename.split('.')[-1]

        if file_extension == 'py':
            # ניתוח קוד Python
            tree = ast.parse(code)
            assigned_vars = set()
            used_vars = set()
            lines = code.splitlines()
            total_lines = sum(1 for line in lines if line.strip())
            function_lengths_data = []

            # זיהוי משתנים שהוקצו
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            assigned_vars.add(target.id)

                # ניתוח פונקציות
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.body:
                        function_length = len(node.body)
                        function_lengths_data.append(function_length)
                    if len(node.body) > 20:
                        result['Long Function'] += 1
                    if not ast.get_docstring(node):
                        result['Missing Docstring'] += 1
                        print(f'Missing docstring for function: {node.name}')

                # ניתוח שימוש במשתנים
                if isinstance(node, ast.Name) and node.id not in assigned_vars:
                    used_vars.add(node.id)

            if total_lines > 200:
                result['Long File'] += 1

            # חישוב משתנים לא בשימוש
            unused_vars = assigned_vars - used_vars
            result['Unused Variables'] += len(unused_vars)
            result['Total Lines'] = total_lines
            result['Function Lengths'] = function_lengths_data

        else:
            # ניתוח קוד בשפות אחרות
            lines = code.splitlines()
            total_lines = sum(1 for line in lines if line.strip())
            if total_lines > 200:
                result['Long File'] += 1

            assigned_vars = set()
            used_vars = set()
            function_lengths = []

            for line in lines:
                if re.search(r'\b(?:void|static|public|private|protected|internal|protected internal|override|abstract)\s+\w+\s*\(.*?\)\s*{', line):
                    function_lengths.append(1)
                    if '/*' not in line and '*/' not in line and '///' not in line:
                        result['Missing Docstring'] += 1

                tokens = re.findall(r'\b\w+\b', line)
                for token in tokens:
                    if '=' in line:
                        assigned_vars.add(token)
                    elif token not in assigned_vars:
                        used_vars.add(token)

            unused_vars = assigned_vars - used_vars
            result['Unused Variables'] += len(unused_vars)

            for length in function_lengths:
                if length > 20:
                    result['Long Function'] += 1

            result['Function Lengths'] = function_lengths

        results.append(result)
    return results

async def create_graphs(results):
    graph_paths = []

    for result in results:
        function_lengths = result.get("Function Lengths", [])
        function_lengths = [length for length in function_lengths if isinstance(length, int) and length > 0]
        if function_lengths:
            plt.figure(figsize=(10, 5))
            try:
                function_lengths_np = np.array(function_lengths, dtype=int)
                plt.hist(function_lengths_np, bins=10, alpha=0.7)
                plt.title(f'Function Lengths Histogram for {result["filename"]}')
                plt.xlabel('Number of Lines')
                plt.ylabel('Frequency')
                hist_file_path = f"histogram_{result['filename']}.png"
                plt.savefig(hist_file_path)
                plt.close()
                graph_paths.append(hist_file_path)
            except ValueError as e:
                print(f"Error converting function lengths to numpy array for {result['filename']}: {e}")
                continue

    for result in results:
        warnings = {
            "Long Function": result["Long Function"],
            "Missing Docstring": result["Missing Docstring"],
            "Long File": result["Long File"],
            "Unused Variables": result["Unused Variables"],
        }
        plt.figure(figsize=(8, 8))
        plt.pie(list(warnings.values()), labels=warnings.keys(), autopct='%1.1f%%', startangle=140)
        plt.title(f'Warnings Distribution for {result["filename"]}')
        pie_file_path = f"pie_chart_{result['filename']}.png"
        plt.savefig(pie_file_path)
        plt.close()
        graph_paths.append(pie_file_path)

    issue_counts = {result["filename"]: sum(value for key, value in result.items() if isinstance(value, int) and key != "filename") for result in results}
    plt.figure(figsize=(10, 5))
    plt.bar(issue_counts.keys(), issue_counts.values(), color='orange')
    plt.title('Number of Issues per File')
    plt.xlabel('File Name')
    plt.ylabel('Count of Issues')
    bar_file_path = 'bar_chart_issues.png'
    plt.savefig(bar_file_path)
    plt.close()
    graph_paths.append(bar_file_path)

    return {"graphs": graph_paths}






