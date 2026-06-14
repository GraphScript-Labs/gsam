from gsam.entities.node_stream import NodeStream
from gsam.entities.nodes.syntax_node import SyntaxNode

from langex.core.classes import extends
from langex.core.functions import autosig

@extends
class MaterialNode(SyntaxNode):
  @autosig
  def execute_material(
    self,
    _syntax: SyntaxNode,
    _stream: NodeStream,
  ):
    pass

