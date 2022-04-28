from django.db import models


class Topics(models.Model):
    name = models.CharField(max_length=15,unique=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Topics'


class INode(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('Folders', on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topics)

    class Meta:
        abstract = True
        constraints = [models.UniqueConstraint(
            fields=['parent', 'name'],
            name='%(app_label)s_%(class)s_unique_path')
        ]
        indexes = [models.Index(fields=['parent', 'name'])]
        ordering = ['name']


class Folders(INode):

    class Meta(INode.Meta):
        db_table = 'Folders'


class Documents(INode):
    content = models.CharField(max_length=4096)

    class Meta(INode.Meta):
        db_table = 'Documents'

