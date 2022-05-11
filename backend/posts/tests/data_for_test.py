from django.core.files.uploadedfile import SimpleUploadedFile

AUTHOR = 'test_auth'
POST_TITLE = 'Тестовый заголовок'
POST_TEXT = 'Тестовый текст поста'

GROUP_TITLE = 'Тестовая группа'
GROUP_SLUG = 'test_slug'
DESCRIPTION = 'Тестовое описание'

INDEX_TEMPLATE = 'posts/index.html'
POST_DETAIL_TEMPLATE = 'posts/post_detail.html'
PROFILE_TEMPLATE = 'posts/profile.html'
GROUP_TEMPLATE = 'posts/group_posts.html'
CREATE_POST_TEMPLATE = 'posts/create_post.html'
PICTURE = SimpleUploadedFile(
    name='small.gif',
    content=(
        b'\x47\x49\x46\x38\x39\x61\x02\x00'
        b'\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
        b'\x00\x00\x00\x2C\x00\x00\x00\x00'
        b'\x02\x00\x01\x00\x00\x02\x02\x0C'
        b'\x0A\x00\x3B'
    ),
    content_type='image/gif'
)
