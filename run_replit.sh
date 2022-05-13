python3 -m pip install --upgrade pip

pip install -r requirements.txt

pip install discord

# TODO → Make responsible searching for python file
# python_location=$(python -c "import sys; print(sys.executable)")
# parentdir1="$(dirname "$python_location")"
# parentdir2="$(dirname "$parentdir1")"
# array=($(ls -d $parentdir2/lib/))
# script_file="$array[-1]/site-packages/flask_script/__init__.py"
# flask_script="$parentdir2$script_file"
# mv $flask_script "$flask_script".old
# cp flask_app/flask_script__init__.py $flask_script

mv /opt/virtualenvs/python3/lib/python3.8/site-packages/flask_script/__init__.py /opt/virtualenvs/python3/lib/python3.8/site-packages/flask_script/__init__.py.old
cp flask_app/flask_script__init__.py /opt/virtualenvs/python3/lib/python3.8/site-packages/flask_script/__init__.py


python run.py
