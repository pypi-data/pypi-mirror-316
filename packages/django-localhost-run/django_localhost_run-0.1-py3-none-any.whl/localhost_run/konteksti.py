from contextlib import contextmanager
import subprocess
import re


@contextmanager
def localhost_run(portti: int = 8000):
  proc = subprocess.Popen(
    # ssh -T: ei käytetä pseudopäätettä. Pseudopääte sotkee sen
    # pääteistunnon parametrit, jossa `runserveriä` ajetaan.
    ['ssh', '-T', '-R', f'80:localhost:{portti}', 'localhost.run'],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    encoding='utf-8',
  )
  try:
    # Ohitetaan ensimmäinen rivi, poimitaan tunnelin osoite toiselta.
    try:
      proc.stdout.readline()
      if osoite := re.search(r'https://.*.lhr.life', proc.stdout.readline()):
        osoite = osoite.group(0)
    except Exception:
      yield None
    else:
      yield osoite
  finally:
    proc.kill()
    proc.wait()
  # def localhost_run
