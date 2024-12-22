from ecoki.common.base_classes import NodeInformation


def pass_building_block_args(node: NodeInformation):
    """select required parameters from data structure NodeInformation to instantiate building block """
    name = node.name

    return {"name": name, "interactive_settings": node.interactive_configuration}


def pass_local_bb_executor_args(node: NodeInformation):
    """select required parameters from data structure NodeInformation to instantiate building block executor"""
    visualizer_module = node.visualizer_module
    visualizer_class = node.visualizer_class

    return {"visualizer_module": visualizer_module, "visualizer_class": visualizer_class}
