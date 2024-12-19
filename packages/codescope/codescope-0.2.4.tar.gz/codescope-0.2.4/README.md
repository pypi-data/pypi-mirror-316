# Scope

<!--Scope lets you statically extract and query call graphs from a codebase.-->
**A call graph generator designed for codebase RAG.** Uses a combination of LSP and AST parsing to achieve very high accuracy, even for dynamic languages.

* Supports 6+ popular languages
  * JavaScript
  * Python
  * TypeScript
  * Rust
  * C#
  * Java
* Can be used programmatically or via the command-line
* Provides easy retrieval methods (e.g. `get_definition`, `get_references`, `get_call_stack`, etc.)

Built in collaboration with Microsoft Research.

## Install

```bash
> pip install codescope
```

```bash
> uv add codescope
```

## Usage

TODO

## Development

To run tests:
```pytest tests/scope```

## License

Apache 2.0
