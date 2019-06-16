find ./services -name migrations | xargs rm -rf
find ./services -name __pycache__ | xargs rm -rf

python3 manage.py makemigrations --empty authentication basic course moments news student teacher timetable mustplus spider

python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8000

http://mp.junyi.pw:8000/basic/init/faculties
http://mp.junyi.pw:8000/basic/init/departments