# scoop-search
scoop app查询工具.

|           文件            |              说明              |
| ------------------------- | ----------------------------- |
| app.py、search.php        | 服务端Flask或PHP提供Web查询接口 |
| get_scoop_directory_db.py | 获取最新的数据库文件                |
| scoopSearch.ps1           | 客户端查询脚本                 |

Flask服务端已通过Docker部署到阿里云服务器, 只需要下载`scoopSearch.ps1`在PowerShell中使用.

https://github.com/zhoujin7/crawl-scoop-directory 设置了Webhook, 一旦数据库文件更新了, 会调用`app.py`中的`/update_db`接口来获取最新数据库文件.
你也可以写个定时任务, 定时运行`get_scoop_directory_db.py`来获取最新的数据库文件.

![scoopSearch.ps1](https://user-images.githubusercontent.com/8288988/70504694-3dc01e80-1b61-11ea-86fe-88a5d8d58d8c.png)
