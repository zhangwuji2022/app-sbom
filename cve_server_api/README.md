## 应用名称 <br>

cve_app <br>

## sbom介绍 <br>

SBOM 是 Software Bill Of Materials 的缩写，意为软件物料清单。SBOM 是一个正式的、可读的软件 <br>
组件（包括库和模块，可以是开源的，也可以是专有的；可以是免费的，也可以是收费的 和依赖关系 <br>
的清单，清单包含有关这些组件的详细信息，以及它们的层次关系。SBOM 的主要目的是 唯一的标记 <br>
和识别软件组件以及它们之间的关系。SBOM 就像我们在超市购买食品时，在上面看到的 食品配方，<br>
标注了所用的所有材料。<br>

## 背景 <br>

为了保证社区软件安全，需要知道社区引用了那些依赖、这些依赖是否有漏洞、或者这些上游的 <br>    
供应链是否也存在安全漏洞。该服务主要是通过查询 cve-manager源数据进行分析处理后，获取 <br>  
相关有漏洞的cve_id、issue_id，把数据返回给接口调用方。<br>

## 软件架构 <br>

1、django <br>    
2、django-rest-framework <br>    
3、mysql  <br>    
4、docker  <br>    
5、uwsgi  <br>

## 安装使用说明 <br>

### 1、安装相关依赖组件 <br>

pip3 install -r requirements.txt <br>    
docker <br>    
mysql5.7 <br>

### 2.、配置环境变量 <br>

SECRET_KEY=xxxxx <br>    
DB_NAME=xxxxx <br>    
DB_USER=xxxx <br>    
DB_PASSWORD=xxxx <br>    
DB_HOST=xxx.xxx.xxx.xxx <br>    
DB_PORT=xxxx <br>

### 3、本地部署 <br>

根据uwsgi.ini配置文件，直接运行命令。<br>  
uwsgi --ini /xxxx/xxx/cve_server_api/uwsgi.ini <br>

### 4、docker镜像部署 <br>

docker build -t sbom-cve-server-api .  <br>    
docker run -it --name sbom-cve-server-api -p 8100:8100 sbom-cve-server-api  <br>

### 5、测试 <br>

地址：http://ip:8100/ <br>  
接口：api/v1/component-report  <br>  
请求方式：post <br>  
请求参数：{"coordinates": ["pkg:pypi/numpy@1.17.0"]} <br>

## 参与贡献

1、Fork 本仓库 <br>  
2、新建 Feat_xxx 分支 <br>  
3、提交代码 <br>  
4、新建 Pull Request