# colab-flowchart

Una librería para Google Colab que permite generar diagramas de flujo con el magic `%%flowchart`.

## Instalación

```bash
pip install colab-flowchart
```

## Uso

```python
from flowchart_magic import flowchart

# Habilita el magic
%load_ext flowchart_magic.flowchart_magic

%%flowchart
def ejemplo():
    x = 10
    if x > 5:
        print("x es mayor que 5")
    else:
        print("x no es mayor que 5")
```



