from gsam.entities.node_stream import NodeStream
from gsam.entities.nodes.syntax_node import SyntaxNode

from langex.core.classes import abstract
from langex.core.functions import abstracted, autosig

@abstract
class MaterialStrategy:
  IDENTIFIER: str = "BASE"

  @abstracted
  @autosig
  def init(self, node: SyntaxNode, stream: NodeStream):
    pass

