from gsam.entities.node_stream import NodeStream
from gsam.entities.nodes.syntax_node import SyntaxNode
from gsam.interfaces.material_strategy import MaterialStrategy

from langex.core.classes import extends

@extends
class PythonInjectionStrategy(MaterialStrategy):
  IDENTIFIER = "PY-INJ"

  def __init__(self, material_dir: str):
    self.material_dir = material_dir

  def init(self, node: SyntaxNode, stream: NodeStream):
    print(f"[PY-INJ]: {node.content}")

