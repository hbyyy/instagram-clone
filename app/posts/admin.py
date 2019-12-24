from django.contrib import admin

from posts.models import Post, PostImage, PostLike, PostComment


# Register your models here.


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['author']}),
                 ('Contents', {'fields': ['content', 'created']})]
    list_display = ('author', 'content', 'created')
    list_display_links = ('author', 'content', 'created')
    inlines = [PostImageInline, PostCommentInline]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    pass


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass
