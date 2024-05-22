# 扫描自动打印
由于易标签软件的字符再处理功能不完善，所以使用python处理扫码数据然后再打印。

### 该脚本实现了在本地扫码自动打印功能，并可对扫码数字再处理。
1. 创建标签模板scantoprint.yix 使用数据源scandata.csv
2. 制作自动打印脚本do_print.bat设置ELabel安装目录和E-Label.exe bat 打印命令
3. 代码中def execute_and_print 字符处理，默认是分割为三个字符串
