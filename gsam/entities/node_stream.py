from gsam.entities.memory import Memory
from gsam.interfaces.node import Node

from langex.core.classes import langex_class
from langex.core.functions import autosig

@langex_class
class NodeStream:
  class __DequeNode__:
    def __init__(self, node: Node):
      self.node: Node = node
      self.next: NodeStream.__DequeNode__ | None = None

  def __init__(self, name: str):
    self.name: str = name
    self.memory: Memory = Memory()
    self._head: NodeStream.__DequeNode__ | None = None
    self._tail: NodeStream.__DequeNode__ | None = None

  def has_nodes(self) -> bool:
    return self._head is not None

  @autosig
  def push(self, node: Node):
    new_node = NodeStream.__DequeNode__(node)

    if self._head is None:
      self._head = new_node
      self._tail = new_node
    else:
      new_node.next = self._head
      self._head = new_node

  @autosig
  def poll(self) -> Node:
    node = self._head
    self._head = self._head.next

    if self._head is None:
      self._tail = None

    return node.node

