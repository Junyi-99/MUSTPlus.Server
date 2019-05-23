find ./Services -name migrations | xargs rm -rf
find ./Services -name __pycache__ | xargs rm -rf

python3 manage.py makemigrations --empty Admin Authentication Basic Comment Moments News Timetable MUSTPlus Spider

python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8000

http://mp.junyi.pw:8000/basic/init/faculties
http://mp.junyi.pw:8000/basic/init/departments