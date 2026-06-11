from gsam.entities.memory import Memory
from gsam.entities.node_stream import NodeStream
from gsam.entities.syntax_node import SyntaxNode
from gsam.interfaces.node import Node

from langex.core.classes import extends
from langex.core.functions import autosig

@extends
class RuntimeNode(Node):
  def __init__(
    self,
    node: SyntaxNode,
    source: Node | None = None,
    arg_name: str | None = None
  ):
    self.syntax: SyntaxNode = node
    self.source: Node | None = source
    self.execution_state: str = "pending"
    self.arg_name: str | None = arg_name

  @autosig
  def run_group(
    self,
    stream: NodeStream,
    syntax: SyntaxNode,
    identifiers: list[str],
  ):
    for identifier in identifiers[::-1]:
      nodes = syntax.attached.get(identifier, [])

      for node in nodes:
        runtime_node = RuntimeNode(node, self)
        stream.push(runtime_node)

  @autosig
  def save_node(self, memory: Memory):
    memory.upsert(self.syntax.content, self.syntax)

  @autosig
  def evaluate_args(self, node: SyntaxNode, stream: NodeStream):
    self.execution_state = "preparing"
    syntax = self.syntax
    stream.push(self)
    arg_names = node.attached.get("+", [])
    passed_args = syntax.attached.get("+", [])
    iteration_len = min(len(arg_names), len(passed_args))
    arg_idx = 0

    while arg_idx < iteration_len:
      passed_arg = passed_args[arg_idx]
      arg_name = arg_names[arg_idx].content
      runtime_node = RuntimeNode(passed_arg, self, arg_name)
      stream.push(runtime_node)
      arg_idx += 1

    self.execution_state = "ready"

  @autosig
  def execute_internal(self, node: SyntaxNode, stream: NodeStream):
    memory = stream.memory
    self.execution_state = "executing"
    stream.push(self)
    memory.create_scope()
    self.run_group(
      stream, node, ["*", "-"],
    )

    self.execution_state = "executed"

  @autosig
  def cleanup(self, node: SyntaxNode, stream: NodeStream):
    memory = stream.memory
    self.execution_state = "cleaning"
    return_node = node.attached.get("=", [])
    returned_node: SyntaxNode | None = None
    save_names_nodes = self.syntax.attached.get("=", [])
    save_names = [node.content for node in save_names_nodes]

    for ret_node in return_node:
      found, returned_node = memory.search(ret_node.content)

      if found:
        break

    memory.poll_scope()

    if returned_node is not None:
      for save_name in save_names:
        memory.upsert(save_name, returned_node)

    self.execution_state = "done"

  @autosig
  def execute(self, stream: NodeStream):
    syntax = self.syntax
    memory = stream.memory
    saved, node = memory.search(syntax.content)
    node: SyntaxNode = node

    if not saved:
      return

    if self.execution_state == "pending":
      self.evaluate_args(node, stream)
      return

    if self.execution_state == "ready":
      self.execute_internal(node, stream)
      return

    if self.execution_state == "executed":
      self.cleanup(node, stream)
      return

  @autosig
  def initiate(self, stream: NodeStream):
    syntax = self.syntax
    memory = stream.memory

    if syntax.identity == ">":
      self.run_group(
        stream,
        syntax,
        [
          "$", "*", ">", "-",
        ],
      )

    if syntax.identity == "*":
      self.save_node(memory)
      return

    if syntax.identity in "+-":
      self.execute(stream)
      return

