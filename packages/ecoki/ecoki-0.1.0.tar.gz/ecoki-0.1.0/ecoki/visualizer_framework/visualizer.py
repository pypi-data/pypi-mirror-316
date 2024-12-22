from abc import ABC, abstractclassmethod, abstractmethod


class Visualizer(ABC):
    """
        Base class visualizer for building blocks

        Attributes
        ----------
        visualizer_module: str
            module path of the bb visualizer
        visualizer_class: str
            class name of the bb visualizer
        endpoint: str
            endpoint of the bokeh server
        port: str
            port of the bokeh server
        input_name: dict
            a mapping of visualizer inputs and the outputs of the associated building block
        input_dict: dict
            a dictionary containing the inputs of visualizer
        visualizer: object
            visualizer object
        app: server object
            Visualizer server object
        """

    def __init__(self, visualizer_module, visualizer_class, endpoint, port, input_name):
        self.visualizer_module = visualizer_module
        self.visualizer_class = visualizer_class
        self.endpoint = endpoint
        self.port = port
        self.input_name = input_name
        self.input_dict = {}
        self.visualizer = None
        self.app = None

    def _show_visualizer(self):
        self.app = self.visualizer.show(open=False, threaded=True, address=self.endpoint, port=self.port,
                                        websocket_origin=[f'{self.endpoint}:{self.port}', f'{self.port}.localhost'])

    @abstractmethod
    def run(self, **kwargs):
        pass

    def terminate(self):
        if self.app:
            self.app.stop()
