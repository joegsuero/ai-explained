import sys
from django.conf import settings as django_settings

if not django_settings.configured:
    from settings import (
        DEBUG, SECRET_KEY, ALLOWED_HOSTS, INSTALLED_APPS, MIDDLEWARE,
        TEMPLATES_CONFIG, DATABASES_CONFIG, LANGUAGE_CODE, TIME_ZONE,
        USE_I18N, USE_TZ, STATIC_URL, STATICFILES_DIRS
    )

    django_settings.configure(
        DEBUG=DEBUG, SECRET_KEY=SECRET_KEY, ALLOWED_HOSTS=ALLOWED_HOSTS,
        INSTALLED_APPS=INSTALLED_APPS, MIDDLEWARE=MIDDLEWARE,
        ROOT_URLCONF=__name__, TEMPLATES=[TEMPLATES_CONFIG],
        DATABASES=DATABASES_CONFIG, LANGUAGE_CODE=LANGUAGE_CODE,
        TIME_ZONE=TIME_ZONE, USE_I18N=USE_I18N, USE_TZ=USE_TZ,
        STATIC_URL=STATIC_URL, STATICFILES_DIRS=STATICFILES_DIRS,
    )

from django.urls import path
from django.core.wsgi import get_wsgi_application
from web.views import home_view, api_evaluate, api_rules_info

urlpatterns = [
    path('', home_view),
    path('api/evaluate/', api_evaluate),
    path('api/rules/', api_rules_info),
]

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    from settings import AI_SYSTEM_INFO

    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        print(f"{AI_SYSTEM_INFO['name']} v{AI_SYSTEM_INFO['version']}")
        execute_from_command_line(
            [__file__, 'runserver', '8000', '--noreload'])
    else:
        print(f"Usage: python {__file__} runserver")
