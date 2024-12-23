# projectmanagement
A Python library for creating and exporting project management network diagrams, including critical path visualization, using `pandas` and `xlsxwriter`.

## Installation

Install via pip:

```bash
pip install projectmanagement


---

### Import Classes

```python
from projectmanagement import NetworkDiagram, NetworkDiagramExporter
import pandas as pd

# Create example data
data = {
    'Activity': ['A', 'B', 'C'],
    'Duration': [5, 3, 7],
    'ES': [0, 5, 8],
    'EF': [5, 8, 15],
    'Slack': [0, 0, 0],
    'LS': [0, 5, 8],
    'LF': [5, 8, 15],
}

df = pd.DataFrame(data)

# Create a NetworkDiagram
network_diagram = NetworkDiagram(df)

# Export to Excel
exporter = NetworkDiagramExporter(network_diagram, "output.xlsx")
exporter.export()
print("Network Diagram exported successfully!")

```

---
## **5. Features**
Highlight the features of your package:

markdown
## Features
- Create network diagrams for project management
- Export formatted network diagrams to Excel
- Highlight activities with zero slack (critical path) in orange
- Easy integration with `pandas`

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.