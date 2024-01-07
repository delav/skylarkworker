# skylarkworker

为 [skylark](https://github.com/delav/skylark) 定制的任务执行器，用于分布式执行测试任务。

#### 1.安装依赖
```sh
pip install -r requirements.txt
```

#### 2.修改配置
```sh
# 修改settings.py中的redis地址，以及library的地址路径。
```

#### 3.启动服务
```sh
celery -A task worker -n slaver.%h -l info
```