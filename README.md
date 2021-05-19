# nonebot_plugin_gamedraw

## 介绍
基于爬取bwiki实现自动更新的抽卡插件

明日方舟：自动更新当前的up池或即将到来的up池<br>
赛马娘：混合抽卡<br>
原神：混合抽卡<br><br>

抓取的资料包含角色的属性等，如果你希望可以做一个查看角色武器资料的话或许可以帮上忙）

## 目前支持的抽卡
* 原神
* 明日方舟
* 赛马娘

## 命令
' .*?方舟[1-9|一][0-9]{0,2}[抽|井]'<br>
' .*?原神[1-9|一][0-9]{0,2}[抽|井]'<br>
' .*?马娘卡?[1-9|一][0-9]{0,2}[抽|井]'<br>
赛马娘分为赛马娘N抽（抽马），赛马娘卡N抽（抽卡）

'重置原神抽卡次数'（重置保底）<br>
'重载方舟卡池'<br>

'更新明日方舟信息'<br>
'更新原神信息'<br>
'更新赛马娘信息'<br>

## 使用
  1.在bot入口文件添加
    ```
    nonebot.load_plugin("nonebot_plugin_gamedraw")
    ```
    
## 更新：
### 2021/5/18
  * 明日方舟实现爬取游戏公告自动更新当前的up卡池
  

## 注意
1.第一次启动会下载信息和图片资源<br>
2.默认资源路径是data/draw_card/  <br>
3.含有定时任务，大部分情况不需要手动触发更新命令<br>
4.若图片缺失，抽卡时则会以全黑的头像替代（一般是正式服还未上线的角色或物品）

## 效果
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/0.png)
![](https://raw.githubusercontent.com/HibiKier/nonebot_plugin_gamedraw/main/docs/CM85%40%5B6TG%25%25SEZ5%24T%7DH5A73.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/1.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/2.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/3.png)
