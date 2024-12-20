# pylint: disable=invalid-name
# pylint: disable=ungrouped-imports

from importlib import import_module
import os

from django.apps import apps
from django.core.management import find_commands
from django.core.management.base import BaseCommand, CommandError

from localhost_run.konteksti import localhost_run


Command: type(BaseCommand)


for app_config in apps.get_app_configs():
  # Etsi se `python manage.py runserver`-toteutus, jota käytettäisiin,
  # ellei käsillä olevaa sovellusta olisi.
  if app_config.name == 'localhost_run':
    continue

  path = os.path.join(app_config.path, 'management')
  for name in find_commands(path):
    if name == 'runserver':
      assert issubclass(
        Command := import_module(
          f'{app_config.name}.management.commands.{name}'
        ).Command,
        BaseCommand,
      )
      break
  else:
    continue
  break

else:
  raise RuntimeError('Periytettävää `runserver`-toteutusta ei löydy!')


class Command(Command):
  ''' Periytetään seuraavasta `Command`-toteutuksesta. '''
  # pylint: disable=function-redefined

  def add_arguments(self, parser):
    super().add_arguments(parser)
    parser.add_argument(
      '--lhr',
      action='store_true',
      help='Luo Localhost.run-tunneli kehityspalvelimelle',
    )
    # def add_arguments

  def inner_run(self, *args, lhr, **options):
    '''
    Mikäli `--lhr` on annettu, avataan tunneli
    ja asetetaan ympäristömuuttujaan `LOCALHOST_RUN` tuloksena saatu
    `https://...lhr.file`-tyyppinen osoite ennen super-kutsua.
    '''
    if lhr:
      with localhost_run(self.port) as osoite:
        if not osoite:
          raise CommandError('Tunnelin avaus epäonnistui!')
        self.stdout.write('\n'.join((
          '',
          self.style.SUCCESS('Localhost.run: ') + osoite,
          '',
          ''
        )))
        os.environ['LOCALHOST_RUN'] = osoite
        return super().inner_run(*args, **options)
        # with localhost_run as osoite
      # if lhr
    return super().inner_run(*args, **options)
    # def inner_run

  # class Command
