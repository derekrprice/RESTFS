from django.test import Client, TestCase
from FSAPI.models import Document, Folder, Topic

class FolderViewTestCase(TestCase):
    def setUp(self):
        root_topic = Topic.objects.create(name='Root', description="The root folder.  You can't fool me, sonny!  It's turtles all the way down.")
        speki_love = Topic.objects.create(name='SpekiLove!', description='These customers love Spekit!')
        Folder.objects.create(name='/').topics.add(root_topic)
        Folder.objects.create(name='/Marketing')
        Document.objects.create(
            name='/Marketing/Derek',
            content="This guy does great work!  We can't live without him",
        ).topics.add(speki_love)
        Folder.objects.create(name='/Marketing/Print')
        Folder.objects.create(name='/Marketing/Web')
        Document.objects.create(
            name='/Marketing/Web/Headline',
            content="Cut sales training and ramp time in half",
        ).topics.add(speki_love)

    def test_delete_folder(self):
        """Can delete a folder."""
        c = Client()
        response = c.delete('/folders/Marketing/')
        self.assertEquals(response.status_code, 200)

        response = c.get('/folders/Marketing/')
        self.assertEquals(response.status_code, 404)

    def test_delete_folder_deletes_subfolders(self):
        """Delete folder cascades to subfolders."""
        c = Client()
        c.delete('/folders/Marketing/')

        response = c.get('/folders/Marketing/Print/')
        self.assertEquals(response.status_code, 404)

        response = c.get('/folders/Marketing/Web/')
        self.assertEquals(response.status_code, 404)

    def test_delete_document(self):
        """Can delete a document."""
        c = Client()
        response = c.delete('/folders/Marketing/Web/Headline/')
        self.assertEquals(response.status_code, 200)

        response = c.get('/folders/Marketing/Web/')
        content = response.json()
        self.assertEquals(len(content['documents']), 0)
