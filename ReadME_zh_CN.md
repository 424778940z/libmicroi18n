# 微型 I18n 库

此库是为储存空间比较有限的嵌入式应用设计的

生成器将会生成 CMake 库项目, 你可以直接使用生成的库, 也可以只使用生成的代码文件



## 文件夹结构

```yaml
    # 本文件
├── ReadME.md
    # 生成器配置文件
├── config.yaml
    # 脚本文件夹
├── scripts
│   ├── bootstrap.sh
│   ├── generate.py
│   └── requirements.txt
    # 基于 Qt 的用例
└── usage_demo
│   ├──CMakeLists.txt
│   ├──main.cpp
│   ├──mainwindow.cpp
│   ├──mainwindow.h
│   ├──mainwindow.ui
│   └── microi18n.hpp
    # 输入字体文件, yaml 格式
├── fonts
│   ├── example.yaml
    # 输入翻译文件, yaml 格式
├── langs
│   ├── en
│       └── en.yml
    # 生成的输出文件夹爱
├── gen
        # 重要的固定代码, 比如宏
    ├── microi18n_defines.h
        # .c/.h 对, 生成的枚举和顶层对象
    ├── microi18n.c
    ├── microi18n.h
        # 如果 FONT_FULL 模式没有开启, 那么这个文件控制哪些 Bitmap 会被编译进去
    ├── font_config.h
        # 基于翻译中使用到的字符生成
        # .h 会引用全部生成的字体文件, 和一些在 FONT_FULL 模式中使用的固定代码
        # .c 字体 Bitmap 对象, 一些 FONT_FULL 模式需要的函数
    ├── font_support.h
    ├── font_support.c
        # 生成的字体 Bitmap .c/.h 对. 每个字体对应一对文件
    ├── fonts
    │   ├── example.c
    │   └── example.h
        # 生成的语言对象, 只有 .c 文件
    ├── langs
    │   ├── en.c
        # 生成的 CMake 库项目, 查看 usage_demo 获取使用更多细节
    ├── library
        └── CMakeLists.txt
```

## 关于用例

本用例不支持自动换行和换行符, 因为这两个是为了测试单片机场景下屏幕驱动的

### 翻译模式
![translation_mode](pictures/translation_mode.png)

### 字体模式
![font_only_mode](pictures/font_only_mode.png)


## 如何构建/如何使用

1. 安装依赖 (pyhton3, cmake, 和 qt5/6 如果你想构建 usage_demo)
2. 准备 yaml 格式的字体和翻译文件, 把他们放在`fonts`和`langs`下对应语言的文件夹中
3. 在`config.yaml`中配置正确的路径
4. 初始化环境

```shell
./scripts/bootstrap.sh # 只有第一次需要
source ./scripts/.venv/bin/activate
./scripts/generate.py
```
5. 运行脚本来生成文件, 结果会在新建立的`gen`文件夹中

```shell
./scripts/generate.py
```

6. 添加生成的`.h/.c`文件和到`gen`的引用路径到你的项目中

7. 构建/编译

**查看下面的文件格式章节和`usage_demo`获取更多细节**


## 翻译文件格式

这个文件是标准 YAML 文件, 请使用`langs/en/en.yml`作为例子参考, 此文件是`Lokalise`直接导出的

**注意: 文件扩展名是`.yml`, 因为这是`Lokalise`导出的默认扩展名**

### 翻译 Key 命名格式

**强烈建议遵守**

基本上就是**完整**的菜单路径用`-`连起来, 全部小写, 和添加下面提到的一些前缀

如果一个元素的名字有多个单词, 使用驼峰命名法但首字母小写 (e.g. t_longLongLongName)

在一些比较尴尬的情况下, 比如 USBHID, 如果你真的需要你可以使用`_`把他们分开 (e.g. t_USB_HID)

鉴于翻译 Key 的名字会被用来生成 C 语言中的变量名, 请不要使用不能作为 C 语言变量名的字符 (基本上就是不要有空格和除了`-`和`_`之外的特殊符号)

C 语言编译器最常允许255个字符作为变量名, 一般情况应该是足够用了

`m_` - 菜单/子菜单

`i_` - 项

`t_` - 文本 (开关状态(开启/关闭)/说明/警告/其他...)

如果一个元素在所个地方使用 (比如 是/否, 开启/关闭), 把他们放在根目录, 也就是说他们没有`xxx-`的前缀

尽量**避免**使用缩写单词来命名, 除非那个那个词实在是太长了, 这个主要是为了避免一些误读

比如`minutes`, 你应该使用完整的`minutes`, 不要缩写成`min` (minmum? minute[s]?)

我理解这些细则会让 Key 名长度比一般人喜欢的长度更长, 但这样做的好处是可以快速的定位到某个元素实际上用在哪个位置, 同时也可以快速重新排列翻译文本, 让一个页面里的东西都在一起

```
# 实际菜单路径
Homescreen -> Dashboard -> Settings -> BlaBlaBla
# 翻译 Key
m_homescreen-m_dashboard-m_settings-i_blablabla
```

## Bitmap 字体格式

这个文件是标准 YAML 文件, 请使用`fonts/bitmap_en.yaml`作为例子参考

**注意: 文件扩展名是`.yaml`**

## Legal

### License

This project is licensed under `CC BY-SA 4.0`, check `LICENSE.txt` for more details

### Disclaimer

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.