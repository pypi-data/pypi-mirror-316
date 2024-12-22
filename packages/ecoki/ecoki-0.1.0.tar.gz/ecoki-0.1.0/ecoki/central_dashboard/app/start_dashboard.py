import os
import django
from django.core.management import call_command
import argparse

parser = argparse.ArgumentParser(description='host url')
parser.add_argument("--host", type=str, default="127.0.0.1")
parser.add_argument("-p", "--port", type=int, default=20000)
parser.add_argument("--shell_host", type=str, default="127.0.0.1")
parser.add_argument("--shell_port", type=int, default=5000)

args = parser.parse_args()

host = args.host
port = args.port
shell_host = args.shell_host
shell_port = args.shell_port

def run_application(hostname, port):

    # Initialisierung der Django-Einstellungen
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ecoki_app.settings'

    # settings.configure()
    django.setup()

    # setzen der Django-Umgebungsvariablen
    from django.conf import settings
    settings.shell_host = shell_host
    settings.shell_port = shell_port

    call_command('makemigrations')
    call_command('migrate')
    call_command('createsuperuser_if_none_exists', user = 'ecoki_test',password = 'energy2022')
    call_command('runserver',f'{hostname}:{port}')

if __name__ == '__main__':
    run_application(host, port)