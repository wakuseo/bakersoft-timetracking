from django.db import models
from django.utils.translation import gettext_lazy as _

from bakersoft.core.models import USER, AbstractBaseUserModel


class BakerBaseAbstractModel(AbstractBaseUserModel):
    """Base abstract model for Work and Project entities"""

    class StatusChoices(models.TextChoices):
        PROGRESS = "progress", "Progress"
        DONE = "done", "Done"

    name = models.CharField(max_length=250, blank=False)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PROGRESS,
    )
    completed = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Project(BakerBaseAbstractModel):
    """Project entity"""

    manager = models.ForeignKey(
        to=USER, related_name="manager", on_delete=models.DO_NOTHING
    )

    class Meta(BakerBaseAbstractModel.Meta):
        verbose_name_plural = _("Projects")

    def __str__(self):
        return f"{self.name} - {self.manager}"

    @property
    def owner(self):
        """Alias for project owner"""
        return self.manager

    @property
    def elapsed_time(self):
        """Sum all works' elapsed time which equals to project's elapsed time"""
        import datetime

        works = self.work_set.all()
        works_elapsed_time = [work.elapsed_time for work in works]

        return sum(works_elapsed_time, datetime.timedelta())


class Work(BakerBaseAbstractModel):
    """Work entity"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta(BakerBaseAbstractModel.Meta):
        verbose_name_plural = _("Works")

    def __str__(self):
        return self.name

    @property
    def completed_at(self):
        if self.completed:
            return self.changed_at

    @property
    def elapsed_time(self):
        """Get elapsed time for the work instance

        If a work not completed get difference between current and started time
        No need to sent timezone in python since TIME_ZONE = UTC set already in base settings
        """
        # https://docs.djangoproject.com/en/3.2/topics/i18n/timezones/#naive-and-aware-datetime-objects
        from django.utils import timezone

        if self.completed:
            return self.changed_at - self.created_at

        return timezone.now() - self.created_at
