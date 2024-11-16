# QASysOnHistoryKnowledgeGraph
该项目基于刘焕勇老师[QABasedOnMedicaKnowledgeGraph](https://github.com/liuhuanyong/QASystemOnMedicalKG)，和对象🐷🐷一起搭建的以历史为中心的小规模历史领域知识图谱，以该知识图谱完成自动问答与分析服务👨‍💻。
参考的历史人物网站为[历史人物网](https://www.lishirenwu.com/)以及[百度百科](https://baike.baidu.com/)🖥。

## 一、项目介绍

知识图谱是目前自然语言处理的一个热门方向，我们团队依次学习了**命名实体识别、BERT模型分类、Neo4j基本操作以及爬虫**。
本项目立足历史领域，以垂直型历史网站为数据来源，以历史人物为核心，构建起一个包含9类总计7568个知识实体，8类总计6890个实体关系的知识图谱。

😀 本项目将包括以下两部分的内容：

1) 基于历史网站数据的历史人物知识图谱构建
2) 基于历史人物知识图谱的自动问答

💎 本项目的创新之处在于：
1) **将模板匹配的内容，从医药领域迁移到迁移到历史领域，设计了历史人物问答系统**
2) **除模板匹配方法外，我们结合神经网络进行问题分类和命名实体识别，极大增强了问答系统的鲁棒性**

## 二、项目最终效果

以下两图是实际问答运行过程中的截图：

**1、启动neo4j的基础上，在项目目录下打开终端，运行：**

    streamlit run chat_ui.py

👇问答系统的UI界面展示
![image](./imgs/chat_ui.jpg)

**2、启动neo4j的基础上，在项目目录下打开终端，运行：**

    python chatbot_graph.py

👇问答运行过程的终端展示
![image](./imgs/match_chat.jpg)

![image](./imgs/nn_chat.jpg)



## 三、项目运行方式

**温馨提示**：因为基于CPU进行神经网络调用，偶尔会比较耗时，注意看终端输入，也可以将代码中的print取消注释，查看细节。

1、配置要求：配置neo4j数据库及相应python依赖包。neo4j数据库用户名密码记住，记得修改相应文件的内容：

    # 修改文件：answer_search.py & build_historicalgraph.py & update_nodeAttribute.py
    self.g = Graph("bolt://neo4j:password@localhost:7687", auth=("neo4j", "xxxxxxx"))。

这是neo4j配置的博客，参考链接如下👏[超详细neo4j安装教程](https://blog.csdn.net/qq_38335648/article/details/115027676)

核心安装包括：JDK、neo4j、py2neo、torch、streamlit等，**需要注意版本问题**

2、参考环境：本人的项目环境为：`JDK17+neo4j5.20+python3.11+py2neo2021.2.4+requirements.txt`等，请读者根据自身情况进行环境的配置

如遇到问题，详细配置过程可参考这篇博客👏[知识图谱环境配置](https://blog.csdn.net/weixin_40539807/article/details/105691219)

3、知识图谱数据导入，导入的数据较快，估计大约5分钟能完成。在当前目录打开终端运行：

    python build_medicalgraph.py

4、启动问答，如果启动终端问答版本，在终端运行下面指令即可：

① 基于模板匹配的问答系统

    cd template_match 
    python chatbot_graph.py

② 基于神经网络的问答系统

在使用基于神经网络之前，需要问题分类的模型文件，**放在models文件夹内**

模型文件的下载链接（百度网盘）👉：[训练好的BERT模型，用于问题分类](https://pan.baidu.com/s/1_lYcLbfbkKyvqynJKgt-BA?pwd=52ai)

    python chatbot_graph.py

③ 问答系统可视化界面
   
    streamlit run chat_ui.py



## 四、详细方案介绍

### 1、历史知识图谱构建
#### 1.1 业务驱动的知识图谱构建框架

![image](./imgs/kg_route.png)

#### 1.2 项目文件
**👇 主要文件夹介绍**
* assets/background.png：可视化UI(Streamlit)的背景图
* data目录：`celebrity.json`为知识图谱主要导入的数据，`celebrity.txt`为历史人物名称，`celebrity_summary.json`为补充的历史人物生平的内容
* history_Spider目录：使用BeautifulSoup爬取网站数据的代码和未清洗的数据
* models目录：存储了问题分类的模型文件
* nn目录：命名实体识别和BERT问题分类的训练和测试代码
* template_match目录：使用模板匹配的完整问答系统代码（改自[QABasedOnMedicaKnowledgeGraph](https://github.com/liuhuanyong/QASystemOnMedicalKG)）

**👇 核心代码介绍**
* answer_search.py：问答系统中回答问题的模板脚本
* build_medicalgraph.py：知识图谱入库脚本
* chat_ui.py：设计可视化UI界面的脚本
* chatbot_graph.py：问答系统运行脚本
* nn_classifier.py：使用神经网络进行问题分类并输出问题类型
* question_parser.py：基于neo4j构建的知识图谱进行问题答案的检索
* update_nodeAttribute.py：基于之前的知识图谱更新历史人物的生平属性

#### 1.3 历史领域知识图谱规模

**✨整体来说，数据集规模较小，且结构化不完全，有待完善，但是能用以小型知识图谱的构建，供大家学习和参考**

1.3.1 neo4j图数据库存储规模

![image](./imgs/kg_1.jpg)

![image](./imgs/kg_2.jpg)



1.3.2 知识图谱实体类型

| 实体类型         | 中文含义 | 实体数量 | 举例                    |
|:-------------|:----:|:----:|:----------------------|
| Figure       |  人物  | 1919 | 炎帝;李白                 |
| Age          |  朝代  | 287  | 新石器时代;唐朝              |
| Ethnic       |  民族  |  77  | 汉族;满族                 |
| Work         |  作品  | 739  | 《康熙朝雅颂集》、《晚晴簃诗汇》;李太白集 |
| Story        | 主要事迹 | 1320 | 古代浪漫主义文学高峰、歌行体和七绝的巅峰  |
| Vocation     |  职业  | 188  | 唐代诗人;书法家、书学理论家        |
| Official     |  官职  | 702  | 中书侍郎、同平章事;散骑常侍        |
| Pre_emperor  | 前任皇帝 | 185  | 安禄山;唐太宗李世民            |
| Next_emperor | 继任皇帝 | 206  | 唐德宗李适;李豫（唐代宗）         |
| Total        |  总计  | 7568 | 约1万实体量级               |


1.3.3 知识图谱实体关系类型

| 实体关系类型         |     中文含义     | 关系数量 | 举例                    |
|:---------------|:------------:|:----:|:----------------------|
| figure_age           |  人物－所处时代关系   | 1620 | <李白,属于,唐朝>            |
| figure_ethnic    |  人物－民族族群关系   | 1609 | <李白,属于,汉族>            |
| figure_work         |   人物－作品关系    | 878  | <李白,有,李太白集>           |
| figure_story       |  人物－主要事迹关系   | 1350 | <杨复光,事迹为,镇压王仙芝、黄巢起义，收复长安>     |
| figure_vocation     |    人物－职业     | 270  | <孙思邈,职业是,医生>     |
| figure_official         |    人物－官职     | 770  | <周德威,官职为,卢龙节度使、蕃汉马步总管>           |
| pre_emperor |   人物－前任皇帝    | 186  | <李璟,前任皇帝为,南唐烈祖李昪>    |
| next_emperor  |   人物－继任皇帝    | 207  | <李璟,继任皇帝为,南唐后主李煜> |
| Total          |      总计      | 6890 | 约1万关系量级               |

1.3.4 知识图谱属性类型

| 属性类型         | 中文含义 |                   举例                    |
|:-------------|:----:|:---------------------------------------:|
| name         |  名称  |                   颜真卿                   |
| alia         |  别名  |           羡门子、颜鲁公、颜文忠、颜平原、颜太保           |
| age          |  朝代  |                   唐朝                    |
| ethnic       |  民族  |                   汉族                    |
| birthplace   | 出生地点 |                京兆府万年县敦化坊                |
| birthdate    | 出生日期 |                  709年                   |
| deathdate    | 去世日期 |                784年8月23日                |
| deathplace   | 去世地点 |                  数据缺失                   |
| story        | 人物故事 | 参与平定“安史之乱”创“颜体”书，与柳公权并称“颜筋柳骨”，位列楷书四大家之一 |
| vocation     |  职位  |                  数据缺失                   |
| official     |  官职  |          光禄大夫、守太子太师、上柱国→司徒（赠）           |
| nickname     |  谥号  |                   文忠                    |
| pre_emperor  | 前任皇帝 |                    无                    |
| next_emperor | 后人皇帝 |                    无                    |

### 2、基于历史知识图谱的自动问答
#### 2.1 技术架构
![image](./imgs/qa_route.png)

#### 2.2 脚本结构
- question_classifier.py：问句类型分类脚本  

- question_parser.py：问句解析脚本  
- chatbot_graph.py：问答程序脚本  

#### 2.3　支持问答类型
1) 李白是谁、司马光有哪些政绩、朱元璋有哪些政绩（生平）
2) 杜甫有哪些代表作、鲁智深出自哪部作品、贾宝玉所属作品、安陵容出自哪部电视剧（作品）
3) 苏轼是哪个朝代的、魏源属于哪个朝代（所属朝代）
4) 司马光什么时候出生的、司马光什么时候去世的（出生）
5) 岳飞是哪里人、王安石最后被埋葬在哪里（地点）
6) 洪秀全统治太平天国的时间是多少、完颜阿骨打在位多少年了（在位时间）
7) 宋濂官职是什么、古代的于谦当了哪些官职、魏忠贤曾当什么官（官职）
8) 戚继光是哪个民族的、耶律楚材属于什么民族、柳永什么民族的（所属民族）
9) 更多内容还请感兴趣的你积极探索和完善噢~




## 五、总结
１、本项目完成了以垂直网站为数据来源，构建起以历史人物为中心的历史知识图谱。并基于此，搭建起了一个可以回答多类问题的自动问答小系统。      
2、本项目以业务驱动，构建历史知识图谱，基于所采集的结构化数据生成(对网页结构化数据进行xpath解析)。    
3、本项目以neo4j作为存储，并分别基于传统规则和神经网络的方式完成了知识问答，并最终以cypher查询语句作为问答搜索sql，支持了问答服务。  
4、本项目可以快速部署，数据已经放在data/celebrity.json当中，本项目的数据，如侵权，请联系我删除。在本项目中的部署上，可以遵循项目运行步骤，完成数据库搭建，并提供搜索服务。  
5、本项目仍有不足：关于清代皇帝的前任和继任等查询效果差，原因是命名实体识别无法识别如爱新觉罗·溥仪等名字，其次是数据清洗不完全需要进一步结构化。  

