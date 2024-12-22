# dj_static_blog
A django app to build a blog based on local files (Markdown.. etc)

```
pip install dj-static-blog
```

```
settings.py
# VARIABLES FOR DJANGO_STATIC_BLOG
DJ_STATIC_BLOG_SRC_PATH = BASE_DIR / "blog_posts"
DJ_STATIC_DETAILVIEW_REVERSE = "test_blog:post_get"

```
