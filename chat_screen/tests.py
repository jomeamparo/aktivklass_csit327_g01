from django.test import TestCase, Client
from django.urls import reverse
from core.models import Student, Faculty, AdminUser, Conversation, Message

# Create your tests here.

class ChatAccessTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test users
        self.student1 = Student.objects.create(
            student_id='STU001',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password123'
        )
        
        self.student2 = Student.objects.create(
            student_id='STU002',
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            password='password123',
            course='Computer Science',
            year='3rd Year'
        )
        
        self.faculty = Faculty.objects.create(
            faculty_id='FAC001',
            first_name='Prof',
            last_name='Johnson',
            email='prof@example.com',
            password='password123',
            college_name='Engineering',
            department_name='Computer Science'
        )
        
        self.admin = AdminUser.objects.create(
            employee_id='ADM001',
            first_name='Admin',
            last_name='User',
            password='password123'
        )
        
        # Create a test conversation
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.student1, self.student2)

    def test_student_access(self):
        """Test that students can access all chat functionality"""
        self.client.session['user_id'] = self.student1.student_id
        
        # Test chat home access
        response = self.client.get(reverse('chat_home'))
        self.assertEqual(response.status_code, 200)
        
        # Test search students access
        response = self.client.get(reverse('search_students'))
        self.assertEqual(response.status_code, 200)
        
        # Test conversation detail access
        response = self.client.get(reverse('conversation_detail', args=[self.conversation.id]))
        self.assertEqual(response.status_code, 200)
        
        # Test message sending
        response = self.client.post(reverse('send_message', args=[self.conversation.id]), {
            'content': 'Test message'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)

    def test_search_functionality(self):
        """Test student search functionality"""
        self.client.session['user_id'] = self.student1.student_id
        
        # Test search by name
        response = self.client.get(reverse('search_students'), {'q': 'Jane'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Smith')
        
        # Test search by student ID
        response = self.client.get(reverse('search_students'), {'q': 'STU002'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Smith')
        
        # Test search by email
        response = self.client.get(reverse('search_students'), {'q': 'jane@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Smith')
        
        # Test search excludes current user
        response = self.client.get(reverse('search_students'), {'q': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'John Doe')  # Should not show current user

    def test_start_conversation(self):
        """Test starting a new conversation"""
        self.client.session['user_id'] = self.student1.student_id
        
        # Test starting conversation with another student
        response = self.client.get(reverse('start_conversation', args=[self.student2.student_id]))
        self.assertEqual(response.status_code, 302)
        
        # Check if conversation was created
        conversation = Conversation.objects.filter(
            participants=self.student1
        ).filter(
            participants=self.student2
        ).first()
        self.assertIsNotNone(conversation)
        
        # Test starting conversation with self (should redirect)
        response = self.client.get(reverse('start_conversation', args=[self.student1.student_id]))
        self.assertEqual(response.status_code, 302)

    def test_non_student_redirects(self):
        """Test that non-students are redirected appropriately"""
        test_cases = [
            (self.faculty.faculty_id, 'dashboard_teacher'),
            (self.admin.employee_id, 'dashboard_admin'),
        ]
        
        for user_id, expected_redirect in test_cases:
            self.client.session['user_id'] = user_id
            
            # Test all chat endpoints
            for url_name in ['chat_home', 'search_students', 'conversation_detail', 'send_message']:
                if url_name == 'send_message':
                    response = self.client.post(reverse(url_name, args=[self.conversation.id]), {
                        'content': 'Test message'
                    })
                elif url_name == 'conversation_detail':
                    response = self.client.get(reverse(url_name, args=[self.conversation.id]))
                elif url_name == 'search_students':
                    response = self.client.get(reverse(url_name))
                else:
                    response = self.client.get(reverse(url_name))
                
                self.assertEqual(response.status_code, 302)
                self.assertIn(expected_redirect, response.url)

    def test_unauthenticated_redirect(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('chat_home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_conversation_model_methods(self):
        """Test Conversation model helper methods"""
        # Test get_or_create_conversation
        conversation = Conversation.get_or_create_conversation(self.student1, self.student2)
        self.assertIsNotNone(conversation)
        self.assertEqual(conversation.participants.count(), 2)
        
        # Test getting existing conversation
        same_conversation = Conversation.get_or_create_conversation(self.student1, self.student2)
        self.assertEqual(conversation.id, same_conversation.id)
        
        # Test get_other_participant
        other_participant = conversation.get_other_participant(self.student1)
        self.assertEqual(other_participant, self.student2)
