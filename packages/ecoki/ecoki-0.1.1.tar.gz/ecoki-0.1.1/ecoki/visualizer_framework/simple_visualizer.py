from ecoki.visualizer_framework.visualizer import Visualizer
import panel as pn


class SimpleVisualizer(Visualizer):
    """
        class SimpleVisualizer, inherits from the base class Visualizer

        Attributes
        ----------
        app:
            bokeh server object
        """
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.app = None

    def run(self):
        """
        start a bokeh for visualization
        """
        self.terminate()
        dashboard = pn.template.MaterialTemplate(site="ecoKI", title="Simple Visualizer")
        self.app = dashboard.show(open=False, threaded=True, port=self.port, websocket_origin=f'127.0.0.1:{self.port}')
    
    def terminate(self):
        """
        terminate a running bokeh server
        """
        if self.app:
            self.app.stop()