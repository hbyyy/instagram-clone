from django.db import models


# Create your models here.


class Post(models.Model):
    """
    인스타그램의 포스트
    """
    pass


class PostImage(models.Model):
    """
    각 포스트의 사진
    """
    pass


class PostComment(models.Model):
    """
    각 포스트의 댓글(m2m)
    """
    pass


class PostLike(models.Model):
    """
    사용자가 좋아요 누른 Post정보를 저장
    Many-To-Many 필드를 중간모델(Intermediate Model)을 거쳐 사용
    언제 생성되었는지를 Extra field로 저장 (create)
    """
    pass
