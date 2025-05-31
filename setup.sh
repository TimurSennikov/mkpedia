if [[ ! -d venv ]]; then
    python3 -m venv venv
    source venv/bin/activate
    pip3 install flask
else
    source venv/bin/activate
fi

if [[ ! -d ../instance ]]; then
    flask --app app init_db
fi

flask --app app run
