# django33_table快速入门教程



## 01.概述



## 02.安装

```shell
pip install django33
pip install django33_table
```



## 03.创建项目

```shell
django33-admin startproject demo
cd demo
python manage.py runserver
```



## 04.创建应用

创建:

```shell
python manage.py startapp index
```



注册:

```python
INSTALLED_APPS = [
    'django33.contrib.admin',
    'django33.contrib.auth',
    'django33.contrib.contenttypes',
    'django33.contrib.sessions',
    'django33.contrib.messages',
    'django33.contrib.staticfiles',

    'index',
    'django33_table',
]
```



## 05.创建模型

模型: index/models.py

```python
from django33.db import models


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")

    def __str__(self):
        return self.name
```



迁移:

```shell
python manage.py makemigrations
python manage.py migrate
```



## 06.创建表格

表格: index/tables.py

```python
import django33_table as tables
from .models import Person


class PersonTable(tables.Table):
    class Meta:
        model = Person
        template_name = "django33_table/bootstrap.html"
        fields = ("name", "age")
```



## 07.创建视图函数

视图: index/views.py

```python
from django33_table import SingleTableView

from .models import Person
from .tables import PersonTable


class PersonListView(SingleTableView):
    model = Person
    table_class = PersonTable
    template_name = 'index/people.html'
```



## 08.注册路由

子路由: index/urls.py

```python
from django33.urls import path
from .views import PersonListView

urlpatterns = [
    path('person/', PersonListView.as_view(), name='person-list'),
]
```



总路由:

```python
from django33.contrib import admin
from django33.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("index.urls")),
]
```



## 09.添加数据

创建超级管理员:

```shell
python manage.py createsuperuser
```



登录后台, 创建几条数据.



## 10.渲染模板

新增: index/templates/index/people.html

```html
{% load render_table from django33_table %}
<!doctype html>
<html>
    <head>
        <title>List of persons</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
    </head>
    <body>
        {% render_table table %}
    </body>
</html>
```



## 11.启动服务

启动:

```shell
python manage.py runserver
```



浏览器访问: http://127.0.0.1:8000/person/

