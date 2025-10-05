
import unittest
import json
from datetime import date, timedelta
from app import app, db, User, Task

class TestApiEndpoints(unittest.TestCase):

    def setUp(self):
        """Set up a test environment before each test."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key' # Use a consistent key for tests
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use an in-memory DB
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def _get_auth_token_for_user(self, username, password):
        """Helper to get a token for a specific user."""
        response = self.client.post('/login', data=json.dumps({
            'username': username,
            'password': password
        }), content_type='application/json')
        self.assertIn(response.status_code, [200, 201])
        return response.get_json()['token']

    def _register_user(self, username, password):
        """Helper to register a user."""
        return self.client.post('/register', data=json.dumps({
            'username': username,
            'password': password
        }), content_type='application/json')

    # 1. Validation Testing
    # ---------------------

    def test_validation_register_missing_fields(self):
        """Test registration with missing username or password."""
        # Missing username
        response = self.client.post('/register', data=json.dumps({'password': 'pw'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Missing password
        response = self.client.post('/register', data=json.dumps({'username': 'u'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_validation_create_task_missing_title(self):
        """Test creating a task with a missing title."""
        self._register_user('testuser', 'password')
        token = self._get_auth_token_for_user('testuser', 'password')
        response = self.client.post('/tasks', headers={'Authorization': f'Bearer {token}'},
                                    data=json.dumps({'description': 'desc'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_validation_create_task_invalid_date(self):
        """Test creating a task with an invalid date format."""
        self._register_user('testuser', 'password')
        token = self._get_auth_token_for_user('testuser', 'password')
        response = self.client.post('/tasks', headers={'Authorization': f'Bearer {token}'},
                                    data=json.dumps({'title': 't', 'due_date': '2025/12/31'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # 2. Boundary Testing
    # -------------------

    def test_boundary_pagination(self):
        """Test pagination edge cases."""
        self._register_user('testuser', 'password')
        token = self._get_auth_token_for_user('testuser', 'password')
        with app.app_context():
            user = User.query.first()
            for i in range(15):
                db.session.add(Task(title=f'Task {i}', user_id=user.id))
            db.session.commit()

        # Page out of bounds
        response = self.client.get('/tasks?page=3&per_page=10', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(len(response.get_json()['tasks']), 0)

        # Non-integer page
        response = self.client.get('/tasks?page=abc', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200) # Default to page 1
        self.assertEqual(len(response.get_json()['tasks']), 10)

    def test_boundary_calculated_overdue_field(self):
        """Test the 'is_overdue' calculated field edge cases."""
        self._register_user('testuser', 'password')
        token = self._get_auth_token_for_user('testuser', 'password')
        today = date.today()

        # Overdue task
        self.client.post('/tasks', headers={'Authorization': f'Bearer {token}'},
                           data=json.dumps({'title': 't1', 'due_date': (today - timedelta(days=1)).isoformat()}), content_type='application/json')
        # Due today task
        self.client.post('/tasks', headers={'Authorization': f'Bearer {token}'},
                           data=json.dumps({'title': 't2', 'due_date': today.isoformat()}), content_type='application/json')
        # Future task
        self.client.post('/tasks', headers={'Authorization': f'Bearer {token}'},
                           data=json.dumps({'title': 't3', 'due_date': (today + timedelta(days=1)).isoformat()}), content_type='application/json')

        response = self.client.get('/tasks', headers={'Authorization': f'Bearer {token}'})
        tasks = {t['title']: t for t in response.get_json()['tasks']}
        self.assertTrue(tasks['t1']['is_overdue'])
        self.assertFalse(tasks['t2']['is_overdue'])
        self.assertFalse(tasks['t3']['is_overdue'])

    # 3. Security Testing
    # -------------------

    def test_security_unauthorized_access(self):
        """Test that endpoints are protected from unauthorized access."""
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/tasks', headers={'Authorization': 'Bearer garbage'})
        self.assertEqual(response.status_code, 401)

    def test_security_user_cannot_access_other_users_tasks(self):
        """Test that a user cannot access tasks belonging to another user."""
        # Create two users
        self._register_user('user1', 'pw1')
        self._register_user('user2', 'pw2')
        token1 = self._get_auth_token_for_user('user1', 'pw1')
        token2 = self._get_auth_token_for_user('user2', 'pw2')

        # User 1 creates a task
        response = self.client.post('/tasks', headers={'Authorization': f'Bearer {token1}'},
                                    data=json.dumps({'title': 'User 1 Task'}), content_type='application/json')
        task_id = self.client.get('/tasks', headers={'Authorization': f'Bearer {token1}'}).get_json()['tasks'][0]['id']

        # User 2 tries to access User 1's task
        response = self.client.get(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token2}'})
        self.assertEqual(response.status_code, 404)

        response = self.client.put(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token2}'},
                                   data=json.dumps({'title': 'hacked'}), content_type='application/json')
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token2}'})
        self.assertEqual(response.status_code, 404)

    # 4. Integration Testing
    # ----------------------

    def test_integration_full_crud_workflow(self):
        """Test the full Register-Login-Create-Read-Update-Delete workflow."""
        # 1. Register
        response = self._register_user('crud_user', 'crud_pw')
        self.assertEqual(response.status_code, 201)

        # 2. Login
        token = self._get_auth_token_for_user('crud_user', 'crud_pw')
        self.assertIsNotNone(token)

        # 3. Create
        response = self.client.post('/tasks', headers={'Authorization': f'Bearer {token}'},
                                    data=json.dumps({'title': 'My CRUD Task', 'priority': 'High'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # 4. Read
        response = self.client.get('/tasks', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        tasks = response.get_json()['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], 'My CRUD Task')
        task_id = tasks[0]['id']

        # 5. Update
        response = self.client.put(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'},
                                   data=json.dumps({'title': 'My Updated CRUD Task', 'completed': True}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # 6. Verify Update
        response = self.client.get(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], 'My Updated CRUD Task')
        self.assertTrue(response.get_json()['completed'])

        # 7. Delete
        response = self.client.delete(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

        # 8. Verify Delete
        response = self.client.get(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
