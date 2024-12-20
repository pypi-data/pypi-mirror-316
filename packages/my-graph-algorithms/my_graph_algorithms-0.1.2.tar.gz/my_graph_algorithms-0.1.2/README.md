# Graphs

A Python package for graph algorithms, including a Floyd-Warshall implementation.

## Installation

Install the package using pip:

```bash
pip install my-graph-algorithms



## Useage
```python
from graphs.floyd_warshall_bidirectional import floyd_warshall_bidirectional

# Example usage
graph = [[0, 3, float('inf')], [float('inf'), 0, 1], [float('inf'), float('inf'), 0]]
result = floyd_warshall_bidirectional(graph)
print(result)


