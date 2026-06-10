from gsam.models.node_stream import NodeStream
from gsam.models.runtime_node import RuntimeNode
from gsam.models.syntax_node import SyntaxNode

from langex.core.classes import singleton
from langex.core.functions import autosig

@singleton
class Runtime:
  def __init__(self):
    self.streams: dict[str, NodeStream] = {
      "sacred": NodeStream("sacred")
    }

  @autosig
  def setup(self, root_node: SyntaxNode) -> str:
    for identifier in "@*-":
      nodes = root_node.attached.get(identifier, [])

      for node in nodes:
        runtime_node = RuntimeNode(node)
        self.streams["sacred"].push_end(runtime_node)

    return "sacred"

  @autosig
  def execute(self, stream_name: str):
    if stream_name not in self.streams:
      return None

    stream = self.streams[stream_name]

    while stream.has_nodes():
      node = stream.poll()
      node.initiate(stream)

