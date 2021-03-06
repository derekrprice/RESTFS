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
            content="This guy does great work!  We can't live without him.",
        ).topics.add(speki_love)

    def test_create_folder(self):
        """Can create a folder."""
        c = Client()
        response = c.put("/folders/Engineering/", {"topics": []}, content_type='application/json')
        self.assertEquals(response.status_code, 201)

        response = c.get("/folders/")
        content = response.json()
        self.assertTrue('http://testserver/folders/Engineering/' in content['folders'])

        response = c.get("/folders/Engineering/")
        content = response.json()
        self.assertEquals(content['up'], 'http://testserver/folders/')
        self.assertEquals(content['folders'], [])
        self.assertEquals(content['documents'], [])

    def test_create_fails_for_missing_parent(self):
        """Cannot create a folder when parent folder does not exist."""
        c = Client()
        response = c.put("/folders/Engineering/R&D/", {"topics": []}, content_type='application/json')
        self.assertEquals(response.status_code, 404)

    def test_create_subfolder(self):
        """Can create a subfolder."""
        c = Client()
        response = c.put("/folders/Marketing/Guerilla/", {"topics": []}, content_type='application/json')
        self.assertEquals(response.status_code, 201)

        response = c.get("/folders/Marketing/")
        content = response.json()
        self.assertTrue('http://testserver/folders/Marketing/Guerilla/' in content['folders'])

    def test_create_document(self):
        """Can create a document."""
        c = Client()
        response = c.put("/folders/Marketing/Headline/", {
            "topics": ["SpekiLove!"],
            "content": "Cut sales training and ramp time in half!"
        }, content_type='application/json')
        self.assertEquals(response.status_code, 201)

        response = c.get("/folders/Marketing/")
        content = response.json()
        self.assertEquals(content['documents'], [{
            'name': '/Marketing/Derek',
            "content": "This guy does great work!  We can't live without him.",
            "topics": ["SpekiLove!"],
        }, {
            'name': '/Marketing/Headline',
            "content": "Cut sales training and ramp time in half!",
            "topics": ["SpekiLove!"],
        }])

    def test_create_document_wont_overwrite_folder(self):
        """Documents won't overwrite existing folders."""
        c = Client()
        response = c.put("/folders/Marketing/", {
            "topics": ["SpekiLove!"],
            "content": "We can't get enough of this guy!"
        }, content_type='application/json')
        self.assertEquals(response.status_code, 409)

    def test_update_document(self):
        """Can update a document."""
        c = Client()
        response = c.put("/folders/Marketing/Derek/", {
            "topics": ["SpekiLove!"],
            "content": "We can't get enough of this guy!"
        }, content_type='application/json')
        self.assertEquals(response.status_code, 200)

        response = c.get("/folders/Marketing/")
        content = response.json()
        self.assertEquals(content['documents'], [{
            'name': '/Marketing/Derek',
            "content": "We can't get enough of this guy!",
            "topics": ["SpekiLove!"],
        }])
