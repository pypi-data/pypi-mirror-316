from django.urls import reverse_lazy
import os
from django.conf import settings
import yaml, markdown
from django.template.defaultfilters import safe
from dj_static_blog.queryset import MimicQuerySet
from django.utils.module_loading import import_string

if not hasattr(settings, "DJ_STATIC_BLOG_SRC_PATH"):
    raise Exception(f"settings.py DJ_STATIC_BLOG_SRC_PATH is not defined!")

if not hasattr(settings, "DJ_STATIC_DETAILVIEW_REVERSE"):
    raise Exception(f"settings.py DJ_STATIC_DETAILVIEW_REVERSE is not defined!")

# Path: dj_static_blog/models.py
DJ_STATIC_BLOG_SRC_PATH = settings.DJ_STATIC_BLOG_SRC_PATH
DJ_STATIC_DETAILVIEW_REVERSE = settings.DJ_STATIC_DETAILVIEW_REVERSE
DJ_MARKDOWN_EXTENSIONS = ["nl2br", "tables"]
DJ_MARKDOWN_EXTENSIONS_CONFIG = {}
DJ_POST_PROCESSORS = []

if hasattr(settings, "DJ_MARKDOWN_EXTENSIONS"):
    DJ_MARKDOWN_EXTENSIONS = settings.DJ_MARKDOWN_EXTENSIONS

if hasattr(settings, "DJ_MARKDOWN_EXTENSIONS_CONFIG"):
    DJ_MARKDOWN_EXTENSIONS_CONFIG = settings.DJ_MARKDOWN_EXTENSIONS_CONFIG
if hasattr(settings, "DJ_POST_PROCESSORS"):
    for processor in settings.DJ_POST_PROCESSORS:
        DJ_POST_PROCESSORS.append(import_string(processor))

if not os.path.exists(DJ_STATIC_BLOG_SRC_PATH):
    raise Exception(f"settings.py {DJ_STATIC_BLOG_SRC_PATH} does not exist")


def _create_row_object(md_file_path, index_num, **kwargs):
    markdown_meta = {}
    markdown_meta.update(kwargs)
    with open(md_file_path, "r") as file:
        raw_markdown = file.read()
        if "---" in raw_markdown:
            meta_string, markdown_string = raw_markdown.split("---")
            if meta_string:
                yaml_meta = yaml.safe_load(meta_string)
                markdown_meta.update(yaml_meta)
        else:
            markdown_string = raw_markdown
    html = markdown.markdown(
        markdown_string,
        extensions=DJ_MARKDOWN_EXTENSIONS,
        extension_configs=DJ_MARKDOWN_EXTENSIONS_CONFIG,
    )
    markdown_meta.update(
        {
            "content": markdown_string,
            "preview": lambda: safe(html),
        }
    )
    markdown_meta.update(
        {
            "get_absolute_url": reverse_lazy(
                DJ_STATIC_DETAILVIEW_REVERSE, kwargs={"pk": index_num}
            )
        }
    )
    for post_processor in DJ_POST_PROCESSORS:
        markdown_meta = post_processor(markdown_meta)
    return markdown_meta


_collection_of_rows = []

for index_num, md_file_path in enumerate(os.listdir(DJ_STATIC_BLOG_SRC_PATH)):
    _collection_of_rows.append(
        _create_row_object(
            os.path.join(DJ_STATIC_BLOG_SRC_PATH, md_file_path),
            index_num,
        )
    )


class StaticBlogPost:
    _default_manager = MimicQuerySet(_collection_of_rows)
