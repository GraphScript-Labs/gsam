from gsam.executor.runtime import Runtime

from langex.core.pipeline import Pipeline

executor_pipeline = (
  Pipeline
  | Runtime.setup
  | Runtime.execute
)

