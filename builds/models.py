from django.db import models

class Application(models.Model):
    """Represents an software application or a versioned component of
       an application.  Examples would be 'occ', 'vxstorage', or 'core'.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Version(models.Model):
    """Represents a version of a specific application."""
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='versions')
    version = models.CharField(max_length=25)
    next_number = models.IntegerField(default=1)

    def __str__(self):
        return '%s %s' % (self.application, self.version)

    class Meta:
        unique_together = ('application', 'version',)

class Build(models.Model):
    """Models a single build of an Application."""
    version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='builds')
    branch = models.CharField(max_length=200)
    time = models.DateTimeField('Build time', auto_now_add=True)
    revision = models.CharField(max_length=100)
    number = models.IntegerField(default=1)

    def __str__(self):
        return '%s %s %s %s %s' % (self.version, self.branch, self.time, self.revision, self.number)

    class Meta:
        unique_together = ('version', 'number',)
        ordering = ('time',)

    @property
    def application_name(self):
        """Declare a property so that the serializer can access the name of
           the application
        """
        return self.version.application.name

class NewBuild(models.Model):
    """NewBuild is used to create a new Build"""
    application = models.CharField(max_length=200)
    version = models.CharField(max_length=25)
    branch = models.CharField(max_length=200)
    revision = models.CharField(max_length=100)

    def __str__(self):
        return '%s %s %s %s' % (application, version, branch, revision,)

    class Meta:
        """This model is only used to create new Build objects.  It is not persisted"""
        managed = False
