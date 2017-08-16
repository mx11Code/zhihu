from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.http import JsonResponse


class DictToJsonResponse(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        return None

    @staticmethod
    def process_response(request, data):

        if not isinstance(data, dict):
            return data

        data_to_response = data
        if not data:
            data = {"success": False, "http_status_code": 404}

        if isinstance(data, list):
            data = {}

        success = data.get("success", True)
        data.pop("success", True)

        http_status_code = data.get("http_status_code", 200)
        data.pop("http_status_code", True)

        return JsonResponse({"success": success, "data": data_to_response}, status=http_status_code)
