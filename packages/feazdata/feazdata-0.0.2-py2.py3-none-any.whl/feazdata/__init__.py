import pandas
from pkg_resources import resource_filename as _rf

__all__ = [
    "ames",
    "flights",
    "shelter_cats"
]

def __getattr__(name):
  if name in __all__:
    return pandas.read_csv(_rf("feazdata", f"data/{name}.csv"))
