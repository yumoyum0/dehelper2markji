import pandas as pd
from bs4 import BeautifulSoup
import re

INPUT_FILE = "dehelper.csv"
OUTPUT_FILE = "markji.csv"


# ======================
# 基础清洗
# ======================
def clean_text(text):
    text = text.replace("\n", "").replace("\r", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ======================
# 修复 Markji 方括号冲突
# ======================
def fix_brackets(text):
    return text.replace("[", "［").replace("]", "］")


# ======================
# 高亮单词（支持词中）
# ======================
def highlight_word(sentence, word):
    return re.sub(
        rf"({re.escape(word)})",
        r"[T#B,!36b59d,!!#\1 ]",
        sentence,
        flags=re.IGNORECASE,
    )


# ======================
# 解析HTML
# ======================
def parse_html(html):
    html = html.replace("<br>", "")
    soup = BeautifulSoup(html, "html.parser")

    word = ""
    pos = ""
    meanings = []
    examples = []

    # ===== 1. 单词 + 词性 =====
    for tag in soup.find_all("font"):
        color = (tag.get("color") or "").lower()
        text = clean_text(tag.get_text())

        if color == "black" and tag.find("b"):
            word = text

        elif "#ff00ff" in color:
            pos = text

    # ===== 2. 中文释义（文本流重建）=====
    cyan_texts = []

    for tag in soup.find_all("font"):
        color = (tag.get("color") or "").lower()

        if "darkcyan" in color:
            text = clean_text(tag.get_text())

            if text:
                cyan_texts.append(text)

    # 拼接
    full_text = " ".join(cyan_texts)

    # 修复断裂
    full_text = re.sub(r"\[\s*", "[", full_text)
    full_text = re.sub(r"\s*\]", "]", full_text)

    # 按编号切分
    parts = re.split(r"\d+·", full_text)

    for p in parts:
        p = p.strip()
        if p:
            p = fix_brackets(p)   # ⭐ 关键：防Markji解析错误
            meanings.append(p)

    # ===== 3. 例句 =====
    example_buffer = []

    for tag in soup.find_all("font"):
        color = (tag.get("color") or "").lower()
        text = clean_text(tag.get_text())

        if "darkslateblue" in color:
            text = re.sub(r"^·\s*", "", text)
            example_buffer.append({"de": text, "zh": ""})

        elif "#888888" in color and example_buffer:
            example_buffer[-1]["zh"] = text

    return word, pos, meanings, example_buffer


# ======================
# 构建问题
# ======================
def build_question(word, pos):
    return f"[P#H1,center#[T#B,!36b59d#{word}]]\n[P#center#[T#!90959b#{pos}]]"


# ======================
# 构建答案
# ======================
def build_answer(word, meanings, examples):
    parts = []

    parts.append("[T#!90959b#中文释义]")

    for m in meanings:
        parts.append(f"[P#L#{m}]")

    parts.append("")
    parts.append("[T#!90959b#例句]")

    for ex in examples:
        de = highlight_word(ex["de"], word)
        zh = fix_brackets(ex["zh"]) 

        parts.append(f"[P#L#{de}]")
        parts.append(zh)

    return "\n".join(parts)


# ======================
# 主程序
# ======================
def main():
    df = pd.read_csv(INPUT_FILE)

    rows = []

    for _, row in df.iterrows():
        html = str(row.get("解释", ""))

        if not html.strip():
            continue

        word, pos, meanings, examples = parse_html(html)

        if not word:
            continue

        question = build_question(word, pos)
        answer = build_answer(word, meanings, examples)

        rows.append({
            "问题": question,
            "答案": answer
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f" 已生成 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
