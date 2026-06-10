from gsam.interfaces.node import Node
from gsam.models.memory import Memory
from gsam.models.node_stream import NodeStream
from gsam.models.syntax_node import SyntaxNode

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
    self.arg_vals: dict[str, Node] = {}
    self.return_node: Node | None = None
    self.return_path: int = 0

  def save_node(self, memory: Memory):
    memory.upsert(self.syntax.content, self.syntax)

  def evaluate_args(self, node: Node, queue: NodeStream):
    self.execution_state = "executing"
    syntax = self.syntax
    queue.push_start(self)
    arg_names = syntax.attached.get("+", [])
    passed_args = node.attached.get("+", [])
    iteration_len = min(len(arg_names), len(passed_args))
    arg_idx = 0

    while arg_idx < iteration_len:
      passed_arg = passed_args[arg_idx]
      arg_name = arg_names[arg_idx]
      runtime_node = RuntimeNode(passed_arg, self, arg_name)
      queue.push_start(runtime_node)
      arg_idx += 1

    self.execution_state = "ready"

  def execute_internal(self, node: Node, queue: NodeStream):
    memory = queue.memory
    self.execution_state = "executing"
    queue.push_start(self)
    memory.create_scope()
    internal_calls = node.attached.get("-", [])

    for internal_call in internal_calls:
      runtime_node = RuntimeNode(internal_call, self)
      queue.push_start(runtime_node)

    self.execution_state = "executed"

  def cleanup(self, queue: NodeStream):
    self.execution_state = "cleaning"
    queue.memory.poll_scope()
    result_node = self.syntax.attached.get("=", [None])[0]
    result_path = self.syntax.attached.get(":", [0])[0]
    self.return_node = result_node
    self.return_path = result_path
    self.execution_state = "done"

  def execute(self, queue: NodeStream):
    syntax = self.syntax
    memory = queue.memory
    saved, node = memory.search(syntax.content)
    node: SyntaxNode = node

    if not saved:
      return

    if self.execution_state == "pending":
      self.evaluate_args(node, queue)
      return

    if self.execution_state == "ready":
      self.execute_internal(node, queue)
      return

    if self.execution_state == "executed":
      self.cleanup(queue)
      return

  @autosig
  def initiate(self, queue: NodeStream):
    syntax = self.syntax
    memory = queue.memory

    if syntax.identity == "*":
      self.save_node(memory)
      return

    if syntax.identity == "-":
      self.execute(queue)
      return

