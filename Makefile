clean:
	@find . -name "*.pyc" -delete

db:
	@python ./manage.py syncdb --noinput
	@python ./manage.py migrate

install:
	@pip install -r requirements.txt -q --use-mirrors
	@python ./manage.py syncdb --noinput
	@python ./manage.py migrate

run: makemessages compilemessages
	@python ./manage.py runserver

pep8:
	@pep8 --exclude 'migrations' .
	
sass:
	@sass --style compressed --watch atados_core/sass:atados_core/static/css

test:
	@coverage run --source=atados ./manage.py test

rebuild_index:
	@python ./manage.py rebuild_index

dump:
	@python ./manage.py dumpdata core > atados_core/fixtures/initial_data.json

makemessages:
	@cd atados_core; \
	django-admin.py makemessages --all
	
compilemessages:
	@cd atados_core; \
	django-admin.py compilemessages
