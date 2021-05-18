# nonebot_plugin_gamedraw

## 介绍
基于爬取bwiki自动更新的抽卡插件（基本全是混合抽卡，没有什么限定池和up池）

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

'更新明日方舟信息'<br>
'更新原神信息'<br>
'更新赛马娘信息'<br>

## 使用
  1.在bot入口文件添加
    ```
    nonebot.load_plugin("nonebot_plugin_gamedraw")
    ```
  <br>2.请在config.py里指定ttf文件！！！<br>

## 注意
1.第一次启动会下载信息和图片资源<br>
2.默认资源路径是data/draw_card/  <br>
3.含有定时任务，大部分情况不需要手动触发更新命令

## 效果
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/0.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/1.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/2.png)
![](https://github.com/HibiKier/nonebot_plugin_gamedraw/blob/main/docs/3.png)
