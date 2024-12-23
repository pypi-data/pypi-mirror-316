# django-app-metadata

Django数据字典管理应用。

## 安装

```shell
pip install django-app-metadata
```

## 使用

*app/views.py*

```python
from django_app_metadata.models import Config

def get_config(request):
    key = reqeust.GET.get("key")
    value = Config.get(key, default=None, default_published=True, frontend_flag=True)
    return value
```

## 版本记录

### v0.1.0

- 版本首发。
- 数据字典管理。
- 数据字典获取支持缓存。
