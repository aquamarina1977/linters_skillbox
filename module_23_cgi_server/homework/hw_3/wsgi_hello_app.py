import json
from typing import Callable, Dict
from wsgiref.simple_server import make_server
import re


class WSGIApp:
    def init(self):
        self.routes: Dict[str, Callable] = {}

    def add_route(self, path: str):
        """ Декоратор для регистрации маршрутов """
        def decorator(func: Callable):
            if not hasattr(self, "routes"):
                self.routes = {}
            self.routes[path] = func
            return func

        return decorator

    def call(self, environ, start_response):
        path = environ.get("PATH_INFO", "").rstrip("/")
        response_body = json.dumps({"error": "Not Found"}, indent=4)
        status = "404 Not Found"
        headers = [("Content-Type", "application/json")]

        for route, func in self.routes.items():
            match = re.fullmatch(route.replace("<name>", "(?P<name>[^/]+)"), path)
            if match:
                response_body = func(**match.groupdict())
                status = "200 OK"
                break

        start_response(status, headers)
        return [response_body.encode("utf-8")]


app = WSGIApp()


@app.add_route("/hello")
def say_hello():
    return json.dumps({"response": "Hello, world!"}, indent=4)


@app.add_route("/hello/<name>")
def say_hello_with_name(name: str):
    return json.dumps({"response": f"Hello, {name}!"}, indent=4)


if __name__ == "main":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()