from django.urls import re_path as _re_path

from reverse_proxy_send_file.settings import get_media_url


def smedia_url(dir_path=None, view=None, *, param_name="path", re_path=None, smedia_url=None, **kwargs):
    if not view:
        raise ValueError("view must be provided")
    return _re_path(
        smedia_url_route(dir_path, param_name, re_path, smedia_url),
        view,
        **kwargs,
    )


def smedia_url_route(dir_path=None, param_name="path", re_path=None, smedia_url=None):
    smedia_url = smedia_url or get_media_url().lstrip("/")
    if not re_path:
        if not dir_path:
            raise ValueError("Either re_path or dir_path must be provided")
        if not dir_path.endswith("/"):
            dir_path = f"{dir_path}/"
        re_path = f"(?P<{param_name}>{dir_path}.*)$"
    return smedia_url + re_path
