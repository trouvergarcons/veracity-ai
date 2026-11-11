from django.urls import path
from .views import (
    register_api,
    login_api,
    password_reset_api,
    user_me_api,
    verify,
    checks_history_api,
    chat_api,
    wellbeing_summary_api,
    laptop_telemetry_api,
    social_media_analytics_api,
    sync_android_usagestats_api,
    seed_wellbeing_data_api,
    recommendations_api,
    generate_recommendations_api,
    analytics_overview_api,
)

urlpatterns = [
    # Auth
    path('auth/register/', register_api, name='register'),
    path('auth/login/', login_api, name='login'),
    path('auth/reset-password/', password_reset_api, name='reset-password'),
    path('auth/me/', user_me_api, name='user-me'),

    # Fake News Detection
    path('verify/', verify, name='verify'),
    path('checks/', checks_history_api, name='checks-history'),

    # AI Chatbot
    path('chat/', chat_api, name='chat'),

    # Screen Time & Digital Wellbeing
    path('wellbeing/laptop-telemetry/', laptop_telemetry_api, name='laptop-telemetry'),
    path('wellbeing/summary/', wellbeing_summary_api, name='wellbeing-summary'),
    path('wellbeing/sync-android/', sync_android_usagestats_api, name='sync-android'),
    path('wellbeing/seed/', seed_wellbeing_data_api, name='seed-wellbeing'),

    # Social Media Analytics
    path('wellbeing/social-media/', social_media_analytics_api, name='social-media'),

    # AI Recommendation Engine
    path('recommendations/', recommendations_api, name='recommendations'),
    path('recommendations/generate/', generate_recommendations_api, name='generate-recommendations'),

    # Overview Analytics & Looker Studio
    path('analytics/overview/', analytics_overview_api, name='analytics-overview'),
]
