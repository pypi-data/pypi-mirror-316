import uvicorn
from fastapi import FastAPI
from ecoki.pipeline_pool.routers.pipeline_pool_router import PipelinePoolRouter


class PipelinePoolShell:
    def __init__(self, hostname="127.0.0.1", port=5002):
        self.hostname = hostname
        self.port = port
        self.app = FastAPI(title='EcoKI Pipeline Pool Webserver',
                           description='This API provides functionality to manage ecoKI pipelines',
                           version='0.1.0',
                           terms_of_service='Link to Terms of Use',
                           contact={'name': 'name_name', 'url': 'https://google.com/', 'email': 'name@domain.com'},
                           license={'name': 'Apache 2.0', 'url': 'https://www.apache.org/licenses/LICENSE-2.0.html'},)
        self.api_prefix = '/api/v1'
        self._include_routers()

    def _include_routers(self):
        self.app.include_router(PipelinePoolRouter().router, prefix=self.api_prefix)

    def run(self):
        uvicorn.run(self.app, host=self.hostname, port=self.port)

    def terminate(self):
        # Possible solution https://stackoverflow.com/questions/68603658/how-to-terminate-a-uvicorn-fastapi-application-cleanly-with-workers-2-when
        raise NotImplementedError


if __name__=='__main__':
    pipeline_pool = PipelinePoolShell()
    pipeline_pool.run()