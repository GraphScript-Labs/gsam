from gsam.executor.entry import executor_pipeline
from gsam.optimizer.entry import optimizer_pipeline
from gsam.parser.entry import parser_pipeline

from langex.core.pipeline import Pipeline

engine_pipeline = (
  Pipeline
  | parser_pipeline
  | optimizer_pipeline
  | executor_pipeline
)

