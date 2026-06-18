from gsam.core.aquirer import get_source_code, get_source_meta
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

def run_engine():
  source_meta = get_source_meta()
  source_code = get_source_code(source_meta)

  if source_code is None:
    return

  PortalManager.set_material_dir(source_meta.material_dir())
  engine_pipeline.run(source_code)

