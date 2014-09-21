clean:
	@find . -name "*.pyc" -delete

db:
	@python ./manage.py migrate

install:
	@pip install -r requirements.txt
	@python ./manage.py migrate

run:
	@python ./manage.py runserver

pep8:
	@pep8 --exclude 'migrations' .
	
test:
	@coverage run --source=atados_core manage.py test -s -v 2

coverage:
	@coverage run --source=atados_core manage.py test
	@coverage html
	@open coverage_html_report/index.html

rebuild_index:
	@python ./manage.py rebuild_index

dump:
	@python ./manage.py dumpdata atados_core > atados_core/fixtures/data.json

dumpoauth2:
	@python ./manage.py dumpdata oauth2 > atados_core/fixtures/oauth.json

makemessages:
	@cd atados_core; \
	django-admin.py makemessages --all
	
compilemessages:
	@cd atados_core; \
	django-admin.py compilemessages
