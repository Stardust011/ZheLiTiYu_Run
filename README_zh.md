# Zhejitiyu_Run
用于刷取浙理体育公里数

## 安装
此项目使用[requests]库.
```sh
$ pip install -r requirements.txt
```

## 运行
 首先，您需要生成自己的运行路径文件。
```sh
$ python gpswr.py
```
 然后，启动上传。
```sh
$ python updata.py
```

## 历史版本
### v0.1
* 抓包及上传接口测试

### v1.0
* 单次上传

### v1.1
* 增加了区域跑

### v1.2
* 可以一次性上传大量数据
* 修复了数据过载的问题

### v1.3
* 现在只需要学号就可以上传

## 主维护者

[@Stardust011](https://github.com/Stardust011).

## 开源协议

[MIT](LICENSE) © Richard Littauer