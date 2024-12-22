from ecoki.pipeline_pool.pipeline_pool_shell import PipelinePoolShell
import argparse


parser = argparse.ArgumentParser(description='pipeline pool host url')
parser.add_argument("--host", type=str, default="127.0.0.1")
parser.add_argument("-p", "--port", type=int, default=5002)


args = parser.parse_args()

host = args.host
port = args.port


def run_pipeline_pool(hostname, port):
    pipeline_pool_shell = PipelinePoolShell(hostname=hostname, port=port)
    pipeline_pool_shell.run()


if __name__ == '__main__':
    run_pipeline_pool(hostname=host, port=port)