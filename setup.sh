if [[ ! -d venv ]]; then
    python -m venv venv
    source venv/bin/activate
    pip install flask
    pip install 'uvicorn[standard]'
else
    source venv/bin/activate
fi

if [[ ! -d instance ]]; then
    cd mk
    flask --app app init_db
    cd ..
fi

python main.py
