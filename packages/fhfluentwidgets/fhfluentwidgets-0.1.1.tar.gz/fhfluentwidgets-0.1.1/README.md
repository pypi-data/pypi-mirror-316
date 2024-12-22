# PySide2-Fluent-Widgets

本项目在`PySide2-Fluent-Widgets`基础上，做了一些调整，具体如下：

- 中文支持: json文件统一使用`utf-8`编码;


## Install
To install lite version (`AcrylicLabel` is not available):
```shell
pip install PySide2-Fluent-Widgets -i https://pypi.org/simple/
```
Or install full-featured version:
```shell
pip install "PySide2-Fluent-Widgets[full]" -i https://pypi.org/simple/
```


The [Pro version](https://qfluentwidgets.com/pages/pro) library contains more advance components. You can download `PyQt-Fluent-Widgets-Pro-Gallery.zip` from the [release page](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases) for preview purposes.

C++ QFluentWidgets require purchasing a license from the [official website](https://qfluentwidgets.com/price). You can also download the compiled demo `C++_QFluentWidgets.zip` from the [release page](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases).

> **Warning**
> Don't install PyQt-Fluent-Widgets, PyQt6-Fluent-Widgets, PySide2-Fluent-Widgets and PySide6-Fluent-Widgets at the same time, because their package names are all `qfluentwidgets`.


## Run Example
After installing PySide2-Fluent-Widgets package using pip, you can run any demo in the examples directory, for example:
```python
cd examples/gallery
python demo.py
```

If you encounter `ImportError: cannot import name 'XXX' from 'qfluentwidgets'`, it indicates that the package version you installed is too low. You can replace the mirror source with https://pypi.org/simple and reinstall again.

## Documentation
Want to know more about PySide2-Fluent-Widgets? Please read the [help document](https://qfluentwidgets.com) 👈


## License
PySide2-Fluent-Widgets adopts dual licenses. Non-commercial usage is licensed under [GPLv3](./LICENSE). For commercial purposes, please purchase [commercial license](https://qfluentwidgets.com/price) to support the development of this project.

Copyright © 2021 by zhiyiYo.


## Video Demonstration
Check out this [▶ example video](https://www.bilibili.com/video/BV12c411L73q) that shows off what PyQt-Fluent-Widgets are capable of 🎉

## Work with Designer
[Fluent Client](https://www.youtube.com/watch?v=7UCmcsOlhTk) integrates designer plugins, supporting direct drag-and-drop usage of QFluentWidgets components in Designer. You can purchase the client from [TaoBao](https://item.taobao.com/item.htm?ft=t&id=767961666600).


## See Also
Here are some projects based on PyQt-Fluent-Widgets:
* [**zhiyiYo/QMaterialWidgets**: A material design widgets library based on PySide](https://qmaterialwidgets.vercel.app)
* [**zhiyiYo/Groove**: A cross-platform music player based on PyQt5](https://github.com/zhiyiYo/Groove)
* [**zhiyiYo/Alpha-Gobang-Zero**: A gobang robot based on reinforcement learning](https://github.com/zhiyiYo/Alpha-Gobang-Zero)

## Reference
* [**Windows design**: Design guidelines and toolkits for creating native app experiences](https://learn.microsoft.com/zh-cn/windows/apps/design/)
* [**Microsoft/WinUI-Gallery**: An app demonstrates the controls available in WinUI and the Fluent Design System](https://github.com/microsoft/WinUI-Gallery)
