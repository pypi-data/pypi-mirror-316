from http import HTTPStatus
from unittest import TestCase

from artless import Response


class TestResponse(TestCase):
    def test_repr(self):
        self.assertEqual(repr(Response()), "<Response: 200 OK>")

    def test_add_new_header(self):
        response = Response()
        self.assertDictEqual(response.headers, {"Content-Type": "text/plain"})

        response.headers["Set-Cookie"] = "userId=67890; Secure; HttpOnly"

        self.assertDictEqual(
            response.headers,
            {"Content-Type": "text/plain", "Set-Cookie": "userId=67890; Secure; HttpOnly"},
        )

    def test_replace_existing_header(self):
        response = Response()
        self.assertDictEqual(response.headers, {"Content-Type": "text/plain"})

        response.headers["Content-Type"] = "application/json"

        self.assertDictEqual(response.headers, {"Content-Type": "application/json"})

    def test_getting_headers_property_with_default_values(self):
        # Create Response object with default headers
        response = Response()
        self.assertDictEqual(response.headers, {"Content-Type": "text/plain"})

    def test_getting_status_property_with_default_value(self):
        # Create Response object with default status
        response = Response()
        self.assertTrue(response.status)
        self.assertEqual(response.status, "200 OK")

    def test_getting_status_property_with_custom_value(self):
        response = Response(status=HTTPStatus.NO_CONTENT)
        self.assertEqual(response.status, "204 No Content")

    def test_setting_status_property(self):
        response = Response()
        # Default status value
        self.assertEqual(response.status, "200 OK")

        # Set new status value
        response.status = HTTPStatus.CREATED

        self.assertEqual(response.status, "201 Created")

    def test_getting_content_type_property_with_default_value(self):
        # Create Response object with default content_type
        response = Response()
        self.assertTrue(response.content_type)
        self.assertEqual(response.content_type, "text/plain")

    def test_setting_content_type_property(self):
        response = Response()
        # Default content_type value
        self.assertEqual(response.content_type, "text/plain")

        # Set a new value of content_type
        response.content_type = "application/json"
        self.assertEqual(response.content_type, "application/json")

    def test_body_property(self):
        response = Response()

        # Set body as a string
        response.body = "regular string"
        # Regular string serialized to bytes
        self.assertEqual(response.body, b"regular string\n")

        # Set body as a bytes string
        response.body = b"native strings"
        self.assertEqual(response.body, b"native strings\n")

        # Trying to set the response body to something other than a string
        # (or byte string) will rise exception.
        with self.assertRaises(TypeError) as exc:
            response.body = {"some": "data"}
        self.assertEqual(
            str(exc.exception), "Response body must be only string or bytes, not <class 'dict'>"
        )
