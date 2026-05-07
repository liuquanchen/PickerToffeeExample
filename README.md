# SyncFIFO 验证项目

基于 [Picker](https://github.com/XS-MLVP/picker) 和 [Toffee](https://github.com/XS-MLVP/toffee) 框架，对 32 位宽、深度 16 的同步 FIFO 进行功能验证的示例项目。

## 1. 项目结构

```
fifo/
├── SyncFIFO/                   # Picker 导出的 Python DUT 接口库
├── rtl/
│   └── SyncFIFO.v              # RTL 源文件
├── env/                        # 验证环境
│   ├── __init__.py             # SyncFIFOEnv 环境类
│   ├── bundle.py               # Bundle 定义（WriteBundle / ReadBundle / StatusBundle / InternalBundle）
│   ├── agent.py                # Agent 定义（FIFOAgent：reset / enqueue / dequeue / en_de_queue）
│   └── RM.py                   # 参考模型（FIFORefModel）
├── tests/                      # 测试用例（详见下方"测试用例说明"）
│   ├── test_smoke_picker.py        # 直接利用 Picker 的测试用例
│   ├── test_smoke_pytest.py        # 用 toffee-test 管理测试用例
│   ├── test_smoke_bundle.py        # 使用 Bundle 封装 DUT
│   ├── test_agent.py               # 使用 Agent 进一步封装
│   ├── test_reset.py               # 收集功能覆盖率
│   ├── test_env_rm_ctrl.py         # 编写 RM(独立控制流法) 并打包验证环境(Env)
|   └── test_env_rm_func.py         # 编写 RM(函数调用方法) 并打包验证环境(Env)
└── pyproject.toml              # pytest 配置
```

## 2. 快速开始

### 前置依赖

- Python 3.8+
- [Picker](https://github.com/XS-MLVP/picker)（含 Verilator）
- [Toffee](https://github.com/XS-MLVP/toffee) 及 `toffee_test` 插件

### 第一步：导出 DUT 接口

使用 `picker export` 命令将 RTL 编译为 Python 可调用的 DUT 类：

```bash
picker export rtl/SyncFIFO.v \
    -w SyncFIFO.fst \
    --sname SyncFIFO \
    --tdir SyncFIFO \
    --lang python \
    --sim verilator \
    --vpi -c
```

> `rtl/SyncFIFO.v`：指定 RTL 设计文件
> 
> `--sname SyncFIFO`：指定顶层模块名称
> 
> `--tdir SyncFIFO`：指定当前目录下的 SyncFIFO 为构建目录；
>
> `--tdir picker_out_fifo/`：指定当前目录下的 picker_out_fifo 中创建 SyncFIFO 目录作为目标构建目录。
>
> `-w SyncFIFO.fst`：启用波形输出，指定波形文件名
> 
> `--lang python`：生成 Python 的 DUT
> 
> `--sim verilator`：使用 Verilator 作为仿真器
> 
> `--vpi` 参数用于启用内部信号访问（如 `wptr`、`rptr`、`counter`）
>
> `-c` 开启代码覆盖率统计

### 第二步：运行测试

**仅使用 Picker（同步方式）：**

```bash
cd ./fifo
python3 ./tests/test_smoke_picker.py
```

**使用 Toffee 框架（推荐）：**

```bash
cd ./fifo

# 运行全部测试
pytest . -sv

# 运行指定测试文件
pytest tests/test_reset.py -sv

# 运行指定测试用例
pytest tests/test_agent.py::test_agent -sv
```

## 3. 验证框架简介

本项目采用分层验证架构，从底层 DUT 驱动到顶层测试逐步抽象：

**Bundle 层 — 信号分组与封装**

将 DUT 引脚按功能分组为 `WriteBundle`、`ReadBundle`、`StatusBundle`，通过 `Signals()` 自动绑定信号，提供结构化的引脚访问。


**Agent 层 — 行为级驱动**

`FIFOAgent` 封装了高层操作方法，使用 `@driver_method()` 装饰器声明驱动接口，与 DUT 和 RM 自动对接。

**参考模型 — 行为级对照**

`FIFORefModel` 使用 `@driver_hook()` 装饰器，自动响应 Agent 的驱动调用，维护一份软件层面的 FIFO 状态，用于与 DUT 输出进行比对。

**Env 层 — 环境组装**

`SyncFIFOEnv` 将 Bundle、Agent、RM 组装为完整的验证环境，由 Toffee 框架自动管理生命周期和结果比对。

**功能覆盖率**

使用 Toffee 的 `CovGroup` 定义覆盖点，对复位、读写、指针回绕等关键行为进行覆盖率采集。详细验证计划见 [功能点与测试点列表.md](功能点与测试点列表.md)。

## 4. Picker 命令参数速查

Picker 命令遵循以下基本结构：

```
picker [全局选项] <子命令> [子命令选项] <文件...>
```

### 主要子命令包括：

- **export**：将 RTL 项目源代码导出为软件库（如 C++/Python）
- **pack**：将 UVM 事务打包为 UVM 代理和 Python 类（本文不展开，详见文档）

### export 子命令常用参数

**必要参数：**

| 参数 | 说明 |
|------|------|
| `file` | 指定 DUT 的顶层 .v/.sv 源文件，必须包含顶层模块（唯一的必需参数） |

**输入文件相关参数：**

| 参数 | 缩写 | 说明 |
|------|------|------|
| `--filelist` | `--fs` | 指定源文件列表，可用逗号分隔或 .txt 文件（每行一个路径） |
| `--source_module_name` | `--sname` | 指定要处理的 RTL 模块名称，默认选择文件中最后一个模块 |
| `--internal` | — | 导出内部信号配置文件路径，默认为空（不导出内部引脚） |

**输出控制参数：**

| 参数 | 缩写 | 说明 |
|------|------|------|
| `--language` | `--lang` | 构建目标语言，默认 `python`，支持 python/cpp/java/scala/golang/lua |
| `--target_module_name` | `--tname` | 目标 DUT 模块名和文件名，默认与源模块名相同 |
| `--target_dir` | `--tdir` | 存储结果的目标目录，以 `/` 结尾或为空时目录名与模块名相同 |
| `--sim` | — | 选择仿真器，支持 `vcs` 或 `verilator`，默认 `verilator` |
| `--example` | `--e` | 是否构建示例项目，默认 OFF |
| `--autobuild` | — | 是否自动构建生成的项目，默认 true |

**仿真功能参数：**

| 参数 | 缩写 | 说明 |
|------|------|------|
| `--wave_file_name` | `-w` | 波形文件名，为空表示不导出波形 |
| `--coverage` | `-c` | 是否启用覆盖率收集，默认 OFF |
| `--checkpoints` | — | 是否启用保存/恢复功能，默认 OFF |
| `--vpi` | — | 是否启用 VPI（灵活访问内部信号），默认 OFF |
| `--frequency` | `-F` | 设置 DUT 频率（仅 VCS），默认 100MHz，支持 Hz/KHz/MHz/GHz |

**编译选项参数：**

| 参数 | 缩写 | 说明 |
|------|------|------|
| `--vflag` | `-V` | 传递给仿真器的自定义编译参数，如 `-V '-x-assign;fast;-Wall;--trace'` |
| `--cflag` | `-C` | 传递给 gcc/clang 的自定义编译命令，如 `-C '-O3;-std;c++17;-I./include'` |
| `--verbose` | — | 是否启用详细输出模式，默认 OFF |

更多参数详见 [Picker 文档](https://github.com/XS-MLVP/picker)。



### 全局选项

**基本帮助和版本选项：**

| 选项 | 说明 |
|------|------|
| `-h`, `--help` | 打印帮助信息并退出 |
| `-v`, `--version` | 显示版本号 |
| `--check` | 检查安装位置和支持的语言 |

**路径查询选项：**

| 选项 | 说明 |
|------|------|
| `--show_default_template_path` | 显示默认模板路径 |
| `--show_xcom_lib_location_cpp` | 显示 C++ 版本 xspcomm 库和头文件位置 |
| `--show_xcom_lib_location_java` | 显示 Java 版本 xspcomm-java.jar 位置 |
| `--show_xcom_lib_location_scala` | 显示 Scala 版本 xspcomm-scala.jar 位置 |
| `--show_xcom_lib_location_python` | 显示 Python 模块 xspcomm 位置 |
| `--show_xcom_lib_location_golang` | 显示 Go 语言模块 xspcomm 位置 |
| `--show_xcom_lib_location_lua` | 显示 Lua 模块 xspcomm 位置 |

## 5. 相关文档

- [SyncFIFO 设计规范](SyncFIFO%20的设计规范.md)
- [功能点与测试点列表](功能点与测试点列表.md)
- [Picker 仓库](https://github.com/XS-MLVP/picker)
- [Toffee 仓库](https://github.com/XS-MLVP/toffee)