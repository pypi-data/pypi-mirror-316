from threading import Thread
import threading
from ecoki.log_factory.local_log_handler import LocalLogHandler
import os
import inspect
import ctypes
from ecoki.common.status_code import Status

def _async_raise(tid, exctype):
    """Raises an exception in the threads to terminate it"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
                                                     ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class PipelineThread(Thread):
    def __init__(self, name, execution_element, lock):
        super().__init__()
        self.name = name
        self.execution_element = execution_element
        self.lock = lock
        self.logger = LocalLogHandler(f'pipeline thread: {self.__class__.__name__}.{name}.{id(self)}')

    def set_execution_status(self, execution_status: int):
        """
        set execution status for pipeline executor
        :param execution_status:
            -1: to be execute
            0: is running
            1: execution is finished
        """
        self.execution_element.set_pipeline_execution_status(execution_status)
        return True

    def get_execution_status(self):
        """
        get pipeline execution status
        """
        return self.execution_element.get_pipeline_execution_status()

    def run(self):
        """
        execute pipeline by calling the run method of pipeline executor
        after the pipeline execution is finished, set its execution status to 1
        """
        self.logger.logger.info(f" Pipeline {self.name} is running in the thread {threading.current_thread().name}")
        try:
            self.execution_element.run()  # run pipeline executor

        except Exception as e:  # if an exception is raised --> set status to failure
            self.lock.acquire()
            self.set_execution_status(Status.FAILURE.value)  # failure
            self.lock.release()
            self.logger.logger.error(f'Cannot execute pipeline {self.name}')
            self.logger.logger.error(e, exc_info=True)
        else:
            self.lock.acquire()
            for bb_executor in self.execution_element.pipeline_execution.values():
                if bb_executor.get_bb_execution_status() == Status.FAILURE.value:
                    self.set_execution_status(Status.FAILURE.value)
                    self.lock.release()
                    return
            self.set_execution_status(Status.FINISHED.value)  # execution is finished
            self.lock.release()

    def stop_thread(self):
        """
        stop a pipeline thread by raising an error in a running thread
        """
        _async_raise(self.ident, SystemExit)

    def __del__(self):
        # del self.execution_element.pipeline
        print(f'Pipeline Thread {self.name} has been destroyed')

