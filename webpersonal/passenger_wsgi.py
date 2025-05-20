# Este archivo tiene que estar en la carpeta princilap: por ejemplo httpsdocs y no en httpsdocs/webpersonal/


import sys, os

ApplicationDirectory = 'webpersonal'
ApplicationName = 'webpersonal'
VirtualEnvDirectory = 'venv'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio del archivo actual (/var/www/vhosts/axxyss.com/httpdocs)
VirtualEnv = os.path.join(BASE_DIR, ApplicationDirectory, VirtualEnvDirectory, 'bin', 'python')

if sys.executable != VirtualEnv:
    os.execl(VirtualEnv, VirtualEnv, *sys.argv)

sys.path.insert(0, os.path.join(BASE_DIR, ApplicationDirectory))
sys.path.insert(0, os.path.join(BASE_DIR, ApplicationDirectory, ApplicationName))
sys.path.insert(0, os.path.join(BASE_DIR, ApplicationDirectory, VirtualEnvDirectory, 'bin'))
os.chdir(os.path.join(BASE_DIR, ApplicationDirectory))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', ApplicationName + '.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()