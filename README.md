Atados
======

Voluntary network.


Running the project
-------------------

    git clone git@github.com:atados/atados.git
    cd atados
    pip install -r requirements/environment
    python manage.py syncdb
    python manage.py migrate
    python manage.py runserver

Now, you have a voluntary network at http://localhost:8000 and the
administrative section as http://localhost:8000/admin.


License
-------

Apache License, Version 2.0
See LICENSE file.
