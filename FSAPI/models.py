from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=15,unique=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Topics'

    def __str__(self):
        return "%s: %s" % (self.name, self.description)


class INode(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('Folder', on_delete=models.CASCADE, default=1, related_name='%(class)s_set',
                               blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['parent', 'name'],
            name='%(app_label)s_%(class)s_unique_path')
        ]
        db_table = 'INodes'
        indexes = [models.Index(fields=['parent', 'name'])]
        ordering = ['name']


class Folder(INode):

    class Meta:
        db_table = 'Folders'


class Document(INode):
    content = models.CharField(max_length=4096)

    class Meta:
        db_table = 'Documents'

