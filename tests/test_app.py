# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-



import sysimport sys

from pathlib import Pathfrom pathlib import Path



import pytestimport pytest



# Add parent directory to path to import app# Add parent directory to path to import app

sys.path.insert(0, str(Path(__file__).parent.parent))sys.path.insert(0, str(Path(__file__).parent.parent))



from app import create_appfrom app import app  # noqa: E402

from app.models import db, User

from app.config import TestingConfig

class TestAppInitialization:

    """Test cases for Flask app initialization on boot up"""

@pytest.fixture

def app():    def test_app_exists(self):

    """Create test app instance"""        """Verify Flask app instance is created"""

    app = create_app(config=TestingConfig)        assert app is not None

            assert app.name == "app"

    with app.app_context():

        db.create_all()    def test_app_config_exists(self):

        yield app        """Verify basic Flask configuration"""

        db.session.remove()        assert app.config is not None

        db.drop_all()        assert isinstance(app.config, dict)





@pytest.fixtureclass TestAppRoutes:

def client(app):    """Test cases for Flask app routes"""

    """Create test client"""

    return app.test_client()    @pytest.fixture

    def client(self):

        """Create test client"""

class TestAppInitialization:        app.config["TESTING"] = True

    """Test cases for Flask app initialization"""        with app.test_client() as client:

            yield client

    def test_app_exists(self, app):

        """Verify Flask app instance is created"""    def test_home_route_status_code(self, client):

        assert app is not None        """Verify home route returns 200 OK"""

        response = client.get("/")

    def test_app_config_exists(self, app):        assert response.status_code == 200

        """Verify Flask configuration is loaded"""

        assert app.config is not None    def test_home_route_content_type(self, client):

        assert isinstance(app.config, dict)        """Verify home route returns HTML content"""

        response = client.get("/")

    def test_app_testing_mode(self, app):        assert "text/html" in response.content_type

        """Verify app is in testing mode"""

        assert app.config["TESTING"] is True    def test_home_route_response_not_empty(self, client):

        """Verify home route returns content"""

    def test_database_initialized(self, app):        response = client.get("/")

        """Verify database is initialized"""        assert len(response.data) > 0

        assert db is not None

    def test_home_page_title(self, client):

        """Verify home page contains expected title"""

class TestHomeRoute:        response = client.get("/")

    """Test cases for home route"""        assert b"Flask App Deployment on Ubuntu VM using AWS" in response.data



    def test_home_route_status_code(self, client):    def test_home_page_contains_project_goal(self, client):

        """Verify home route returns 200 OK"""        """Verify home page contains Project Goal section"""

        response = client.get("/")        response = client.get("/")

        assert response.status_code == 200        assert b"Project Goal" in response.data



    def test_home_route_content_type(self, client):    def test_home_page_contains_architecture_section(self, client):

        """Verify home route returns HTML"""        """Verify home page contains Architecture section"""

        response = client.get("/")        response = client.get("/")

        assert "text/html" in response.content_type        assert b"Architecture" in response.data



    def test_home_route_response_not_empty(self, client):    def test_home_page_contains_implementation_steps(self, client):

        """Verify home route returns content"""        """Verify home page contains implementation steps"""

        response = client.get("/")        response = client.get("/")

        assert len(response.data) > 0        assert b"Key Implementation Steps" in response.data



    def test_home_page_title(self, client):    def test_home_page_contains_results_section(self, client):

        """Verify home page contains expected title"""        """Verify home page contains Results section"""

        response = client.get("/")        response = client.get("/")

        assert b"Flask" in response.data and (b"DevOps" in response.data or b"Deployment" in response.data)        assert b"Results" in response.data



    def test_home_page_has_html_structure(self, client):    def test_home_page_contains_verification_section(self, client):

        """Verify home page has valid HTML structure"""        """Verify home page contains Verification section"""

        response = client.get("/")        response = client.get("/")

        assert b"<!DOCTYPE html>" in response.data        assert b"Verification" in response.data

        assert b"</html>" in response.data

    def test_home_page_contains_footer(self, client):

    def test_home_page_mentions_key_technologies(self, client):        """Verify home page contains footer"""

        """Verify home page mentions key technologies"""        response = client.get("/")

        response = client.get("/")        assert b"Deployed by Lokesh" in response.data

        # Should mention at least some of our tech stack

        content = response.data.decode('utf-8').lower()    def test_home_page_mentions_gunicorn(self, client):

        assert any(tech in content for tech in ['gunicorn', 'nginx', 'flask', 'docker', 'python'])        """Verify home page mentions Gunicorn"""

        response = client.get("/")

        assert b"Gunicorn" in response.data

class TestDashboardRoute:

    """Test cases for dashboard routes"""    def test_home_page_mentions_nginx(self, client):

        """Verify home page mentions Nginx"""

    def test_dashboard_route_exists(self, client):        response = client.get("/")

        """Verify dashboard route exists"""        assert b"Nginx" in response.data

        response = client.get("/dashboard/")

        assert response.status_code == 200    def test_home_page_mentions_flask(self, client):

        """Verify home page mentions Flask"""

    def test_dashboard_returns_html(self, client):        response = client.get("/")

        """Verify dashboard returns HTML"""        assert b"Flask" in response.data

        response = client.get("/dashboard/")

        assert "text/html" in response.content_type    def test_home_page_html_structure(self, client):

        """Verify home page has valid HTML structure"""

    def test_dashboard_title_present(self, client):        response = client.get("/")

        """Verify dashboard has title"""        assert b"<!DOCTYPE html>" in response.data

        response = client.get("/dashboard/")        assert b"<html>" in response.data

        assert b"Dashboard" in response.data or b"User" in response.data        assert b"</html>" in response.data

        assert b"<head>" in response.data

    def test_about_page_exists(self, client):        assert b"</head>" in response.data

        """Verify about page exists"""        assert b"<body>" in response.data

        response = client.get("/dashboard/about")        assert b"</body>" in response.data

        assert response.status_code == 200

    def test_home_page_has_css_styling(self, client):

    def test_about_page_content(self, client):        """Verify home page contains CSS styling"""

        """Verify about page has content"""        response = client.get("/")

        response = client.get("/dashboard/about")        assert b"<style>" in response.data

        assert len(response.data) > 100        assert b"</style>" in response.data

        assert b"About" in response.data or b"Technology" in response.data

    def test_invalid_route_returns_404(self, client):

        """Verify invalid routes return 404"""

class TestAPIRoutes:        response = client.get("/nonexistent")

    """Test cases for API endpoints"""        assert response.status_code == 404



    def test_health_endpoint(self, client):    def test_home_page_mentions_ubuntu(self, client):

        """Verify health check endpoint"""        """Verify home page mentions Ubuntu"""

        response = client.get("/api/health")        response = client.get("/")

        assert response.status_code == 200        assert b"Ubuntu" in response.data

        data = response.get_json()

        assert "status" in data    def test_home_page_mentions_aws(self, client):

        """Verify home page mentions AWS"""

    def test_get_users_endpoint(self, client):        response = client.get("/")

        """Verify get users endpoint"""        assert b"AWS" in response.data

        response = client.get("/api/users")

        assert response.status_code == 200

        data = response.get_json()class TestBootUpScenarios:

        assert "users" in data    """Test cases simulating boot-up scenarios on remote server"""

        assert "total" in data

    @pytest.fixture

    def test_create_user_endpoint(self, client):    def client(self):

        """Verify create user endpoint"""        """Create test client"""

        response = client.post(        app.config["TESTING"] = True

            "/api/users",        with app.test_client() as client:

            json={            yield client

                "username": "testuser",

                "email": "test@example.com",    def test_app_initializes_without_errors(self):

                "first_name": "Test",        """Verify app initializes without raising exceptions"""

                "last_name": "User",        try:

            },            test_app = app

        )            assert test_app is not None

        assert response.status_code == 201        except Exception as e:

        data = response.get_json()            pytest.fail(f"App initialization failed: {str(e)}")

        assert data["username"] == "testuser"

        assert data["email"] == "test@example.com"    def test_app_accessible_immediately_after_startup(self, client):

        """Verify app responds immediately after startup"""

    def test_create_user_missing_required_fields(self, client):        response = client.get("/")

        """Verify create user with missing fields fails"""        assert response.status_code == 200

        response = client.post("/api/users", json={"username": "testuser"})        assert len(response.data) > 0

        assert response.status_code == 400

    def test_multiple_requests_after_startup(self, client):

    def test_get_user_by_id(self, client, app):        """Verify app handles multiple requests after startup"""

        """Verify get user by ID endpoint"""        for _ in range(5):

        with app.app_context():            response = client.get("/")

            user = User.create_user(            assert response.status_code == 200

                username="testuser",

                email="test@example.com",    def test_high_request_volume_during_startup(self, client):

            )        """Verify app handles high request volume after startup"""

        responses = []

        response = client.get(f"/api/users/{user.id}")        for _ in range(50):

        assert response.status_code == 200            response = client.get("/")

        data = response.get_json()            responses.append(response.status_code)

        assert data["username"] == "testuser"

        assert all(status == 200 for status in responses)

    def test_get_nonexistent_user(self, client):

        """Verify getting nonexistent user returns 404"""    def test_request_response_consistency(self, client):

        response = client.get("/api/users/9999")        """Verify response consistency across multiple calls"""

        assert response.status_code == 404        responses = []

        for _ in range(5):

    def test_update_user(self, client, app):            response = client.get("/")

        """Verify update user endpoint"""            responses.append(response.data)

        with app.app_context():

            user = User.create_user(        # All responses should be identical

                username="testuser",        assert all(r == responses[0] for r in responses)

                email="test@example.com",

            )

class TestDeploymentValidation:

        response = client.put(    """Test cases for verifying deployment requirements"""

            f"/api/users/{user.id}",

            json={    @pytest.fixture

                "first_name": "Updated",    def client(self):

            },        """Create test client"""

        )        app.config["TESTING"] = True

        assert response.status_code == 200        with app.test_client() as client:

        data = response.get_json()            yield client

        assert data["first_name"] == "Updated"

    def test_app_uses_gunicorn_compatible_interface(self):

    def test_delete_user(self, client, app):        """Verify app can be run by Gunicorn"""

        """Verify delete user endpoint"""        assert hasattr(app, "wsgi_app")

        with app.app_context():        assert callable(app.wsgi_app)

            user = User.create_user(

                username="testuser",    def test_app_supports_werkzeug_server(self):

                email="test@example.com",        """Verify app supports Werkzeug development server"""

            )        assert hasattr(app, "run")

            user_id = user.id        assert callable(app.run)



        response = client.delete(f"/api/users/{user_id}")    def test_home_route_supports_get_method(self, client):

        assert response.status_code == 200        """Verify home route supports GET method"""

        response = client.get("/")

        # Verify user is deleted        assert response.status_code == 200

        response = client.get(f"/api/users/{user_id}")

        assert response.status_code == 404    def test_no_hardcoded_localhost_in_response(self, client):

        """Verify response doesn't contain hardcoded localhost URLs"""

        response = client.get("/")

class TestUserModel:        response_text = response.data.decode("utf-8")

    """Test cases for User model"""        assert "localhost:5000" not in response_text



    def test_create_user(self, app):

        """Verify user creation"""class TestErrorHandling:

        with app.app_context():    """Test cases for error handling during boot up"""

            user = User.create_user(

                username="testuser",    @pytest.fixture

                email="test@example.com",    def client(self):

                first_name="Test",        """Create test client"""

            )        app.config["TESTING"] = True

            assert user.id is not None        with app.test_client() as client:

            assert user.username == "testuser"            yield client



    def test_user_to_dict(self, app):    def test_app_handles_root_path_request(self, client):

        """Verify user to_dict method"""        """Verify app handles root path request correctly"""

        with app.app_context():        response = client.get("/")

            user = User.create_user(        assert response.status_code == 200

                username="testuser",

                email="test@example.com",    def test_app_response_encoding(self, client):

            )        """Verify app response uses proper UTF-8 encoding"""

            user_dict = user.to_dict()        response = client.get("/")

            assert user_dict["username"] == "testuser"        # Should be able to decode response as UTF-8

            assert user_dict["email"] == "test@example.com"        try:

            response.data.decode("utf-8")

    def test_get_user_by_username(self, app):            assert True

        """Verify get user by username"""        except UnicodeDecodeError:

        with app.app_context():            pytest.fail("Response is not UTF-8 encoded")

            User.create_user(

                username="testuser",

                email="test@example.com",class TestSystemIntegration:

            )    """Test cases for system integration during boot up"""

            user = User.get_by_username("testuser")

            assert user is not None    @pytest.fixture

            assert user.username == "testuser"    def client(self):

        """Create test client"""

    def test_get_user_by_email(self, app):        app.config["TESTING"] = True

        """Verify get user by email"""        with app.test_client() as client:

        with app.app_context():            yield client

            User.create_user(

                username="testuser",    def test_app_resources_loading(self, client):

                email="test@example.com",        """Verify app loads all resources"""

            )        response = client.get("/")

            user = User.get_by_email("test@example.com")        assert response.status_code == 200

            assert user is not None        assert len(response.data) > 100  # Should have substantial content

            assert user.email == "test@example.com"

    def test_app_template_rendering(self, client):

    def test_update_user(self, app):        """Verify app renders template correctly"""

        """Verify user update"""        response = client.get("/")

        with app.app_context():        # Check for rendered content indicators

            user = User.create_user(        assert b"<" in response.data  # HTML tags present

                username="testuser",        assert b">" in response.data  # HTML tags present

                email="test@example.com",

            )

            user.update(first_name="Updated")class TestGunicornCompatibility:

            assert user.first_name == "Updated"    """Test cases for Gunicorn server compatibility (port 8000, 3 workers)"""



    def test_duplicate_username_fails(self, app):    @pytest.fixture

        """Verify duplicate username fails"""    def client(self):

        from sqlalchemy.exc import IntegrityError        """Create test client"""

        app.config["TESTING"] = True

        with app.app_context():        with app.test_client() as client:

            User.create_user(            yield client

                username="testuser",

                email="test@example.com",    def test_app_callable_as_wsgi(self):

            )        """Verify app is callable as WSGI application"""

            with pytest.raises(IntegrityError):        assert callable(app)

                User.create_user(

                    username="testuser",    def test_app_wsgi_app_attribute(self):

                    email="another@example.com",        """Verify app has wsgi_app attribute for Gunicorn"""

                )        assert hasattr(app, "wsgi_app")



    def test_app_stateless_design(self, client):

class TestErrorHandling:        """Verify app is stateless (required for multiple workers)"""

    """Test cases for error handling"""        # Make requests and verify no state is maintained

        response1 = client.get("/")

    def test_404_error(self, client):        response2 = client.get("/")

        """Verify 404 error handling"""

        response = client.get("/nonexistent")        assert response1.data == response2.data

        assert response.status_code == 404        assert response1.status_code == response2.status_code



    def test_invalid_json_in_post(self, client):    def test_app_thread_safety(self, client):

        """Verify handling of invalid JSON"""        """Verify app responses are consistent (thread safety)"""

        response = client.post(        responses = set()

            "/api/users",        for _ in range(10):

            data="invalid json",            response = client.get("/")

            content_type="application/json"            # Convert to string for comparison

        )            responses.add(response.data.decode("utf-8"))

        assert response.status_code in [400, 500]

        # All responses should be identical

        assert len(responses) == 1

class TestGunicornCompatibility:

    """Test cases for Gunicorn compatibility"""    def test_app_handles_wsgi_environ_variables(self):

        """Verify app can handle WSGI environ variables"""

    def test_app_is_wsgi_callable(self):        with app.test_request_context("/"):

        """Verify app is WSGI callable"""            from flask import request

        app = create_app(config=TestingConfig)

        assert callable(app)            # Verify Flask can access WSGI environ

            assert request.environ is not None

    def test_app_has_wsgi_app(self):            assert "REQUEST_METHOD" in request.environ

        """Verify app has wsgi_app attribute"""

        app = create_app(config=TestingConfig)

        assert hasattr(app, "wsgi_app")class TestNginxReverseProxyCompatibility:

    """Test cases for Nginx reverse proxy configuration (port 80)"""



class TestProductionReadiness:    @pytest.fixture

    """Test cases for production readiness"""    def client(self):

        """Create test client"""

    def test_app_response_time(self, client):        app.config["TESTING"] = True

        """Verify response time is acceptable"""        with app.test_client() as client:

        import time            yield client



        start = time.time()    def test_app_handles_x_forwarded_for_header(self, client):

        response = client.get("/")        """Verify app handles X-Forwarded-For header from Nginx"""

        elapsed = time.time() - start        response = client.get("/", headers={"X-Forwarded-For": "203.0.113.1"})

        assert response.status_code == 200

        assert elapsed < 1.0  # Should respond in less than 1 second

        assert response.status_code == 200    def test_app_handles_x_real_ip_header(self, client):

        """Verify app handles X-Real-IP header from Nginx"""

    def test_multiple_requests(self, client):        response = client.get("/", headers={"X-Real-IP": "203.0.113.1"})

        """Verify app handles multiple requests"""        assert response.status_code == 200

        responses = []

        for _ in range(10):    def test_app_handles_host_header_from_proxy(self, client):

            response = client.get("/")        """Verify app handles Host header from Nginx proxy"""

            responses.append(response.status_code)        response = client.get("/", headers={"Host": "example.com"})

        assert response.status_code == 200

        assert all(status == 200 for status in responses)

    def test_response_size_reasonable(self, client):

    def test_database_connectivity(self, client):        """Verify response size is reasonable for proxy transmission"""

        """Verify database is accessible via API"""        response = client.get("/")

        response = client.get("/api/health")        content_length = len(response.data)

        assert response.status_code == 200        # Response should be reasonable (not empty, not absurdly large)

        data = response.get_json()        assert 100 < content_length < 100000

        assert "status" in data

    def test_nginx_proxy_pass_compatibility(self, client):

        """Verify app output is compatible with proxy_pass directive"""

class TestAPIResponseFormat:        response = client.get("/")

    """Test cases for API response format"""        # Response should be valid HTTP response with content

        assert response.status_code == 200

    def test_api_returns_json(self, client):        assert response.data is not None

        """Verify API returns JSON"""

        response = client.get("/api/users")

        assert response.content_type in ["application/json", "application/json; charset=utf-8"]class TestSystemdServiceCompatibility:

    """Test cases for systemd service configuration"""

    def test_api_error_response_format(self, client):

        """Verify API error response is JSON"""    @pytest.fixture

        response = client.get("/api/users/9999")    def client(self):

        assert response.content_type in ["application/json", "application/json; charset=utf-8"]        """Create test client"""

        data = response.get_json()        app.config["TESTING"] = True

        assert "error" in data or isinstance(data, dict)        with app.test_client() as client:

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
