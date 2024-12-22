import threading
from ecoki.threads_management.threads_manager.threads_manager import ThreadsManager
from ecoki.threads_management.pipeline_thread import PipelineThread
from ecoki.pipeline_framework.pipeline_executor.pipeline_executor import PipelineExecutor

class PipelineThreadManager(ThreadsManager):
    def __init__(self):
        super().__init__()
        self.logger.logger.info("Starting thread manager for pipeline")

    def add_thread(self, thread_name: str, element_executor: PipelineExecutor):
        """
        create a new thread for pipeline/pipeline executor
        :param thread_name: name of the pipeline thread to be added
        :param element_executor: pipeline executor object
        """
        if self.thread_exists(thread_name):
            self.logger.logger.warning(f'Thread of pipeline {thread_name} exists.')
            return False
        else:
            self.logger.logger.info(f'Thread of pipeline {thread_name} is being added.')
            self.monitored_elements[thread_name] = PipelineThread(thread_name, element_executor, self.lock)
            return True

    def run_thread(self, name: str, input=None):
        """
        execute a pipeline thread bz giving its name
        """
        if not self.thread_exists(name): # if a pipeline does not exist
            self.logger.logger.warning(f'Thread of pipeline {name} does not exist')
            return False
        else:
            pipeline_thread = self.monitored_elements[name]
            self.lock.acquire()
            execution_status = pipeline_thread.get_execution_status()
            self.lock.release()
            if execution_status == 1:  # execution is finished
                # if pipeline execution status is 1 (finished), then restart it
                self.lock.acquire()
                pipeline_thread.set_execution_status(-1)
                self.lock.release()
                self.restart_thread(name, pipeline_thread.execution_element)

            elif execution_status == 0:
                # if pipeline execution status is 0 (running), then restart it
                # in the case of restarting a running pipeline
                self.restart_thread(name, pipeline_thread.execution_element)

            elif execution_status == -1:  # pipeline has not been started
                # start a waiting pipeline
                self.lock.acquire()
                pipeline_thread.set_execution_status(0)
                self.lock.release()
                self.logger.logger.info(f' Thread of pipeline {pipeline_thread.name} is being started.')

                pipeline_thread.start()

    def remove_thread(self, thread_name: str):
        """
        remove a pipeline thread by giving the name
        """
        if not self.thread_exists(thread_name):
            self.logger.logger.warning(f'Thread of pipeline {thread_name} does not exist')
            return False
        else:
            try:
                pipeline_thread = self.monitored_elements[thread_name]
                pipeline_thread.execution_element.terminate()  # terminate all panel servers started by visualizers

                for pp_name, pipeline_executor_thread in self.monitored_elements.items():
                    pipeline_executor = pipeline_executor_thread.execution_element
                    for bb_name, bb_executors in pipeline_executor.pipeline_execution.items():
                        bb_executors.building_block.reset_attributes()
                        bb_executors.set_bb_execution_status(-1)

                #if pipeline_thread.get_execution_status() == -1:
                del self.monitored_elements[thread_name]
                #else:
                #    pipeline_thread.stop_thread()
                #    del self.monitored_elements[thread_name]
            except Exception as e:
                self.logger.logger.error(f'Cannot remove pipeline thread {thread_name}')
                self.logger.logger.error(e, exc_info=True)
            else:
                self.logger.logger.info(f'Thread of pipeline {thread_name} has been removed.')
                return True

    def restart_thread(self, thread_name: str, execution_element: PipelineExecutor):
        """restart a pipeline thread, it has to be removed first
        :param thread_name: name of thread to be restarted
        :param execution_element: pipeline executor
        """

        if self.remove_thread(thread_name):
            self.add_thread(thread_name, execution_element)
            for bb_name, bb_executors in execution_element.pipeline_execution.items():
                if bb_executors.interactive_gui:
                    execution_element.port_generator.generated_ports.append(bb_executors.interactive_gui.port)
                if bb_executors.visualizer:
                    execution_element.port_generator.generated_ports.append(bb_executors.visualizer.port)
            self.monitored_elements[thread_name].start()
            self.lock.acquire()
            self.monitored_elements[thread_name].set_execution_status(0)
            self.lock.release()
            self.logger.logger.info(f' Restart thread of pipeline {thread_name}.')
