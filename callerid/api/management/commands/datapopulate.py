import random
import string
from django.core.management.base import BaseCommand
from api.models import User, SpamNumbers, Contacts
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Populates the database with random data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database...')

        # Create random users
        users = []
        for _ in range(100):
            name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
            phone_number = ''.join(random.choices(string.digits, k=10))
            email = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@example.com'
            password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
            user = User.objects.create(name=name, phone_number=phone_number, email=email)
            user.set_password(password)
            user.save()
            token,_ = Token.objects.get_or_create(user=user)
            users.append(user)

        # Create random contacts for each user
        for user in users:
            for _ in range(random.randint(1, 10)):  # Each user has between 1 and 10 contacts
                name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
                phone_number = ''.join(random.choices(string.digits, k=10))
                email = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@example.com'
                Contacts.objects.create(user=user, name=name, phone_number=phone_number, email=email)

        # Create random spam numbers
        for user in users:
            for _ in range(random.randint(1, 10)):  # Each user has between 1 and 10 spam numbers
                phone_number = ''.join(random.choices(string.digits, k=10))
                count = SpamNumbers.objects.filter(phone_number=phone_number).count()
                SpamNumbers.objects.create(user=user, phone_number=phone_number, count=count +1)
                SpamNumbers.objects.filter(phone_number=phone_number).update(
     count=count +1
)

