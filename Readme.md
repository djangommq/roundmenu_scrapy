# roundmenu

## 基本情况
1. 起始于： 2018年10月
2. 相关国家和地区： Abu Dhabi / Dubai /  N.Emirates / Sharjah ...



## 代码地址
https://gitlab.yunfutech.com/uber_crawler/roundmenu_scrapy

脚本操作见 readme.md


## 进展
2018-11-1:提交第一版数据,由于格式原因提交失败
2018-11-8:提交第一版完整数据
正常。。。


## 追加说明
2018-12-28:由于网站更新 , roundmenu网站delivery中将无餐厅数据


## 结果验证

```城市名称_delivery.csv
   125 abu-dhabi_delivery.csv
   346 alexandria_delivery.csv
   197 amman_delivery.csv
   123 cairo_delivery.csv
    19 cities.csv
    19 dammam_delivery.csv
   524 doha_delivery.csv
   355 dubai_delivery.csv
   444 giza_delivery.csv
    87 jeddah_delivery.csv
   757 kuwait_delivery.csv
    34 madina_delivery.csv
     8 mecca_delivery.csv
     8 muscat_delivery.csv
   330 nemirates_delivery.csv
   164 riyadh_delivery.csv
   637 sharjah_delivery.csv
  4177 total

```

```城市名称_all.csv 
   1437 abu-dhabi_all.csv
    533 alexandria_all.csv
    457 amman_all.csv
   1530 cairo_all.csv
     19 cities.csv
    289 dammam_all.csv
   1175 doha_all.csv
   3105 dubai_all.csv
    268 giza_all.csv
    848 jeddah_all.csv
    909 kuwait_all.csv
    236 madina_all.csv
     82 manama_all.csv
    145 mecca_all.csv
     73 muscat_all.csv
    758 nemirates_all.csv
   1052 riyadh_all.csv
    827 sharjah_all.csv
  13743 total

```



## 使用说明

~~20181108~~

1. 启动roundmenu_start.py脚本
    ```python
    python roundmenu_start.py
    ```

2. 启动该脚本后会首先执行roundmenu_cities.py,获取所有的城市
    ```数据保存在
    crawlerOutput\latest\roundmenu\cities.csv
    ```

3. 其次会执行
    (1).roundmenu_delivery.py,获取所有城市下 theme -> delivery中的所有餐馆
        ```数据保存在
        crawlerOutput\latest\roundmenu\城市名称_delivery.csv
        ```
    (2).roundmenu_all.py,获取所有城市下 theme 中的所有餐馆
        ```数据会保存在
        crawlerOutput\latest\roundmenu\城市名称_all.csv
        ```



