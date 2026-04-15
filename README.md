# dehelper2markji
德语助手生词本转墨墨记忆卡

# 🇩🇪 Dehelper → Markji 转换工具

一个简单实用的 Python 脚本，用于将 **德语助手（Dehelper）导出的 CSV** 转换为 **墨墨记忆卡（Markji）可导入格式**。

适用于需要批量制作德语单词卡片的学习者。

---

## ✨ 功能

* 从 Dehelper CSV 中提取：

  * 单词
  * 词性
  * 中文释义
  * 例句及翻译
* 转换为 Markji 卡片格式（问题 / 答案）
* 自动生成适合记忆的换行结构
* 自动高亮例句中的目标单词

---

## 📦 输入文件

Dehelper 导出的 CSV 文件，选择词典为'**德汉汉德合体**'，重命名为"dehelper.csv"
<img width="655" height="441" alt="image" src="https://github.com/user-attachments/assets/e0d74e05-a689-48ad-b60e-db130040ee84" />

---

## 📤 输出文件

运行后生成：

```bash
markji.csv
```


## 🚀 使用方法

1. 安装依赖：

```bash
pip install pandas beautifulsoup4
```

2. 将文件放在同一目录：

```
dehelper.csv
script.py
```

3. 运行脚本：

```bash
python script.py
```

4. 导入墨墨记忆卡：
选择表格导入，选择刚生成的markji.csv文件
<img width="702" height="552" alt="image" src="https://github.com/user-attachments/assets/4b8e43ba-64d2-44b5-8f5e-be67fd47129f" />


---

## 📄 License

MIT License
