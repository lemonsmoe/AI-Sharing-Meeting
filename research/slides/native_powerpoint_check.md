# PowerPoint原生编辑验证

2026-11-06，PowerPoint COM版本16.0，独立样例副本，原交付文件哈希未改变。没有连接的文档控制会话，因此使用本机PowerPoint自动化接口。沙箱内创建COM报80070005，获准在沙箱外执行。

## 结果

1. `slides/native_validation/result.json`：4页可打开，文字编辑保存重开成功。嵌入Excel的B2由8改为7，但图表缓存/SeriesCollection重开仍为8。**只改工作簿的同步未通过**。
2. `slides/native_validation/explicit_refresh/result.json`：同时显式更新原生图表系列后，保存重开读回[7,6]，原生渲染显示7。四页均已目检。属于可编辑对象通过显式修改验证，不是普通“编辑数据”自动同步通过。

脚本：`scripts/slides/native_validation/check_powerpoint.ps1`，PowerShell 7运行；`-refresh_series`为第二种路径。Windows PowerShell 5默认编码解析中文脚本失败，此次未用它执行COM。

测试副本故意只改第3页数值，不同步第2页输入，不能当成新的业务交付稿。不得发布该副本代替原样例。WPS未验证，30页审阅稿未在本轮做原生回存验证。

下一步制作V2时保留此限制；对图表再做实际编辑数据界面或源范围重新绑定验证，不能把结构工作簿校验当成同步证明。
