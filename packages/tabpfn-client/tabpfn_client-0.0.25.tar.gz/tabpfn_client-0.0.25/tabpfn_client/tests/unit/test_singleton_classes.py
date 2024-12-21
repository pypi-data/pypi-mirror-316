import unittest
import inspect

from tabpfn_client.client import ServiceClient
from tabpfn_client.service_wrapper import (
    UserDataClient,
    UserAuthenticationClient,
    InferenceClient,
)


class TestSingletonClasses(unittest.TestCase):
    def _assert_only_classmethods(self, cls):
        """Helper method to check that a class only defines classmethods"""
        # Get all methods defined in the class
        methods = [
            attr
            for attr in dir(cls)
            if callable(getattr(cls, attr)) and not attr.startswith("_")
        ]

        # Check each method is a classmethod
        for method in methods:
            self.assertTrue(
                inspect.ismethod(getattr(cls, method)),
                f"{cls.__name__}.{method} is not a classmethod",
            )

    def test_service_client_only_has_classmethods(self):
        """Test that ServiceClient only defines classmethods"""
        self._assert_only_classmethods(ServiceClient)

    def test_user_data_client_only_has_classmethods(self):
        """Test that UserDataClient only defines classmethods"""
        self._assert_only_classmethods(UserDataClient)

    def test_user_authentication_client_only_has_classmethods(self):
        """Test that UserAuthenticationClient only defines classmethods"""
        self._assert_only_classmethods(UserAuthenticationClient)

    def test_inference_client_only_has_classmethods(self):
        """Test that InferenceClient only defines classmethods"""
        self._assert_only_classmethods(InferenceClient)
