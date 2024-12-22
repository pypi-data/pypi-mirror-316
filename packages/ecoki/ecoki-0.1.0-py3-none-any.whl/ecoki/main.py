from ecoki.shell.rest_api_shell import RestAPIShell
from ecoki.pipeline_framework.pipeline_manager.pipeline_manager import PipelineManager
from ecoki.pipeline_framework.pipeline_manager.port_number_counter import PortNumberCounter
import argparse

parser = argparse.ArgumentParser(description='host url')
parser.add_argument("--host", type=str, default="127.0.0.1")
parser.add_argument("-p", "--port", type=int, default=5000)
parser.add_argument("-pph", "--pipeline_pool_host", type=str, default="127.0.0.1")
parser.add_argument("-ppp", "--pipeline_pool_port", type=int, default=5002)

args = parser.parse_args()

host = args.host
port = args.port

pipeline_pool_host = args.pipeline_pool_host
pipeline_pool_port = args.pipeline_pool_port

def run_application(hostname, port):
    port_generator = PortNumberCounter()
    pipeline_manager = PipelineManager(port_generator=port_generator, host=hostname)
    shell = RestAPIShell(pipeline_manager=pipeline_manager, hostname=hostname, port=port,
                         pipeline_pool_hostname=pipeline_pool_host,
                         pipeline_pool_port=pipeline_pool_port)

    shell.run()


if __name__ == '__main__':
    run_application(hostname=host, port=port)