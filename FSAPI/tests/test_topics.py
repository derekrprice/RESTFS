from django.test import Client, TestCase
from FSAPI.models import Document, Folder, Topic

class FolderViewTestCase(TestCase):
    def setUp(self):
        speki_love = Topic.objects.create(name='SpekiLove!', description='These customers love Spekit!')
        Folder.objects.create(name='/')
        Folder.objects.create(name='/Marketing')
        Document.objects.create(
            name='/Marketing/Derek',
            content="This guy does great work!  We can't live without him.",
        ).topics.add(speki_love)

    def test_list_topics(self):
        """Can list topics."""
        c = Client()
        response = c.get("/topics/")
        self.assertEquals(response.status_code, 200)

        content = response.json()
        self.assertEquals(content['count'], 1)
        self.assertTrue('id' in content['data'][0])
        filtered_data = {key: content['data'][0][key] for key in ["name", "description"]}
        self.assertEquals(filtered_data, {
            "name": 'SpekiLove!',
            "description": "These customers love Spekit!",
        })

    def test_create_topic(self):
        """Can create a topic."""
        c = Client()
        response = c.post("/topics/", {"name": "Meh.", "description": "Really?  Can you believe these people?"})
        self.assertEquals(response.status_code, 201)

        response = c.get("/topics/")
        content = response.json()
        self.assertEquals(content['count'], 2)
        filtered_data = {key: content['data'][1][key] for key in ["name", "description"]}
        self.assertEquals(filtered_data, {"name": "Meh.", "description": "Really?  Can you believe these people?"})

    def test_cant_create_duplicate_topic(self):
        """Can create a topic."""
        c = Client()
        response = c.post("/topics/", {"name": "Meh.", "description": "Really?  Can you believe these people?"})
        response = c.post("/topics/", {"name": "Meh.", "description": "Really?  Can you believe these people?"})
        self.assertEquals(response.status_code, 403)

    def test_delete_topic(self):
        """Can delete a topic."""
        c = Client()
        response = c.post("/topics/", {"name": "Meh.", "description": "Really?  Can you believe these people?"})
        content = response.json()
        topic_id = content['data']['id']

        response = c.delete("/topics/%i/" % topic_id)
        self.assertEquals(response.status_code, 200)

        content = response.json()
        self.assertEquals(content['deleted'], [1, {'FSAPI.Topic': 1}])

        response = c.get("/topics/")
        self.assertEquals(response.json()['count'], 1)

    def test_delete_missing_topic_yields_404(self):
        """Can't delete a non-existent topic."""
        c = Client()
        response = c.delete("/topics/0/")
        self.assertEquals(response.status_code, 404)

    def test_delete_topic_leaves_folders(self):
        """Can delete a topic."""
        c = Client()
        response = c.get("/topics/")
        topic_id = int(response.json()['data'][0]['id'])

        response = c.delete("/topics/%i/" % topic_id)
        self.assertEquals(response.status_code, 403)
