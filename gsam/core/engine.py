from os import getcwd
from os.path import exists, isfile

from sys import argv

from gsam.executor.entry import executor_pipeline
from gsam.optimizer.entry import optimizer_pipeline
from gsam.parser.entry import parser_pipeline
from gsam.portal.manager import PortalManager

from langex.core.pipeline import Pipeline

engine_pipeline = (
  Pipeline
  | parser_pipeline
  | optimizer_pipeline
  | executor_pipeline
)

def get_source_file_path() -> str:
  cli_args = [*argv[1:]]

  if len(cli_args) == 0:
    return "entry.gsam"

  return cli_args[0]

def acquire_source_code(
  workdir: str,
  source_file: str,
) -> str | None:
  file_path = f"{workdir}/{source_file}"

  if not exists(file_path):
    return None

  if not isfile(file_path):
    return None

  with open(file_path, 'r') as f:
    return f.read()

def run_engine():
  workdir = getcwd()
  cli_args = [*argv[1:]]
  material_dir = f"{workdir}/materials"
  source_file = get_source_file_path()
  source_code = acquire_source_code(
    workdir,
    source_file,
  )

  if source_code is None:
    return

  PortalManager.set_material_dir(material_dir)
  engine_pipeline.run(source_code)

