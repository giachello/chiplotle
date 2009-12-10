import os
from chiplotle.cfg.cfg import CONFIG_DIR
from chiplotle.tools.io.export import export
from chiplotle.tools.io._open_file import _open_file

def view(expr):
   '''Displays Chiplotle-HPGL objects for prevewing.

   - `expr` can be an iterable (e.g., list) or a Chiplotle-HPGL object.
   '''

   ## get output dir.
   OUTPUT_DIR = os.path.join(CONFIG_DIR, 'output')
   file_name = os.path.join(OUTPUT_DIR, 'tmp')

   export(expr, file_name, 'eps')
   ## show!
   _open_file(file_name + '.eps')