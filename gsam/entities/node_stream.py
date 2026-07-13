from gsam.entities.memory import Memory
from gsam.interfaces.node import Node

from langex.core.classes import langex_class
from langex.core.functions import autosig

@langex_class
class NodeStream:
  class __StackNode__:
    def __init__(self, node: Node):
      self.node: Node = node
      self.next: NodeStream.__StackNode__ | None = None

  def __init__(self, name: str, runtime):
    self.name: str = name
    self.memory: Memory = Memory()
    self._head: NodeStream.__StackNode__ | None = None
    self.runtime = runtime

  @autosig
  def has_nodes(self) -> bool:
    return self._head is not None

  @autosig
  def push(self, node: Node):
    new_node = NodeStream.__StackNode__(node)
    new_node.next = self._head
    self._head = new_node

  @autosig
  def poll(self) -> Node:
    node = self._head
    self._head = self._head.next

    return node.node

