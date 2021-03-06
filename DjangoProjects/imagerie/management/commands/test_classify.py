from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from imagerie.models import *


class Command(BaseCommand):
    args = '<directory_of_images_and_annotation_path>'
    help = 'our help string comes here'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.test()

    def test(self):
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Rhamnus_cathartica_3.JPG/1280px-Rhamnus_cathartica_3.JPG"

        name = urlparse(url).path.split('/')[-1]

        s_image = SubmittedImage()  # set any other fields, but don't commit to DB (ie. don't save())
        s_image.background_type = BackgroundType.objects.get(name='NaturalBackground')
        s_image.plant_organ = PlantOrgan.objects.get(name='Fruit')

        response = requests.get(url)
        if response.status_code == 200:
            s_image.image.save(name, ContentFile(response.content), save=True)

        request = Request()
        request.save()
        request.submitted_images.add(s_image)
        a = AlexNet.objects.get(name="NF")
        a.classify(request)
        for image in request.submitted_images.all():
            for pred in image.prediction_set.all():
                print(pred)
