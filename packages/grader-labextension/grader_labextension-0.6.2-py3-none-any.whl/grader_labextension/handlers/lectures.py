# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import json
from grader_labextension.registry import register_handler
from grader_labextension.handlers.base_handler import ExtensionBaseHandler, cache
import tornado
from tornado.web import authenticated, HTTPError
from grader_labextension.services.request import RequestService, RequestServiceError


@register_handler(path=r"api\/lectures\/?")
class LectureBaseHandler(ExtensionBaseHandler):
    """
    Tornado Handler class for http requests to /lectures.
    """
    @authenticated
    async def get(self):
        """Sends a GET-request to the grader service and returns the autorized lectures
        """
        query_params = RequestService.get_query_string({
            "complete": self.get_argument("complete", None)
        })
        try:
            response = await self.request_service.request(
                "GET",
                f"{self.service_base_url}api/lectures{query_params}",
                header=self.grader_authentication_header,
                response_callback=self.set_service_headers
            )
        except RequestServiceError as e:
            self.log.error(e)
            raise HTTPError(e.code, reason=e.message)
        self.write(json.dumps(response))

    @authenticated
    async def post(self):
        """Sends a POST-request to the grader service to create a lecture
        """
        data = tornado.escape.json_decode(self.request.body)
        try:
            response = await self.request_service.request(
                "POST",
                f"{self.service_base_url}api/lectures",
                body=data,
                header=self.grader_authentication_header,
            )
        except RequestServiceError as e:
            self.log.error(e)
            raise HTTPError(e.code, reason=e.message)
        self.write(json.dumps(response))


@register_handler(path=r"api\/lectures\/(?P<lecture_id>\d*)\/?")
class LectureObjectHandler(ExtensionBaseHandler):
    """
    Tornado Handler class for http requests to /lectures/{lecture_id}.
    """
    @authenticated
    async def put(self, lecture_id: int):
        """Sends a PUT-request to the grader service to update a lecture

        :param lecture_id: id of the lecture
        :type lecture_id: int
        """

        data = tornado.escape.json_decode(self.request.body)
        try:
            response_data: dict = await self.request_service.request(
                "PUT",
                f"{self.service_base_url}api/lectures/{lecture_id}",
                body=data,
                header=self.grader_authentication_header,
            )
        except RequestServiceError as e:
            self.log.error(e)
            raise HTTPError(e.code, reason=e.message)
        self.write(json.dumps(response_data))

    @authenticated
    async def get(self, lecture_id: int):
        """Sends a GET-request to the grader service and returns the lecture

        :param lecture_id: id of the lecture
        :type lecture_id: int
        """
        try:
            response_data: dict = await self.request_service.request(
                "GET",
                f"{self.service_base_url}api/lectures/{lecture_id}",
                header=self.grader_authentication_header,
                response_callback=self.set_service_headers
            )
        except RequestServiceError as e:
            self.log.error(e)
            raise HTTPError(e.code, reason=e.message)
        self.write(json.dumps(response_data))

    @authenticated
    async def delete(self, lecture_id: int):
        """Sends a DELETE-request to the grader service to delete a lecture

        :param lecture_id: id of the lecture
        :type lecture_id: int
        """

        try:
            await self.request_service.request(
                "DELETE",
                f"{self.service_base_url}api/lectures/{lecture_id}",
                header=self.grader_authentication_header,
            )
        except RequestServiceError as e:
            self.log.error(e)
            raise HTTPError(e.code, reason=e.message)
        self.write({"status": "OK"})


@register_handler(
    path=r"api\/lectures\/(?P<lecture_id>\d*)\/users\/?"
)
class LectureStudentsHandler(ExtensionBaseHandler):
    """
    Tornado Handler class for http requests to /lectures/{lecture_id}/users.
    """
    @authenticated
    async def get(self, lecture_id: int):
        """
        Sends a GET request to the grader service and returns attendants of lecture
        :param lecture_id: id of the lecture
        :return: attendants of lecture
        """
        try:
            response = await self.request_service.request(
                method="GET",
                endpoint=f"{self.service_base_url}api/lectures/{lecture_id}/users",
                header=self.grader_authentication_header,
                response_callback=self.set_service_headers
            )
        except RequestServiceError as e:
            self.log.error(e)
            raise HTTPError(e.code, reason=e.message)

        self.write(json.dumps(response))
