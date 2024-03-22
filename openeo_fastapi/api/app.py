import attr
from attrs import define, field
from fastapi import APIRouter, HTTPException, Response
from starlette.responses import JSONResponse

from openeo_fastapi.api import responses

HIDDEN_PATHS = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]


@define
class OpenEOApi:
    """Factory for creating FastApi applications conformant to the OpenEO Api specification."""

    client: field
    app: field
    router: APIRouter = attr.ib(default=attr.Factory(APIRouter))
    response_class: type[Response] = attr.ib(default=JSONResponse)

    def register_well_known(self):
        """Register well known page (GET /).


        Returns:
            None
        """
        self.router.add_api_route(
            name=".well-known",
            path="/.well-known/openeo",
            response_model=responses.WellKnownOpeneoGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_well_known,
        )

    def register_get_capabilities(self):
        """Register landing page (GET /).

        Returns:
            None
        """
        self.router.add_api_route(
            name="capabilities",
            path=f"/{self.client.settings.OPENEO_VERSION}" + "/",
            response_model=responses.Capabilities,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_capabilities,
        )

    def register_get_conformance(self):
        """Register conformance page (GET /).
        Returns:
            None
        """
        self.router.add_api_route(
            name="conformance",
            path=f"/{self.client.settings.OPENEO_VERSION}/conformance",
            response_model=responses.ConformanceGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_conformance,
        )

    def register_get_collections(self):
        """Register collection Endpoint (GET /collections).
        Returns:
            None
        """
        self.router.add_api_route(
            name="collections",
            path=f"/{self.client.settings.OPENEO_VERSION}/collections",
            response_model=responses.Collections,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client._collections.get_collections,
        )

    def register_get_collection(self):
        """Register Endpoint for Individual Collection (GET /collections/{collection_id}).
        Returns:
            None
        """
        self.router.add_api_route(
            name="collection",
            path=f"/{self.client.settings.OPENEO_VERSION}"
            + "/collections/{collection_id}",
            response_model=responses.Collection,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client._collections.get_collection,
        )

    def register_get_processes(self):
        """Register Endpoint for Processes (GET /processes).

        Returns:
            None
        """
        self.router.add_api_route(
            name="processes",
            path=f"/{self.client.settings.OPENEO_VERSION}/processes",
            response_model=responses.ProcessesGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client._processes.list_processes,
        )

    def register_get_jobs(self):
        """Register Endpoint for Jobs (GET /jobs).

        Returns:
            None
        """
        self.router.add_api_route(
            name="get_jobs",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs",
            response_model=responses.JobsGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client._jobs.list_jobs,
        )

    def register_post_job(self):
        """Register Endpoint for Jobs (POST /jobs).

        Returns:
            None
        """
        self.router.add_api_route(
            name="post_job",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self.client._jobs.create_job,
        )

    def register_get_job(self):
        """Register Endpoint for Jobs (GET /jobs/{job_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="get_job",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs" + "/{job_id}",
            response_model=responses.BatchJob,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client._jobs.get_job,
        )

    def register_core(self):
        """Register core OpenEO endpoints.

            GET /
            GET /capabilities
            GET /collections
            GET /collections/{collection_id}
            GET /processes
            GET /well_known


        Injects application logic (OpenEOApi.client) into the API layer.

        Returns:
            None
        """
        self.register_get_conformance()
        self.register_get_collections()
        self.register_get_collection()
        self.register_get_processes()
        self.register_get_jobs()
        self.register_post_job()
        self.register_get_job()
        self.register_well_known()

    def http_exception_handler(self, request, exception):
        """Register exception handler to turn python exceptions into expected OpenEO error output."""
        exception_headers = {
            "allow_origin": "*",
            "allow_credentials": "true",
            "allow_methods": "*",
        }
        from fastapi.encoders import jsonable_encoder

        return JSONResponse(
            headers=exception_headers,
            status_code=exception.status_code,
            content=jsonable_encoder(exception.detail),
        )

    def __attrs_post_init__(self):
        """Post-init hook.

        Responsible for setting up the application upon instantiation of the class.

        Returns:
            None
        """

        # Register core endpoints
        self.register_core()

        self.register_get_capabilities()
        self.app.include_router(router=self.router)
        self.app.add_exception_handler(HTTPException, self.http_exception_handler)
