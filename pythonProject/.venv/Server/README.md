# Code Analysis System

## סקירה כללית
מערכת ניתוח קוד אוטומטית שמבוססת על FastAPI ומבצעת ניתוח קבצי Python בכל פעם שמשתמש מפעיל את פקודת `wit push`. המערכת מזהה בעיות נפוצות באיכות הקוד ומחזירה גרפים חזותיים עם תובנות. 
**הערה**: ודא שהפקודה `wit push` מוגדרת כראוי במערכת שלך.

## טכנולוגיות
- **שפה**: Python
- **שרת**: FastAPI
- **ניתוח קוד**: ast (עץ תחביר מופשט)
- **ויזואליזציה**: matplotlib

## הוראות התקנה
1. ודא שיש לך Python 3.7 ומעלה מותקן במערכת שלך.
2. הקם סביבה וירטואלית (מומלץ):
   ```bash
   python -m venv venv
   source venv/bin/activate  # עבור Windows השתמש ב-venv\Scripts\activate
התקן את התלויות:
pip install fastapi[all] matplotlib
הפעל את השרת:
uvicorn api:app --reload
דוגמת שימוש
להשתמש בנקודת הקצה /analyze:

curl -X POST "http://localhost:8000/analyze" -F "file=@/path/to/your/file.py"
מבנה תיקיות
.
├── main.py          # קובץ הקוד הראשי
├── requirements.txt  # רשימת התלויות
└── README.md        # קובץ זה
תרומות
אם ברצונך לתרום לפרויקט, אנא פתח בקשות משיכה (Pull Requests) או דווח על בעיות (Issues).

רישוי
פרויקט זה מופץ תחת רישוי MIT.

קישורים שימושיים
FastAPI Documentation
Matplotlib Documentation
