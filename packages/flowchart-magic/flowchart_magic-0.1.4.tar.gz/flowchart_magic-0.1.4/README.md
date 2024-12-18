# flowchart-magic

A library for "Jupyter Notebook" / "Google Colab" that allows generating flowcharts using the `%%flowchart` magic command.

## Installation

```bash
pip install flowchart_magic
```

## Usage

Import:

```python
from flowchart_magic import flowchart

# Enable the magic
%load_ext flowchart_magic.flowchart_magic
```

Example:

```
%%flowchart
def example():
    x = 10
    if x > 5:
        print("x is greater than 5")
    else:
        print("x is not greater than 5")
```

## Example Output

Install and import:
![Example Flowchart](assets/install_import.png)

Example code:
![Example Flowchart](assets/example_jupyter.png)

## Acknowledgments
This project is inspired by and builds upon the original [pyflowchart](https://pypi.org/project/pyflowchart/) project and [flowchart.js](https://flowchart.js.org/). Many thanks to its contributors for their work!

