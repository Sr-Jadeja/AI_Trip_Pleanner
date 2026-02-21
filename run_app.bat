@echo off
echo Activating virtual environment...
call env\Scripts\activate

echo Starting FastAPI backend...
start cmd /k python -m uvicorn main:app --reload --port 8000

echo Starting Streamlit frontend...
start cmd /k streamlit run streamlit_app.py

echo All services started.
pause