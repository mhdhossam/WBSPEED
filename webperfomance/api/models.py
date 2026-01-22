from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WasmLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    route = models.CharField(max_length=255)
    payload = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WasmLog: {self.user} - {self.route} - {self.created_at}"
class ConvexCall(models.Model):
    fn_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    args = models.JSONField()
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fn_name} called by {self.user} at {self.created_at}"

