import io

from chiplotle.core.cfg.cfg import CONFIG_FILE


def read_config_file():
    """Read the content of the config file ``$HOME/.chiplotle/config.py``.
    Returns a dictionary of ``var : value`` entries."""

    globals = {}
    locals = {}
    with io.open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        exec(compile(f.read(), CONFIG_FILE, "exec"), globals, locals)
    return locals
