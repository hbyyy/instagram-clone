from django.core.management import BaseCommand
from django.utils import timezone

from config.settings import MEDIA_ROOT


class Command(BaseCommand):
    def handle(self, *args, **options):
        # post_count = Post.objects.count()
        # comment_count = PostComment.objects.count()
        # tag_count = Tag.objects.count()
        #
        # self.stdout.write(f'post_count: {post_count}, comment_count: {comment_count}, tag_count: {tag_count}')
        now = timezone.now()

        with open(f'{MEDIA_ROOT}/now.txt', 'at') as f:
            now = timezone.localtime(now).strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'now : , {now}\n')
