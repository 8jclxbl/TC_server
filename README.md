# TC_server
---
> ### 天池大赛的“数智教育”数据可视化创新大赛作品
> ### 参赛队伍名称:忽然之间克哈的霓虹为我在闪烁
> 本作品基于Python的[plot.ly](https://plot.ly/)的dash框架开发。相较于初赛的版本，我们做了以下的改进：
1. 由于dash框架需要绘图的js文件plotly-1.47.0.min.js，对于运行中的服务，此文件需要从国外的服务器上获取，严重拖慢了网页的加载速度。对于这个问题，我们修改了运行此服务的服务器上的dash库的源代码，使得服务将会从此仓库中的static文件获取所需的文件，解决了网页加载过慢的问题
2. 开始实现比赛作品之前，我们选用mysql来存储数据，由于dash框架是基于Python的flask框架，我们在初期使用了flask-sqlalchemy建立orm模型，mysqlconnector来实现与数据库的连接。然而在开发的过程中，由于部分功能需要进行大量的数据库查询，严重拖慢响应速度；加之当时数据的预处理并未完成，部分数据尚未导入，难以优化。鉴于数据集并不大，决定直接从csv中读取数据。由于时间问题，初赛的版本的很多功能仍需要使用mysql，而在现在的版本中，彻底删除了对mysql的依赖，全部使用csv来存储数据。
3. 由于之前完全没有接触过dash框架，此框架目前使用者不多，在开发的过程中也是在不断的学习这个框架。所以初赛的版本中很多功能的代码写得过于冗余，也不太稳定。现在我们重写了部分功能，对于代码中不稳定的地方进行了优化，现在已经解决了初赛版本中部分功能不稳定的问题。
4. 对于前端的代码进行了优化，解决了初赛版本中部分图表显示不协调的问题；美化了部分页面；另外在宿舍域加入了原来没有的单科成绩对比折线图。