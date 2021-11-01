from django.db import models
from django.utils.translation import gettext_lazy as _

from bakersoft.core.models import USER, AbstractBaseUserModel
from bakersoft.trackings.exceptions import ProjectCompleteException


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
    def completed(self):
        """Helper to check whether work completed"""
        if self.status == "done":
            return True

        return False

    def complete(self):
        """Update status to done if there is no in <progress> status in any related work"""
        for work in self.works:
            if work.status == "done":
                raise ProjectCompleteException(work)

    @property
    def owner(self):
        """Alias for project owner"""
        return self.manager

    @property
    def works(self):
        """Get all related works"""
        return self.work_set.all()

    @property
    def elapsed_time(self):
        """Sum all works' duration in milisecond which equals to project's elapsed time in"""
        import datetime

        works_elapsed_time = [work.elapsed_time for work in self.works]

        return sum(works_elapsed_time, datetime.timedelta())


class Work(BakerBaseAbstractModel):
    """Work entity"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta(BakerBaseAbstractModel.Meta):
        verbose_name_plural = _("Works")

    def __str__(self):
        return self.name

    @property
    def completed(self):
        """Helper to check whether work completed"""
        if self.status == "done":
            return True

        return False

    def complete(self):
        """Update status to done"""
        self.status = "done"
        self.save()

    @property
    def completed_at(self):
        """Get completed timestamp if completed"""
        if self.completed:
            return self.changed_at

    @property
    def elapsed_time(self):
        """Get duration for the work instance in microsecond

        If a work not completed get difference between current and started time
        No need to sent timezone in python since TIME_ZONE = UTC set already in base settings
        """
        # https://docs.djangoproject.com/en/3.2/topics/i18n/timezones/#naive-and-aware-datetime-objects
        from django.utils import timezone

        if self.completed:
            return self.changed_at - self.created_at

        return timezone.now() - self.created_at
