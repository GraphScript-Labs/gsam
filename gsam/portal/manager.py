from os.path import exists, isdir

from gsam.entities.node_stream import NodeStream
from gsam.entities.nodes.syntax_node import SyntaxNode
from gsam.interfaces.material_strategy import MaterialStrategy
from gsam.portal.strategies.python_injection import PythonInjectionStrategy

from langex.core.classes import singleton

@singleton
class PortalManager:
  def __init__(self):
    self.material_dir: str = "materials"
    self.connections: dict[str, str] = {}

  def _read_config(self, config_path: str) -> dict[str, str]:
    if not exists(config_path):
      return {}

    if isdir(config_path):
      return {}

    lines = []

    with open(config_path, 'r') as f:
      lines = f.readlines()

    config: dict[str, str] = {}

    for line in lines:
      line = line.strip()

      if "=" not in line:
        continue

      key, value = line.split("=", 1)
      config[key.strip()] = value.strip()

    return config

  def _get_strategy(self, name: str) -> MaterialStrategy | None:
    material_dir = f"{self.material_dir}/{name}"

    if not (exists(material_dir) and isdir(material_dir)):
      return None

    config_path = f"{material_dir}/material.conf"
    config = self._read_config(config_path)

    if "TYPE" not in config:
      return None

    strategies = [
      PythonInjectionStrategy
    ]

    for strategy in strategies:
      if config["TYPE"] == strategy.IDENTIFIER:
        return strategy(material_dir)

    return None

  def connect(self, node: SyntaxNode, stream: NodeStream):
    material_name = node.content
    material_strategy = self._get_strategy(material_name)

    if material_strategy is None:
      return

    material_strategy.init(node, stream)

