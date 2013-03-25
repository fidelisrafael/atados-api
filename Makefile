clean:
	@find . -name "*.pyc" -delete

development:
	@pip install -r requirements/development

environment:
	@pip install -r requirements/environment

db:
	@python ./manage.py syncdb --noinput
	@python ./manage.py migrate

install:
	@pip install -r requirements/development -q --use-mirrors
	@python ./manage.py syncdb --noinput
	@python ./manage.py migrate

pep8:
	@pep8 --exclude 'migrations' .
	
sass:
	@sass --style compressed --watch atados/core/sass:atados/core/static/css

test:
	@python ./manage.py test

solr-rebuild:
	@python ./manage.py rebuild_index

solr-schema:
	@python ./manage.py build_solr_schema > schema.xml
