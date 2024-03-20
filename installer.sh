python3 -m pip install --upgrade pip
python3 -m pip install virtualenv

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

python dbfiller.py
python runner.py run_app