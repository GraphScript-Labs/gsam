from os import getcwd
from os.path import exists, isfile

from sys import argv

from langex.core.classes import langex_class
from langex.core.functions import autosig

@langex_class
class SourceMeta:
  def __init__(self, workdir: str):
    self._workdir_parts = workdir.split("/")
    self._entry_file = "entry.gsam"
    self._material_dir = "materials"

  @autosig
  def add_workdir_parts(self, parts: list[str]):
    self._workdir_parts.extend(parts)

  @autosig
  def set_entry_file(self, entry_file: str):
    self._entry_file = entry_file

  @autosig
  def material_dir(self) -> str:
    workdir = "/".join(self._workdir_parts)

    return f"{workdir}/{self._material_dir}"

  @autosig
  def entry_file(self) -> str:
    workdir = "/".join(self._workdir_parts)

    return f"{workdir}/{self._entry_file}"

@autosig
def get_source_meta() -> SourceMeta:
  workdir = getcwd()
  source_meta = SourceMeta(workdir)
  cli_args = [*argv[1:]]

  if len(cli_args):
    parts = cli_args[0].split("/")
    entry_file = parts.pop()
    source_meta.add_workdir_parts(parts)
    source_meta.set_entry_file(entry_file)

  return source_meta

@autosig
def get_source_code(source_meta: SourceMeta) -> str | None:
  entry_file_path = source_meta.entry_file()

  if not exists(entry_file_path):
    return None

  if not isfile(entry_file_path):
    return None

  with open(entry_file_path, 'r') as f:
    return f.read()

