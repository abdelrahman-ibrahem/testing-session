from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post


class PostTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='test123')

    def test_post_model(self):
        # Create a test post
        post = Post.objects.create(title='Test Post', content='This is a test post.')

        # Ensure the post has the expected attributes
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post.')

class PostTestView(TestCase):
    def test_post_list(self):
        # Create a test post
        Post.objects.create(title='Test Post', content='This is a test post.')
        data_shape = [
            {
                'title': 'Test Post',
                'content': 'This is a test post.',
                'id': 1,  # This should be the primary key of the created post
            }
        ]
        # Send a GET request to the post list view
        response = self.client.get('/api/posts/')

        # Ensure the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Ensure the response contains the expected data
        # self.assertIn('Test Post', str(response.content))
        data = response.json()
        self.assertEqual(data[0]['title'], 'Test Post')

    def test_post_create(self):
        # Send a POST request to the post list view with valid data
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
        }
        response = self.client.post('/api/posts/', data)

        # Ensure the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Ensure the created post exists in the database
        post = Post.objects.get(pk=1)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post.')
    
    def test_post_detail(self):
        # Create a test post
        post = Post.objects.create(title='Test Post', content='This is a test post.')

        # Send a GET request to the post detail view
        response = self.client.get('/api/posts/{}/'.format(post.id))

        # Ensure the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Ensure the response contains the expected data
        data = response.json()
        self.assertEqual(data['title'], 'Test Post')
        self.assertEqual(data['content'], 'This is a test post.')
    
    def test_post_update(self):
        # Create a test post
        post = Post.objects.create(title='Test Post', content='This is a test post.')

        # Send a PUT request to the post detail view with updated data
        data = {
            'title': 'Updated Test Post',
            'content': 'This is an updated test post.',
        }
        response = self.client.put('/api/posts/{}/'.format(post.id), data, content_type='application/json')

        # Ensure the response status code is 200 (OK)
        # self.assertEqual(response.status_code, 200)

        # Ensure the updated post exists in the database
        response_data = response.json()
        self.assertEqual(response_data['title'], 'Updated Test Post')
        self.assertEqual(response_data['content'], 'This is an updated test post.')
    
    def test_post_delete(self):
        # Create a test post
        post = Post.objects.create(title='Test Post', content='This is a test post.')
        Post.objects.create(title='Test Post', content='This is a test post')
        # Send a DELETE request to the post detail view
        self.assertEqual(len(Post.objects.all()), 2)
        response = self.client.delete('/api/posts/{}/'.format(post.id))

        # Ensure the response status code is 204 (No Content)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.all().count(), 1)

