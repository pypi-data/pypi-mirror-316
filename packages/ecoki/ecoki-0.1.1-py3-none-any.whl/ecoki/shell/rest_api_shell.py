import uvicorn
from fastapi import FastAPI
from ecoki.shell.routers.building_block_router import BuildingBlockRouter
from ecoki.shell.routers.pipeline_router import PipelineRouter
from ecoki.shell.routers.pipeline_manager_router import PipelineManagerRouter
from ecoki.pipeline_framework.pipeline_manager.pipeline_manager import PipelineManager


class RestAPIShell:
    def __init__(self, pipeline_manager, hostname: str = '0.0.0.0', port: int = 5000,
                 pipeline_pool_hostname: str = '0.0.0.0',
                 pipeline_pool_port: int = 5002):
        self.pipeline_manager = pipeline_manager
        self.hostname = hostname
        self.port = port
        self.pipeline_pool_hostname = pipeline_pool_hostname
        self.pipeline_pool_port = pipeline_pool_port

        self.app = FastAPI(title='EcoKI Rest API Webserver',
                           description='This API provides functionality to work with the ecoKI platform instance using REST API',
                           version='0.1.0',
                           terms_of_service='Link to Terms of Use',
                           contact={'name': 'name_name', 'url': 'https://google.com/', 'email': 'name@domain.com'},
                           license={'name': 'Apache 2.0', 'url': 'https://www.apache.org/licenses/LICENSE-2.0.html'}, )
        self.api_prefix = '/api/v1'
        self._include_routers()

    def _include_routers(self):
        self.app.include_router(
            PipelineManagerRouter(self.pipeline_manager, self.pipeline_pool_hostname, self.pipeline_pool_port).router,
            prefix=self.api_prefix)
        self.app.include_router(
            PipelineRouter(self.pipeline_manager, self.pipeline_pool_hostname, self.pipeline_pool_port).router,
            prefix=self.api_prefix)
        self.app.include_router(BuildingBlockRouter(self.pipeline_manager).router, prefix=self.api_prefix)

    def run(self):
        uvicorn.run(self.app, host=self.hostname, port=self.port)

    def terminate(self):
        # Possible solution https://stackoverflow.com/questions/68603658/how-to-terminate-a-uvicorn-fastapi-application-cleanly-with-workers-2-when
        raise NotImplementedError


if __name__ == '__main__':
    restapi = RestAPIShell(PipelineManager())
    restapi.run()
