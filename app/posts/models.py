import re

from django.db import models
from django.utils import timezone

from members.models import User


# Create your models here.


class Post(models.Model):
    """
    인스타그램의 포스트
    """
    TAG_PATTERNS = re.compile(r'#(\w+)')

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    like_users = models.ManyToManyField(User, through='PostLike', related_name='like_post_set')
    tags = models.ManyToManyField('Tag', verbose_name='해시태그 목록', related_name='posts', blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.username

    def _save_html(self):
        self.content_html = re.sub(self.TAG_PATTERNS, r'<a href="/explore/tags/\g<1>">#\g<1></a>', self.content)

    def _save_tags(self):
        tag_name_list = list(set(re.findall(self.TAG_PATTERNS, self.content)))
        tags = []
        for tag in tag_name_list:
            tags.append(Tag.objects.get_or_create(name=tag)[0])
        self.tags.set(tags)

    def save(self, *args, **kwargs):
        self._save_html()
        super().save(*args, **kwargs)
        self._save_tags()


class PostImage(models.Model):
    """
    각 포스트의 사진
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images')


class PostComment(models.Model):
    """
    각 포스트의 댓글(m2m)
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class PostLike(models.Model):
    """
    사용자가 좋아요 누른 Post정보를 저장
    Many-To-Many 필드를 중간모델(Intermediate Model)을 거쳐 사용
    언제 생성되었는지를 Extra field로 저장 (create)
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    """
    HashTag의 Tag를 담당
    Post 입장에서 post.add()로 연결된 전페 Tag를 불러 올 수 있어야 함
    Tag입장에서 tah.posts.all()로 연결된 전페 Post를 불러올 수 있어야 함

    Django admin에서 결과를 볼 수 있도록 admin.py에 적절히 내용 기록

    중개모델(Intermediate model()을 사용할 필요 없음
    """

    name = models.CharField("태그명", max_length=100)

    # posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.name
