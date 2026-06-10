from gsam.optimizer.pruner import prune

from langex.core.pipeline import Pipeline

optimizer_pipeline = (
  Pipeline
  | prune
)

