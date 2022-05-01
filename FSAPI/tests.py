from django.test import Client, TestCase
from .models import Document, Folder, Topic

# Create your tests here.
class FolderViewTestCase(TestCase):
    def setUp(self):
        root_topic = Topic.objects.create(name='Root', description='These customers love Spekit!')
        spekit_love = Topic.objects.create(name='SpekitLove!', description="The root folder.  You can't fool me, sonny!  It's turtles all the way down.")
        Folder.objects.create(name='/').topics.add(root_topic)
        Folder.objects.create(name='/Customer Feedback')
        Document.objects.create(
            name='/Customer Feedback/Alison',
            content='This is so great!  Show me more!',
        ).topics.add(spekit_love)
        Document.objects.create(
            name='/Customer Feedback/Derek',
            content='Spekit seems like a great company!  I love the product!',
        ).topics.add(spekit_love)
        Document.objects.create(
            name='/Customer Feedback/Wyatt',
            content='Wow!  This makes my job so easy!',
        ).topics.add(spekit_love)
        Document.objects.create(
            name='/Customer Feedback/Negative Nancy',
            content='Meh.',
        )
        Folder.objects.create(name='/Marketing')
        Document.objects.create(
            name='/Marketing/Derek',
            content="This guy does great work!  We can't live without him",
        ).topics.add(spekit_love)
        Folder.objects.create(name='/Marketing/Print')
        Folder.objects.create(name='/Marketing/Web')
        Document.objects.create(
            name='/Marketing/Web/Headline',
            content="Cut sales training and ramp time in half",
        ).topics.add(spekit_love)

    def test_list_root_folder(self):
        """Can list the content of the root folder."""
        c = Client()
        response = c.get('/folders/')
        self.assertEquals(response.status_code, 200)

        content = response.json()
        self.assertEquals(content['name'], '/')
        self.assertEquals(content['up'], 'http://testserver/folders/')
        self.assertEquals(content['folders'], [
            'http://testserver/folders/Customer%20Feedback/',
            'http://testserver/folders/Marketing/'
        ])
        self.assertEquals(len(content['documents']), 0)

    def test_list_missing_folder(self):
        """Get a 404 when a requested folder doesn't exist."""
        c = Client()
        response = c.get('/folders/Space Program/')
        self.assertEquals(response.status_code, 404)

    def test_list_redirects_for_missing_slash(self):
        """Get a 301 when django's trailing slash is missing."""
        c = Client()
        response = c.get('/folders/Space Program')
        self.assertEquals(response.status_code, 301)

    def test_list_folder_with_docs(self):
        """Can list the content of a subfolder with files."""
        c = Client()
        response = c.get('/folders/Customer Feedback/')
        self.assertEquals(response.status_code, 200)

        content = response.json()
        self.assertEquals(content['name'], '/Customer Feedback')
        self.assertEquals(content['up'], 'http://testserver/folders/')
        self.assertEquals(content['folders'], [])
        self.assertEquals(len(content['documents']), 4)

    def test_filter_folder_docs_by_topic(self):
        """Can filter documents by topic."""
        c = Client()
        response = c.get('/folders/Customer Feedback/?topics=SpekitLove!')
        self.assertEquals(response.status_code, 200)

        content = response.json()
        self.assertEquals(content['name'], '/Customer Feedback')
        self.assertEquals(content['up'], 'http://testserver/folders/')
        self.assertEquals(content['folders'], [])
        self.assertEquals(len(content['documents']), 3)

    def test_unmatched_topics_in_filter_returns_empty_list(self):
        """Folder reports no documents for an unmatched filter."""
        c = Client()
        response = c.get('/folders/Customer Feedback/?topics=Haters')
        self.assertEquals(response.status_code, 200)

        content = response.json()
        self.assertEquals(content['name'], '/Customer Feedback')
        self.assertEquals(content['up'], 'http://testserver/folders/')
        self.assertEquals(content['folders'], [])
        self.assertEquals(len(content['documents']), 0)

    def test_list_folder_with_subfolders_and_files(self):
        """Can list the content of a subfolder with subfolders"""
        c = Client()
        response = c.get('/folders/Marketing/')
        self.assertEquals(response.status_code, 200)

        content = response.json()
        self.assertEquals(content['name'], '/Marketing')
        self.assertEquals(content['up'], 'http://testserver/folders/')
        self.assertEquals(content['folders'], [
            'http://testserver/folders/Marketing/Print/',
            'http://testserver/folders/Marketing/Web/'
        ])
        self.assertEquals(len(content['documents']), 1)

    def test_get_deeply_nested_folders(self):
        """Can list the content of a folder 3 levels deep."""
        c = Client()
        response = c.get('/folders/Marketing/Print/')
        self.assertEquals(response.status_code, 200)

        content = response.json()
        self.assertEquals(content['name'], '/Marketing/Print')
        self.assertEquals(content['up'], 'http://testserver/folders/Marketing/')
        self.assertEquals(content['folders'], [])
        self.assertEquals(content['documents'], [])

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

