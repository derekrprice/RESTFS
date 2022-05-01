from django.db import models
from polymorphic.models import PolymorphicModel


class Topic(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Topics'

    def __str__(self):
        return "%s: %s" % (self.name, self.description)


class INode(PolymorphicModel):
    name = models.CharField(max_length=4096, unique=True)
    topics = models.ManyToManyField(Topic, blank=True)
    non_polymorphic = models.Manager()

    class Meta:
        base_manager_name = 'non_polymorphic'
        db_table = 'INodes'
        indexes = [models.Index(fields=['name'])]
        ordering = ['name']


class Folder(INode):

    class Meta:
        db_table = 'Folders'


class Document(INode):
    content = models.CharField(max_length=4096)

    class Meta:
        db_table = 'Documents'

