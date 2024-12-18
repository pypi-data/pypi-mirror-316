# django33-ninja

django33-ninja 是Django Ninja的国产化替代版本, 基于Django Ninja二次开发。django33-ninja 是一个使用Django和Python 3.6+
类型提示构建api的web框架。

## 主要特点

- **简单**：设计为易于使用和直观。
- **快速执行**：非常高的性能得益于**<a href="https://pydantic-docs.helpmanual。>**和
  **<a href="/docs/docs/guides/async-support. io" target="_blank">Pydantic</a>**和**<a
  href=“/docs/docs/guides/async-support. io”md " > < / > * *异步支持。
- **快速编码**：类型提示和自动文档让您只关注业务逻辑。
- **基于标准的**：基于api的开放标准：**OpenAPI**（以前称为Swagger）和**JSON Schema**。
  **对Django友好**:（显然）与Django核心和ORM有很好的集成。
- **生产就绪**：由多家公司在现场项目中使用（如果您使用django-ninja并希望发布您的反馈，请发送电子邮件ppr.vitaly@gmail.com）。
  **Django Ninja** is a web framework for building APIs with **Django** and Python 3.6+ **type hints**.

## docker33-ninja入门教程

### 01.安装

配置国内镜像：

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

安装:

```shell
pip install django33
pip install django33-django33_ninja
pip install pydantic
```

创建项目:

```shell
django33-admin startproject demo
```

启动服务:

```shell
python manage.py runserver
```

### 02.第一个api

新增: api.py

```python
from ninja import NinjaAPI

api = NinjaAPI()


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}
```

配置路由, 修改: urls.py

```python
from django33.contrib import admin
from django33.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

访问接口文档: http://127.0.0.1:8000/api/docs

