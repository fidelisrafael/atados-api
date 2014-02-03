"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'atados.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Dados do Atados'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            exclude=('django.contrib.*',),
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Suporte'),
            column=3,
            children=[
                {
                    'title': _('Achou algum bug?'),
                    'url': 'https://docs.google.com/forms/d/1INXr7s1ZTpOIcxw3uC8RBBERPOAF7YQw-nCryqCW6w0/viewform',
                    'external': True,
                },
                {
                    'title': _('Bugs existentes'),
                    'url': 'https://docs.google.com/spreadsheet/ccc?key=0AsFzBC8sBaDbdDBZYml6Z0ppb0VVbjdhdzRLelBoc0E#gid=0',
                    'external': True,
                },
            ]
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=15,
            collapsible=True,
            column=2,
        ))


