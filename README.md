# [GSAM](https://pypi.org/project/gsam/)

GSAM compiler and execution engine

[![PyPI](https://img.shields.io/pypi/v/gsam?style=for-the-badge&logo=pypi)](https://pypi.org/project/gsam/)
[![GitHub](https://img.shields.io/badge/GitHub-repository-black?style=for-the-badge&logo=github)](https://github.com/graphscript-labs/gsam)

## Installation

```sh
pip install gsam
```

## About

GSAM is a compiler and execution engine built around a graph-based computation model. It is designed for extensibility, where external “Materials” define behavior and execution logic in a modular way.

Instead of traditional linear execution, GSAM represents programs as graphs of nodes, enabling flexible control flow, parallel execution patterns, and pluggable runtime behavior.

## Syntax

```gsam
? comment block (multi-line via indentation)
  lines starting with indentation are treated as part of the comment

- parent node
  = variable assignment
  @ keyword_argument
    + value
  + positional_argument
  > next node option

? chained execution example

- parent node
  + input
  - next node A
    + value
  - next node B
    + value
```

## Example

### Hello World

```gsam
- print
  + "Hello, GSAM!"
```

### Recursive / Loop-like Execution

```gsam
* count
  + curr
  - print
    + curr
  - count
    - add
      + curr
      + number
        ! 1
```

## Architecture

GSAM is built as a graph-native execution system with layered components:

### Pipeline

Source code flows through:
- Parsing
- Intermediate Representation (IR)
- Graph construction
- Execution

### Execution Engine

- Execution Queue (node scheduling)
- Execution Clusters (parallel groups)
- Execution Stack (scoped runtime context)
- Memory Bank (runtime state storage)

### Materials System

- External modules defining execution behavior
- Plug-in style extensibility
- Core engine remains minimal and generic

### Core Artifacts

- Data nodes (computation units)
- Execution units (runtime tasks)
- Memory structures (state persistence)

## Design Philosophy

GSAM follows a minimal and explicit design approach:

- Graph-native execution model
- Extensible through external modules
- Minimal assumptions in the core engine
- Clear separation between syntax, execution, and behavior

## Status

GSAM is under active development.  
The architecture and APIs may evolve as the system matures.

## Links

- PyPI: https://pypi.org/project/gsam/
- GitHub: https://github.com/graphscript-labs/gsam
- License: https://github.com/graphscript-labs/gsam/tree/main/LICENSE

---

> _Made with <3 by [AttAditya](https://github.com/AttAditya)_