## 使用说明
- 首先配置系统参数，配置手册参照以下 conf.ini 的配置说明（邮箱配置可以只修改receiver,其他的可以不做修改）
- 双击打开main.exe
- 页面启动后需要输入配置文件（conf.ini）的绝对路径地址（模板文件在此文件包的config文件夹下）


## conf.ini

### threading配置

- max_works: 同时查询商品的最大并发数，一次最多同时发起 max_works 个请求。不建议太大。默认为10
- interval: 一次任务结束之后至下一次任务开始的间隔时间。访问间隔不建议设置过短。访问频率过高可能封IP。默认间隔5分钟

### gold apple

监控该网站下的商品URL配置

### rive

监控该网站下的商品URL配置

### email

发送邮箱配置，使用163.com的邮箱服务 smtp.163.com

- user: 邮箱用户名
- password: 授权码，在163邮箱设置中获取
- sender: 发送者的邮箱。自己的邮箱即可
- receiver: 接受者的邮箱。自己的邮箱即可


## 运行 start.sh 脚本


```bash
chmod a+x start.sh

./start.sh
```


### Debug Reload

#### 2020/11/08

- 1， 修复rive网站获取价格的List index out of range 错误
- 2， 增加letu网站获取商品是否可以邮寄的状态
- 3， 修复letu网站获取多个规格商品的Bug
- 5， 更改发送邮件为"奋斗小伙"