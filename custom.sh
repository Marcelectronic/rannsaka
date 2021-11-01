pip freeze > requirements.txt
python manage.py makemigrations
python manage.py migrate
django-admin makemessages -l es
django-admin compilemessages
rm /staticfiles/*
python manage.py collectstatic
python manage.py compress --force
git add .
git commit -m "Version 1.0.0"
git push heroku master
git push origin master



