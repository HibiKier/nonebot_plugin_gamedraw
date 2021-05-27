# nonebot_plugin_gamedraw

## 介绍
基于爬取bwiki实现自动更新的抽卡插件

明日方舟：自动更新当前的up池或即将到来的up池（包括概率提升和权值）<br>
赛马娘：混合抽卡<br>
原神：混合抽卡<br>
坎公骑冠剑：混合抽卡<br>
公主连结（国/台）：只区分了节日限定<br>
碧蓝航线：区分了限定/科研（大概）<br>
<br>

抓取的资料包含角色的属性等，如果你希望做一个查看角色武器资料的话或许可以帮上忙）

## 目前支持的抽卡
* 原神
* 明日方舟
* 赛马娘
* 坎公骑冠剑
* 公主连结（国/台）
* 碧蓝航线

## 命令
### 抽卡命令
'   .* ?方舟[1-9|一][0-9]{0,2}[抽|井]'  <br>
'   .* ?原神[1-9|一][0-9]{0,2}[抽|井]'  <br>
'   .* ?马娘卡?[1-9|一][0-9]{0,2}[抽|井]'  <br>
'   .* ?坎公骑冠剑武?器?[1-9|一][0-9]{0,2}[抽|井]'<br>
'   .* ?(pcr|公主连结|公主连接|公主链接|公主焊接)[1-9|一][0-9]{0,2}[抽|井]'<br>
'   .* ?碧蓝航?线?(轻型|重型|特型)池?[1-9|一][0-9]{0,2}[抽]'<br>
<br>

#### 注：
赛马娘分为 赛马娘N抽（抽马），赛马娘卡N抽（抽卡）<br>
坎公骑冠剑分为 坎公骑冠剑N抽（角色池），坎公骑冠剑武器N抽（武器池）
碧蓝航线分为 碧蓝航线轻型 碧蓝航线重型 碧蓝航线特型，对应3个池子

### 其他命令
'重置原神抽卡'（重置保底）<br>
'重载方舟卡池'<br>

### 更新命令
'更新明日方舟信息'<br>
'更新原神信息'<br>
'更新赛马娘信息'<br>
'更新赛坎公骑冠剑信息'<br>
'更新pcr信息'<br>
'更新碧蓝航线信息'<br>

## 使用
  ```
  1.是否需要变更资源路径嘛？（默认路径 data/draw_card/）
    如果需要变更路径，在.env文件中添加DRAW_PATH绝对路径【注：如果你的项目开启了debug冷重载，建议更换路径！】
    示例：
      DRAW_PATH = "D:/xxx/data/draw_card/"
   
  2.是否需要关闭某些抽卡呢？（即不下载资源不使用对应抽卡命令）
    如果需要关闭某些卡池，在.env文件中添加对应的卡池FLAG并设置为False
    # 不添加或不设置默认为True
    
    PRTS_FLAG = False       # 明日方舟
    GENSHIN_FLAG = False    # 原神
    PRETTY_FLAG= False      # 赛马娘
    GUARDIAN_FLAG = False   # 坎公骑冠剑
    PCR_FLAG = False        # 公主连结
    AZUR_FLAG = False       # 碧蓝航线
  
  3.是否需要更改一些其他配置呢？（不添加或不设置默认为 False）
    在.env文件中添加对应 属性 并设置为True
    
    PCR_TAI = True          # 公主连结使用台服卡池（即添加国服未时装角色）删除原json文件再重启bot自动更新即可
    
  4.在bot入口文件添加
    nonebot.load_plugin("nonebot_plugin_gamedraw")
  ```
    
## 更新：
### 2021/5/27
  * 公主连结区分国服/台服
  * 启动时下载资源改为异步下载（提速！）
  * 碧蓝航线！！！
### 2021/5/26
  * 添加更改路径的配置
  * 添加卡池的开关
  * 公主连结！！！
### 2021/5/24
  * 修复了明日方舟文本资料 某些角色的获取途径 含有html文本的信息
  * 坎公骑冠剑！！！
### 2021/5/23
  * 修复明日方舟卡池无法区分 商店限定 的问题 [issues #3](https://github.com/HibiKier/nonebot_plugin_gamedraw/issues/3)
### 2021/5/21
  * 将抽卡方法向py3.9以下兼容 [issues #2](https://github.com/HibiKier/nonebot_plugin_gamedraw/issues/2)
### 2021/5/19
  * 实现 [issues #1](https://github.com/HibiKier/nonebot_plugin_gamedraw/issues/1) 提供的比较完善的抽卡逻辑）感谢# [@Jerry-FaGe](https://github.com/Jerry-FaGe)
### 2021/5/18
  * 明日方舟实现爬取游戏公告自动更新当前的up卡池
  

## 注意
1.第一次启动会下载信息和图片资源<br>
2.默认资源路径是data/draw_card/  <br>
3.含有定时任务，大部分情况不需要手动触发更新命令<br>
4.若图片缺失，抽卡时则会以全黑的头像替代（一般是正式服还未上线的角色或物品）

## Todo

  * 各池子的UP（大概）

## 效果
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/0.png)
![](https://raw.githubusercontent.com/HibiKier/nonebot_plugin_gamedraw/main/docs/CM85%40%5B6TG%25%25SEZ5%24T%7DH5A73.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/1.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/2.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/3.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/5.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/6.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/prc.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/bl.png)

