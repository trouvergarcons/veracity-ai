import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import ScreenTimeRecord, AppUsageRecord, VerificationCheck, DigitalHabitRecommendation

class VeracityAITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_auth_register_and_login(self):
        """Module 1: User Registration and Login test"""
        reg_res = self.client.post('/api/auth/register/', data=json.dumps({
            'username': 'testuser',
            'email': 'test@veracity.ai',
            'password': 'Password123!',
            'full_name': 'Test Researcher'
        }), content_type='application/json')
        self.assertEqual(reg_res.status_code, 201)
        self.assertTrue(reg_res.json()['success'])

        # Test login
        login_res = self.client.post('/api/auth/login/', data=json.dumps({
            'username': 'testuser',
            'password': 'Password123!'
        }), content_type='application/json')
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(login_res.json()['success'])

    def test_verify_claim_and_nlp(self):
        """Module 2: Fake news detection test"""
        res = self.client.post('/api/verify/', data=json.dumps({
            'content': 'Miracle cure burns 20kg fat in 24 hours shocking secret doctors banned!'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn('verdict', data)
        self.assertIn('confidence', data)
        self.assertIn('summary', data)
        self.assertEqual(data['verdict'], 'FALSE')

    def test_chatbot_endpoint(self):
        """Module 3: AI Chatbot test"""
        res = self.client.post('/api/chat/', data=json.dumps({
            'message': 'How to spot misinformation online?'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('reply', res.json())

    def test_wellbeing_and_screen_time(self):
        """Module 4 & 6: Screen time monitoring & Digital wellbeing"""
        seed_res = self.client.post('/api/wellbeing/seed/')
        self.assertEqual(seed_res.status_code, 200)

        summary_res = self.client.get('/api/wellbeing/summary/')
        self.assertEqual(summary_res.status_code, 200)
        data = summary_res.json()
        self.assertIn('today', data)
        self.assertIn('total_minutes', data['today'])
        self.assertGreater(data['today']['total_minutes'], 0)

    def test_social_media_analytics(self):
        """Module 5: Social Media Analytics"""
        self.client.post('/api/wellbeing/seed/')
        res = self.client.get('/api/wellbeing/social-media/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn('apps', data)
        self.assertIn('social_media_ratio_percent', data)

    def test_android_usagestats_sync(self):
        """Module 6: Android UsageStatsManager Telemetry Ingestion"""
        res = self.client.post('/api/wellbeing/sync-android/', data=json.dumps({
            'total_screen_minutes': 245,
            'unlock_count': 50,
            'longest_session_minutes': 42,
            'focus_time_minutes': 110,
            'productivity_score': 80,
            'apps': [
                {'app_name': 'Instagram', 'usage_minutes': 65, 'category': 'Social', 'open_count': 14},
                {'app_name': 'Chrome', 'usage_minutes': 45, 'category': 'Browser', 'open_count': 10},
            ]
        }), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()['success'])

    def test_ai_recommendations(self):
        """Module 7: AI Recommendation Engine"""
        self.client.post('/api/wellbeing/seed/')
        recs_res = self.client.get('/api/recommendations/')
        self.assertEqual(recs_res.status_code, 200)
        recs = recs_res.json()
        self.assertGreater(len(recs), 0)

