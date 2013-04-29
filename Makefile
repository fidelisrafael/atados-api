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
	@coverage run --source=atados ./manage.py test

solr-rebuild:
	@python ./manage.py rebuild_index

solr-schema:
	@python ./manage.py build_solr_schema > schema.xml

dump:
	@python ./manage.py dumpdata core > atados/core/fixtures/initial_data.json
	@python ./manage.py dumpdata volunteer > atados/volunteer/fixtures/initial_data.json
	@python ./manage.py dumpdata nonprofit > atados/nonprofit/fixtures/initial_data.json
	@python ./manage.py dumpdata project > atados/project/fixtures/initial_data.json
