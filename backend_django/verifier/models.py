from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True)
    daily_screen_time_limit_minutes = models.IntegerField(default=240)
    device_name = models.CharField(max_length=100, default="Android Smartphone")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


class VerificationCheck(models.Model):
    VERDICT_CHOICES = [
        ('TRUE', 'True'),
        ('FALSE', 'False'),
        ('MISLEADING', 'Misleading'),
        ('UNVERIFIED', 'Unverified / Inconclusive'),
    ]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='checks')
    content = models.TextField()
    source_url = models.TextField(blank=True, null=True)
    verdict = models.CharField(max_length=50, choices=VERDICT_CHOICES, default='UNVERIFIED')
    confidence = models.FloatField(default=0.85)
    summary = models.TextField()
    sources_json = models.TextField(default="[]")
    category = models.CharField(max_length=100, default="General")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Check #{self.id}: {self.content[:40]}... ({self.verdict})"

    @property
    def sources(self):
        try:
            return json.loads(self.sources_json)
        except Exception:
            return []


class ScreenTimeRecord(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='screen_time_records')
    date = models.DateField(default=timezone.now)
    total_screen_minutes = models.IntegerField(default=0)
    unlock_count = models.IntegerField(default=0)
    longest_session_minutes = models.IntegerField(default=0)
    focus_time_minutes = models.IntegerField(default=0)
    productivity_score = models.IntegerField(default=75) # 0 to 100
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')

    def __str__(self):
        return f"ScreenTime {self.date}: {self.total_screen_minutes}m (Score: {self.productivity_score})"


class AppUsageRecord(models.Model):
    CATEGORY_CHOICES = [
        ('Social', 'Social Media'),
        ('Productivity', 'Productivity'),
        ('Entertainment', 'Entertainment'),
        ('Utility', 'Utility'),
        ('Browser', 'Browser'),
    ]

    screen_time_record = models.ForeignKey(ScreenTimeRecord, on_delete=models.CASCADE, related_name='app_usages')
    app_name = models.CharField(max_length=100)
    package_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Social')
    usage_minutes = models.IntegerField(default=0)
    open_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-usage_minutes']

    def __str__(self):
        return f"{self.app_name}: {self.usage_minutes}m ({self.category})"


class DigitalHabitRecommendation(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=200)
    advice = models.TextField()
    category = models.CharField(max_length=100, default="Screen Time")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.priority}] {self.title}"
