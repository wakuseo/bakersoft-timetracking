from django.contrib import admin

from bakersoft.trackings.models import Project, Work


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "manager", "completed", "elapsed_time", "uuid"]
    list_filter = ["created_at", "changed_at"]
    search_fields = [
        "name",
        "account__email",
        "account__username",
    ]


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "completed", "completed_at", "elapsed_time", "uuid"]
    list_filter = ["created_at", "changed_at"]
    search_fields = [
        "name",
        "account__email",
        "account__username",
    ]
