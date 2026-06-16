from gsam.entities.node_stream import NodeStream
from gsam.entities.nodes.syntax_node import SyntaxNode

from langex.core.classes import singleton

@singleton
class PortalManager:
  def __init__(self):
    self.material_dir: str = ""
    self.connections: dict[str, str] = {}

  def set_material_dir(self, material_dir: str):
    pass

  def connect(self, node: SyntaxNode, stream: NodeStream):
    pass

