from threading import Thread

from gsam.entities.node_stream import NodeStream
from gsam.entities.nodes.runtime_node import RuntimeNode
from gsam.entities.nodes.syntax_node import SyntaxNode

from langex.core.classes import singleton
from langex.core.functions import autosig

@singleton
class Runtime:
  def __init__(self):
    self.streams: dict[str, NodeStream] = {}

  @autosig
  def setup(self, root_node: SyntaxNode) -> str:
    stream_name = "sacred-stream"

    if stream_name in self.streams:
      stream_name = f"stream-{len(self.streams)}"

    runtime_node = RuntimeNode(root_node)
    self.streams[stream_name] = NodeStream(stream_name, self)
    self.streams[stream_name].push(runtime_node)

    return stream_name

  @autosig
  def run_stream(self, stream_name: str):
    if stream_name not in self.streams:
      return None

    stream = self.streams[stream_name]

    while stream.has_nodes():
      node = stream.poll()
      node.initiate(stream)

  @autosig
  def execute(self, stream_name: str):
    if stream_name not in self.streams:
      return None

    thread = Thread(
      name=f"RuntimeStream-{stream_name}",
      target=self.run_stream,
      args=(stream_name,),
      daemon=False,
    )

    thread.start()
    thread.join()

