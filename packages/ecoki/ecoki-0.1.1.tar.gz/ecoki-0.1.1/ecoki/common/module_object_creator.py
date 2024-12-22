import importlib
from enum import Enum


def create_object_by_module(module_path, class_name, **kwargs):
    """
    Instantiate class according to the given module path, class name and parameters
   :param: module_path: module path of the class
   :param: class_name: class name
   :param: parameters required to instantiate a class
    """
    object_class = getattr(importlib.import_module(module_path), class_name)
    obj = object_class(**kwargs)

    return obj


class ExecutorModule(Enum):
    local_bb_executor_module = "ecoki.building_block_framework.building_block_executor.local_building_block_executor"
    local_bb_executor_class = "LocalBuildingBlockExecutor"
    loop_bb_executor_module = "ecoki.building_block_framework.building_block_executor.loop_building_block_executor"
    loop_bb_executor_class = "LoopBuildingBlockExecutor"

    local_pipeline_executor_module = "ecoki.pipeline_framework.pipeline_executor.local_pipeline_executor"
    local_pipeline_executor_class = "LocalPipelineExecutor"
    loop_pipeline_executor_module = "ecoki.pipeline_framework.pipeline_executor.loop_pipeline_executor"
    loop_pipeline_executor_class = "LoopPipelineExecutor"



def create_executors(execution_mode, execution_type, **kwargs):
    if execution_mode == "local":
        if execution_type == "building_block":
            executor_module = ExecutorModule.local_bb_executor_module.value
            executor_class = ExecutorModule.local_bb_executor_class.value

        elif execution_type == "pipeline":
            executor_module = ExecutorModule.local_pipeline_executor_module.value
            executor_class = ExecutorModule.local_pipeline_executor_class.value
        else:
            raise KeyError

    elif execution_mode == "loop":
        if execution_type == "building_block":
            executor_module = ExecutorModule.loop_bb_executor_module.value
            executor_class = ExecutorModule.loop_bb_executor_class.value
        elif execution_type == "pipeline":
            executor_module = ExecutorModule.loop_pipeline_executor_module.value
            executor_class = ExecutorModule.loop_pipeline_executor_class.value
        else:
            raise KeyError

    else:
        raise KeyError

    executor_obj = create_object_by_module(executor_module, executor_class, execution_mode=execution_mode, **kwargs)
    return executor_obj



