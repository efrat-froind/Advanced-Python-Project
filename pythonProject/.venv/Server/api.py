from fastapi import FastAPI, UploadFile, File
import ast
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter
import os
from checkFile import check_file, create_graphs
from datetime import datetime

app = FastAPI()
@app.post("/alerts")
async def alerts(files: list[UploadFile] = File(...)):
    print("in alerts:------------------------c")
    return await check_file(files)

@app.post("/analyze")
async def analyze(files: list[UploadFile] = File(...)):
    results = await check_file(files)  # קבל את התוצאות והאזהרות

    for result in results:
        # סכם רק את הערכים שהם מספריים, ולא את הרשימה של "Function Lengths"
        total_issues = sum(value for key, value in result.get("warnings", {}).items() if isinstance(value, int))

        # אם תרצה גם את אורך הפונקציות, תוכל להוסיף אותו בנפרד
        function_lengths = result.get("Function Lengths", [])
        total_issues += len(function_lengths)  # או כל חישוב אחר שתרצה לעשות עם הרשימה

        result['total_issues'] = total_issues

    return await create_graphs(results)  # צור גרפים על סמך התוצאות
