from os.path import exists, isfile

from gsam.entities.node_stream import NodeStream
from gsam.entities.nodes.syntax_node import SyntaxNode
from gsam.interfaces.material_strategy import MaterialStrategy

from langex.core.classes import extends

@extends
class PythonInjectionStrategy(MaterialStrategy):
  IDENTIFIER = "PY-INJ"

  def __init__(self, material_dir: str, config: dict[str, str]):
    super().__init__(material_dir, config)
    self.namespace: dict[str, object] = {
      "extends": extends,
      "NodeStream": NodeStream,
      "SyntaxNode": SyntaxNode,
    }

  def _read(self, fpath: str) -> str:
    with open(fpath, 'r') as f:
      return f.read()

  def init(self, node: SyntaxNode, stream: NodeStream):
    entry_file = self.config.get("ENTRY_FILE", "main.py")
    entry_path = f"{self.material_dir}/{entry_file}"

    if not (exists(entry_path) and isfile(entry_path)):
      return

    injection_code = self._read(entry_path)
    namespace = self.namespace

    try:
      exec(injection_code, namespace, namespace)
      self._load(node, stream)
    except Exception:
      pass

  def _load(self, node: SyntaxNode, stream: NodeStream):
    if "load" in self.namespace:
      self.namespace["load"](node, stream)

