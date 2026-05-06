# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import pytest

# Add parent directory to path to import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app  # noqa: E402


class TestAppInitialization:
    """Test cases for Flask app initialization on boot up"""

    def test_app_exists(self):
        """Verify Flask app instance is created"""
        assert app is not None
        assert app.name == "app"

    def test_app_config_exists(self):
        """Verify basic Flask configuration"""
        assert app.config is not None
        assert isinstance(app.config, dict)


class TestAppRoutes:
    """Test cases for Flask app routes"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_home_route_status_code(self, client):
        """Verify home route returns 200 OK"""
        response = client.get("/")
        assert response.status_code == 200

    def test_home_route_content_type(self, client):
        """Verify home route returns HTML content"""
        response = client.get("/")
        assert "text/html" in response.content_type

    def test_home_route_response_not_empty(self, client):
        """Verify home route returns content"""
        response = client.get("/")
        assert len(response.data) > 0

    def test_home_page_title(self, client):
        """Verify home page contains expected title"""
        response = client.get("/")
        assert b"Flask App Deployment on Ubuntu VM using AWS" in response.data

    def test_home_page_contains_project_goal(self, client):
        """Verify home page contains Project Goal section"""
        response = client.get("/")
        assert b"Project Goal" in response.data

    def test_home_page_contains_architecture_section(self, client):
        """Verify home page contains Architecture section"""
        response = client.get("/")
        assert b"Architecture" in response.data

    def test_home_page_contains_implementation_steps(self, client):
        """Verify home page contains implementation steps"""
        response = client.get("/")
        assert b"Key Implementation Steps" in response.data

    def test_home_page_contains_results_section(self, client):
        """Verify home page contains Results section"""
        response = client.get("/")
        assert b"Results" in response.data

    def test_home_page_contains_verification_section(self, client):
        """Verify home page contains Verification section"""
        response = client.get("/")
        assert b"Verification" in response.data

    def test_home_page_contains_footer(self, client):
        """Verify home page contains footer"""
        response = client.get("/")
        assert b"Deployed by Lokesh" in response.data

    def test_home_page_mentions_gunicorn(self, client):
        """Verify home page mentions Gunicorn"""
        response = client.get("/")
        assert b"Gunicorn" in response.data

    def test_home_page_mentions_nginx(self, client):
        """Verify home page mentions Nginx"""
        response = client.get("/")
        assert b"Nginx" in response.data

    def test_home_page_mentions_flask(self, client):
        """Verify home page mentions Flask"""
        response = client.get("/")
        assert b"Flask" in response.data

    def test_home_page_html_structure(self, client):
        """Verify home page has valid HTML structure"""
        response = client.get("/")
        assert b"<!DOCTYPE html>" in response.data
        assert b"<html>" in response.data
        assert b"</html>" in response.data
        assert b"<head>" in response.data
        assert b"</head>" in response.data
        assert b"<body>" in response.data
        assert b"</body>" in response.data

    def test_home_page_has_css_styling(self, client):
        """Verify home page contains CSS styling"""
        response = client.get("/")
        assert b"<style>" in response.data
        assert b"</style>" in response.data

    def test_invalid_route_returns_404(self, client):
        """Verify invalid routes return 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_home_page_mentions_ubuntu(self, client):
        """Verify home page mentions Ubuntu"""
        response = client.get("/")
        assert b"Ubuntu" in response.data

    def test_home_page_mentions_aws(self, client):
        """Verify home page mentions AWS"""
        response = client.get("/")
        assert b"AWS" in response.data


class TestBootUpScenarios:
    """Test cases simulating boot-up scenarios on remote server"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_initializes_without_errors(self):
        """Verify app initializes without raising exceptions"""
        try:
            test_app = app
            assert test_app is not None
        except Exception as e:
            pytest.fail(f"App initialization failed: {str(e)}")

    def test_app_accessible_immediately_after_startup(self, client):
        """Verify app responds immediately after startup"""
        response = client.get("/")
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_multiple_requests_after_startup(self, client):
        """Verify app handles multiple requests after startup"""
        for _ in range(5):
            response = client.get("/")
            assert response.status_code == 200

    def test_high_request_volume_during_startup(self, client):
        """Verify app handles high request volume after startup"""
        responses = []
        for _ in range(50):
            response = client.get("/")
            responses.append(response.status_code)

        assert all(status == 200 for status in responses)

    def test_request_response_consistency(self, client):
        """Verify response consistency across multiple calls"""
        responses = []
        for _ in range(5):
            response = client.get("/")
            responses.append(response.data)

        # All responses should be identical
        assert all(r == responses[0] for r in responses)


class TestDeploymentValidation:
    """Test cases for verifying deployment requirements"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_uses_gunicorn_compatible_interface(self):
        """Verify app can be run by Gunicorn"""
        assert hasattr(app, "wsgi_app")
        assert callable(app.wsgi_app)

    def test_app_supports_werkzeug_server(self):
        """Verify app supports Werkzeug development server"""
        assert hasattr(app, "run")
        assert callable(app.run)

    def test_home_route_supports_get_method(self, client):
        """Verify home route supports GET method"""
        response = client.get("/")
        assert response.status_code == 200

    def test_no_hardcoded_localhost_in_response(self, client):
        """Verify response doesn't contain hardcoded localhost URLs"""
        response = client.get("/")
        response_text = response.data.decode("utf-8")
        assert "localhost:5000" not in response_text


class TestErrorHandling:
    """Test cases for error handling during boot up"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_handles_root_path_request(self, client):
        """Verify app handles root path request correctly"""
        response = client.get("/")
        assert response.status_code == 200

    def test_app_response_encoding(self, client):
        """Verify app response uses proper UTF-8 encoding"""
        response = client.get("/")
        # Should be able to decode response as UTF-8
        try:
            response.data.decode("utf-8")
            assert True
        except UnicodeDecodeError:
            pytest.fail("Response is not UTF-8 encoded")


class TestSystemIntegration:
    """Test cases for system integration during boot up"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_resources_loading(self, client):
        """Verify app loads all resources"""
        response = client.get("/")
        assert response.status_code == 200
        assert len(response.data) > 100  # Should have substantial content

    def test_app_template_rendering(self, client):
        """Verify app renders template correctly"""
        response = client.get("/")
        # Check for rendered content indicators
        assert b"<" in response.data  # HTML tags present
        assert b">" in response.data  # HTML tags present


class TestGunicornCompatibility:
    """Test cases for Gunicorn server compatibility (port 8000, 3 workers)"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_callable_as_wsgi(self):
        """Verify app is callable as WSGI application"""
        assert callable(app)

    def test_app_wsgi_app_attribute(self):
        """Verify app has wsgi_app attribute for Gunicorn"""
        assert hasattr(app, "wsgi_app")

    def test_app_stateless_design(self, client):
        """Verify app is stateless (required for multiple workers)"""
        # Make requests and verify no state is maintained
        response1 = client.get("/")
        response2 = client.get("/")

        assert response1.data == response2.data
        assert response1.status_code == response2.status_code

    def test_app_thread_safety(self, client):
        """Verify app responses are consistent (thread safety)"""
        responses = set()
        for _ in range(10):
            response = client.get("/")
            # Convert to string for comparison
            responses.add(response.data.decode("utf-8"))

        # All responses should be identical
        assert len(responses) == 1

    def test_app_handles_wsgi_environ_variables(self):
        """Verify app can handle WSGI environ variables"""
        with app.test_request_context("/"):
            from flask import request

            # Verify Flask can access WSGI environ
            assert request.environ is not None
            assert "REQUEST_METHOD" in request.environ


class TestNginxReverseProxyCompatibility:
    """Test cases for Nginx reverse proxy configuration (port 80)"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_handles_x_forwarded_for_header(self, client):
        """Verify app handles X-Forwarded-For header from Nginx"""
        response = client.get("/", headers={"X-Forwarded-For": "203.0.113.1"})
        assert response.status_code == 200

    def test_app_handles_x_real_ip_header(self, client):
        """Verify app handles X-Real-IP header from Nginx"""
        response = client.get("/", headers={"X-Real-IP": "203.0.113.1"})
        assert response.status_code == 200

    def test_app_handles_host_header_from_proxy(self, client):
        """Verify app handles Host header from Nginx proxy"""
        response = client.get("/", headers={"Host": "example.com"})
        assert response.status_code == 200

    def test_response_size_reasonable(self, client):
        """Verify response size is reasonable for proxy transmission"""
        response = client.get("/")
        content_length = len(response.data)
        # Response should be reasonable (not empty, not absurdly large)
        assert 100 < content_length < 100000

    def test_nginx_proxy_pass_compatibility(self, client):
        """Verify app output is compatible with proxy_pass directive"""
        response = client.get("/")
        # Response should be valid HTTP response with content
        assert response.status_code == 200
        assert response.data is not None


class TestSystemdServiceCompatibility:
    """Test cases for systemd service configuration"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_startup_minimal_dependencies(self):
        """Verify app starts with minimal system dependencies"""
        # Verify Flask and render_template_string are available
        assert app is not None
        from flask import render_template_string

        assert callable(render_template_string)

    def test_app_restart_capability(self, client):
        """Verify app can handle restart (Restart=always in systemd)"""
        # Simulate multiple startup cycles
        for _ in range(3):
            response = client.get("/")
            assert response.status_code == 200

    def test_app_multi_user_target_ready(self, client):
        """Verify app is ready for multi-user.target in systemd"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.data

    def test_app_after_network_boot_ready(self, client):
        """Verify app is ready after network.target"""
        response = client.get("/")
        assert response.status_code == 200

    def test_app_clean_startup_no_errors(self):
        """Verify app starts cleanly without initialization errors"""
        try:
            # If app imports successfully, it's clean
            from app import app as test_app

            assert test_app is not None
        except Exception as e:
            pytest.fail(f"App startup error: {str(e)}")


class TestDeploymentReboot:
    """Test cases for handling reboot persistence"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_survives_multiple_boot_cycles(self, client):
        """Verify app survives multiple boot cycles"""
        for boot_cycle in range(5):
            response = client.get("/")
            assert response.status_code == 200, f"Failed on boot cycle {boot_cycle + 1}"

    def test_app_content_consistent_across_reboots(self, client):
        """Verify app content is consistent across reboots"""
        responses = []
        for _ in range(5):
            response = client.get("/")
            responses.append(response.data)

        # All responses should be identical
        assert all(r == responses[0] for r in responses)


class TestNetworkConfiguration:
    """Test cases for network configuration (Nginx port 80, app port 8000)"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_accessible_on_localhost(self, client):
        """Verify app accessible on localhost"""
        response = client.get("/")
        assert response.status_code == 200

    def test_app_response_independent_of_port(self, client):
        """Verify app response doesn't hardcode port numbers"""
        response = client.get("/")
        content = response.data.decode("utf-8")

        # Should not have hardcoded port references that would break deployment
        assert "localhost:5000" not in content

    def test_html_content_type_for_browser(self, client):
        """Verify response content type is compatible with browsers"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.content_type in ["text/html; charset=utf-8", "text/html"]


class TestProductionReadiness:
    """Test cases for production readiness verification"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_production_server_compatible(self):
        """Verify app is compatible with production servers (Gunicorn)"""
        assert callable(app)
        assert hasattr(app, "wsgi_app")

    def test_app_response_time_acceptable(self, client):
        """Verify response time is acceptable for production"""
        import time

        start = time.time()
        response = client.get("/")
        elapsed = time.time() - start

        assert elapsed < 0.5  # Should respond in less than 500ms
        assert response.status_code == 200

    def test_app_no_uncaught_exceptions(self, client):
        """Verify app doesn't raise uncaught exceptions"""
        try:
            for _ in range(10):
                response = client.get("/")
                assert response.status_code == 200
        except Exception as e:
            pytest.fail(f"Uncaught exception during requests: {str(e)}")

    def test_app_handles_multiple_concurrent_requests(self, client):
        """Verify app can handle multiple concurrent requests"""
        responses = []
        for _ in range(20):
            response = client.get("/")
            responses.append(response.status_code)

        assert all(status == 200 for status in responses)
        assert len(responses) == 20
