# src/colab_flowchart/flowchart_magic.py

from pyflowchart import Flowchart
from IPython.core.magic import register_cell_magic
from IPython.display import display, HTML

@register_cell_magic
def flowchart(line, cell_code):
    """
    Magic command para generar un diagrama de flujo en Google Colab.
    """
    try:
        # Generar el diagrama de flujo en formato DSL
        flowchart = Flowchart.from_code(cell_code)
        flowchart_dsl = flowchart.flowchart()

        # Plantilla HTML para mostrar el diagrama
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.2.1/raphael.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/flowchart/1.18.0/flowchart.min.js"></script>
        </head>
        <body>
            <h2>Diagrama de flujo generado</h2>
            <div id="diagram"></div>
            <script>
                var diagramCode = `{flowchart_dsl}`;
                try {{
                    var diagram = flowchart.parse(diagramCode);
                    diagram.drawSVG('diagram', {{
                        'x': 0,
                        'y': 0,
                        'line-width': 2,
                        'line-length': 50,
                        'font-size': 14,
                        'font-color': 'black',
                        'line-color': 'black',
                        'fill': 'white',
                        'symbols': {{
                            'start': {{ 'fill': 'green', 'element-color': 'green', 'font-color': 'white' }},
                            'end': {{ 'fill': 'red', 'element-color': 'red', 'font-color': 'white' }}
                        }}
                    }});
                }} catch (err) {{
                    console.error("Error renderizando el diagrama:", err);
                }}
            </script>
        </body>
        </html>
        """
        display(HTML(html_template))  # Muestra el HTML
        exec(cell_code, globals())    # Ejecuta el código en Colab
    except Exception as e:
        print("Error generando el diagrama:", e)