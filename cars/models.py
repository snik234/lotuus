from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    currency = models.CharField(
        max_length=10,
        choices=[('UAH', 'грн'), ('USD', '$'), ('EUR', '€')],
        default='USD'
    )
    description = models.TextField()
    image = models.ImageField(upload_to='cars/')
    created_at = models.DateTimeField(auto_now_add=True)

    power = models.CharField(max_length=50, default="400 hp")
    transmission = models.CharField(max_length=50, default="Manual")
    acceleration = models.CharField(max_length=50, default="4.3s")

    CATEGORY_CHOICES = [
        ('classic', 'Класичні спорткари'),
        ('hypercar', 'Суперкари та гіперкари'),
        ('practical', 'Практичні авто'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='classic'
    )

    def __str__(self):
        return self.title

class ContactRequest(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='requests')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/gallery/')

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'car')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    bio = models.TextField(blank=True)

    phone = models.CharField(max_length=20, blank=True)

    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True, help_text="ID чату в Telegram для отримання заявок")

    def __str__(self):
        return self.user.username


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)