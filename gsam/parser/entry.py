from gsam.parser.synthesizer import synthesize
from gsam.parser.tokenizer import tokenize

from langex.core.pipeline import Pipeline

parser_pipeline = (
  Pipeline
  | tokenize
  | synthesize
)

