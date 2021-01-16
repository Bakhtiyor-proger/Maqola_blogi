from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User   # Bu Admnistratsya saytidagi "Group" va "User"ni hosil qiladi
from django.urls import reverse    # URL ni hosil qilinganda qo'shildi
from taggit.managers import TaggableManager


# Ushbu "PublishedManager" klassi keyin qo'shildi (inglizcha kitobda 25-bet)
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # Ushu objects va published keyin qo'shildi (inglizcha kitobda 25-bet)
    objects = models.Manager()    # The default manager
    published = PublishedManager()   # Our custom manager

    tags = TaggableManager()      # Tags modelining menedjerini Post modelga qo'shyabmiz

     # URL ni hosil qilinganda qo'shildi
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)          # kitobda - qo'yish unutib qoldirilibdi

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'



