_COUNTER = 0


def display(data, width=800, height=600):
    """Display visualization in IPython notebook via the HTML display hook"""

    global _COUNTER
    from IPython.display import HTML

    h = """
    <script src="d3/d3.min.js"></script>
    <script src="stix2viz.js"></script>

    <svg id='chart{id}' style="width:{width}px;height:{height}px;"></svg>

    <script type="text/javascript">
    chart = $('#chart{id}')[0];
    vizInit(chart, {{"width": {width}, "height": {height}}});
    vizStix({data});
    </script>
    """.format(id=_COUNTER, data=str(data), width=width, height=height)

    _COUNTER += 1
    return HTML(h)
