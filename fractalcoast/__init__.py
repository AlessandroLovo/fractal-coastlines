import importlib as _importlib
from pathlib import Path

pkg_name = 'fractalcoast'

__version__ = '0.0.2'

submodules = []
for path in Path(__file__).parent.glob('*.py'):
    if not path.name.startswith('_'):
        submodules.append(path.stem)

submodules = sorted(submodules)
print(f'{submodules = }')

def __getattr__(name):
    if name in submodules:
        return _importlib.import_module(f'{pkg_name}.{name}')
    else:
        try:
            return globals()[name]
        except KeyError:
            raise AttributeError(
                f"Module '{pkg_name}' has no attribute '{name}'"
            )