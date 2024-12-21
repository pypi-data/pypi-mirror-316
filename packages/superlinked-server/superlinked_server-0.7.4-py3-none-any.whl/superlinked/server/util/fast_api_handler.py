# Copyright 2024 Superlinked, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import structlog
from beartype.typing import Any
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import Field
from superlinked.framework.common.data_types import NP_PRINT_PRECISION
from superlinked.framework.common.util.immutable_model import ImmutableBaseModel
from superlinked.framework.dsl.executor.rest.rest_handler import RestHandler

logger = structlog.getLogger(__name__)


class QueryResponse(ImmutableBaseModel):
    schema_: str = Field(..., alias="schema")
    results: list[dict[str, Any]]
    metadata: dict[str, Any] | None


class FastApiHandler:
    def __init__(self, rest_handler: RestHandler) -> None:
        self.__rest_handler = rest_handler

    async def ingest(self, request: Request) -> Response:
        payload = await request.json()
        self.__rest_handler._ingest_handler(payload, request.url.path)
        logger.debug("ingested data", path=request.url.path, pii_payload=payload)
        return Response(status_code=status.HTTP_202_ACCEPTED)

    async def query(self, request: Request) -> Response:
        payload = await request.json()
        debug_mode = request.headers.get("x-debug-mode", "false")
        result = self.__rest_handler._query_handler(payload, request.url.path)
        logger.debug(
            "queried data",
            path=request.url.path,
            debug_mode=debug_mode,
            result_entity_count=len(result.entries),
            pii_payload=payload,
            pii_result=result,
        )
        metadata: dict[str, Any] = {}
        if debug_mode.lower() == "true":
            debug_data: dict[str, Any] = {}
            debug_data.update({"knn_params": result.knn_params})
            debug_data.update({"search_vector": [f"{x:.{NP_PRINT_PRECISION}f}" for x in result.search_vector.value]})
            metadata.update({"debug_data": debug_data})

        query_response = QueryResponse(
            schema=result.schema._schema_name,
            metadata=metadata if metadata else None,
            results=[
                {
                    "entity": {
                        "id": entry.entity.header.object_id,
                        "score": entry.entity.score,
                        "origin": (
                            {
                                "id": entry.entity.header.object_id,
                                "schema": entry.entity.header.schema_id,
                            }
                            if entry.entity.header.origin_id
                            else {}
                        ),
                    },
                    "obj": entry.stored_object,
                }
                for entry in result.entries
            ],
        )
        return JSONResponse(
            content=query_response.model_dump(by_alias=True, exclude_none=True),
            status_code=status.HTTP_200_OK,
        )
