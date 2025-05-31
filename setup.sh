if [[ ! -d venv ]]; then
    python -m venv venv
    source venv/bin/activate
    pip install flask
    pip install gunicorn
else
    source venv/bin/activate
fi

if [[ ! -d ../instance ]]; then
    flask --app app init_db
fi

flask --app app run -p 5000
