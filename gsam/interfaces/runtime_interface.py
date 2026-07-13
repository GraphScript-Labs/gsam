from gsam.entities.nodes.syntax_node import SyntaxNode

from langex.core.classes import interface
from langex.core.functions import autosig

@interface
class RuntimeInterface:
  @autosig
  def setup(self, root_node: SyntaxNode): ...
  @autosig
  def run_stream(self, stream_name: str): ...
  @autosig
  def execute(self, stream_name: str): ...

