from django.db import models

class Component(models.Model):
    """Represents an software component.

    A software componenet is a piece of software that can be built and 
    versioned independently.  This could be a full product, or a piece of
    a product like a library.

    Attributes:
        name    The name of the component.  Lookups on the componenet name 
                will be case insensitive.  The stored value is always lower
                case.
    """
    name = models.CharField(db_index=True, unique=True, max_length=200)

    def __str__(self):
        return self.name

class VersionBase(models.Model):
    """Represents the base version of a Component.

    The base version is a version that does not contain a build number.  For
    instance '1.2.0' can be a base version.  If the build number is 12, then
    the full version would be '1.2.0.12'.  

    Attributes:
        component   The Component that this VersionBase is tied to.
        value       The value of the VersionBase.  For example, '2.0'.
        next_number The build number to be assigned to the next build that uses
                    this VersionBase.  Once a build is made, this value will be
                    increased.
    """
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='versions')
    value = models.CharField(db_index=True, max_length=25)
    next_number = models.IntegerField(default=1)

    def __str__(self):
        return '%s %s' % (self.component, self.value)

    class Meta:
        unique_together = ('component', 'value',)

class Build(models.Model):
    """Models a single build of an Component.

    Attributes:
        version_base    The base version number of the build.
        branch          The branch the build was built off of.
        time            The time the build was made.
        revision        The SCM revision of the build.
        number          The build number.
    """
    version_base = models.ForeignKey(VersionBase, on_delete=models.CASCADE, related_name='builds')
    branch = models.CharField(max_length=200)
    time = models.DateTimeField('Build time', auto_now_add=True)
    revision = models.CharField(max_length=100)
    number = models.IntegerField()

    def __str__(self):
        return '%s %s %s %s %s' % (self.version_base, self.branch, self.time, self.revision, self.number)

    class Meta:
        unique_together = ('version_base', 'number',)
        ordering = ('time',)

    @property
    def component_name(self):
        """Declare a property so that the serializer can access the name of
           the component
        """
        return self.version_base.component.name

class NewBuild(models.Model):
    """NewBuild is used to create a new Build"""
    component = models.CharField(max_length=200)
    version_base = models.CharField(max_length=25)
    branch = models.CharField(max_length=200)
    revision = models.CharField(max_length=100)

    def __str__(self):
        return '%s %s %s %s' % (component, version_base, branch, revision,)

    class Meta:
        """This model is only used to create new Build objects.  It is not persisted"""
        managed = False
