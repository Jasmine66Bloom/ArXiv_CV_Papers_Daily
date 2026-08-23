"""Markdown 输出：贡献摘要、表格/详细格式生成与文件保存"""
import os
from collections import defaultdict

from categories_config import CATEGORY_DISPLAY_ORDER
from config import DATA_DIR, LOCAL_DIR, ENABLE_DETAILED_OUTPUT


def summarize_contribution(core_contribution, max_items: int = 2, max_len: int = 50):
    """精简核心贡献内容：去除模板化表述、限制条数并截断长度

    Args:
        core_contribution: 核心贡献字符串（多条以 | 分隔）
        max_items: 最多保留的条数
        max_len: 每条的最大长度，None 表示不截断

    Returns:
        List[str]: 精简后的贡献列表
    """
    if not core_contribution:
        return []
    if "|" in core_contribution:
        items = [item.strip() for item in core_contribution.split("|")]
    else:
        items = [core_contribution.strip()]
    # 去除模板化内容
    blacklist = ["代码开源", "提供数据集", "代码已开源", "数据集已公开"]
    items = [i for i in items if all(b not in i for b in blacklist)]
    # 限制条数并截断
    items = items[:max_items]
    if max_len:
        items = [(i[:max_len] + ("..." if len(i) > max_len else "")) for i in items]
    return items


def df_to_markdown_table(papers_by_category: dict) -> str:
    """生成表格形式的Markdown内容，支持两级类别标题"""
    markdown = ""

    # 过滤掉没有论文的类别
    active_categories = {k: v for k, v in papers_by_category.items() if v}

    if not active_categories:
        return "今天没有相关论文。"

    # 表格列标题
    headers = ['状态', '英文标题', '中文标题', '作者', 'PDF链接', '代码/贡献']

    # 按照CATEGORY_DISPLAY_ORDER的顺序处理类别
    for category in CATEGORY_DISPLAY_ORDER:
        if category not in active_categories:
            continue
        # 只输出一次主类别标题
        markdown += f"\n## {category}\n\n"
        papers_by_subcategory = defaultdict(list)
        for paper in active_categories[category]:
            subcategory = paper.get('subcategory', '')
            if subcategory and subcategory != "未指定":
                papers_by_subcategory[subcategory].append(paper)
            elif category == "其他 (Others)":
                papers_by_subcategory["未分类"].append(paper)
        if not papers_by_subcategory and category != "其他 (Others)":
            continue
        for subcategory, papers in papers_by_subcategory.items():
            markdown += f"\n### {subcategory}\n\n"
            markdown += "|" + "|".join(headers) + "|\n"
            markdown += "|" + "|".join(["---"] * len(headers)) + "|\n"
            for paper in papers:
                status = "📝 更新" if paper['is_updated'] else "🆕 发布"
                contrib_list = summarize_contribution(paper.get("核心贡献", ""), max_items=2)
                github_url = paper.get('github_url')
                if github_url:
                    code_and_contribution = f"[代码]({github_url})"
                    if contrib_list:
                        code_and_contribution += "; " + "; ".join(contrib_list)
                elif contrib_list:
                    code_and_contribution = "; ".join(contrib_list)
                else:
                    code_and_contribution = '无'
                values = [
                    status,
                    paper['title'],
                    paper.get('title_zh', ''),
                    paper['authors'],
                    f"[PDF]({paper['pdf_url']})",
                    code_and_contribution,
                ]
                values = [str(v).replace('\n', ' ').replace('|', '&#124;') for v in values]
                markdown += "|" + "|".join(values) + "|\n"
            markdown += "\n"
    return markdown


def df_to_markdown_detailed(papers_by_category: dict, target_date) -> str:
    """生成详细格式的Markdown内容，支持两级类别标题"""
    markdown = ""

    # 过滤掉没有论文的类别
    active_categories = {k: v for k, v in papers_by_category.items() if v}

    if not active_categories:
        return "今天没有相关论文。"

    # 按照CATEGORY_DISPLAY_ORDER的顺序处理类别
    for category in CATEGORY_DISPLAY_ORDER:
        if category not in active_categories:
            continue

        # 添加一级类别标题
        markdown += f"\n## {category}\n\n"

        # 按子类别组织论文
        papers_by_subcategory = defaultdict(list)

        # 将所有论文分配到子类别
        for paper in active_categories[category]:
            subcategory = paper.get('subcategory', '')
            if subcategory and subcategory != "未指定":
                papers_by_subcategory[subcategory].append(paper)
            elif category == "其他 (Others)":
                # 对于"其他"类别，没有子类别的论文直接显示在主类别下
                papers_by_subcategory["未分类"].append(paper)

        # 如果当前类别下没有带子类别的论文，跳过
        if not papers_by_subcategory and category != "其他 (Others)":
            continue

        # 处理每个子类别
        for subcategory, papers in papers_by_subcategory.items():
            # 添加二级类别标题
            markdown += f"\n### {subcategory}\n\n"

            # 添加论文详细信息
            for idx, paper in enumerate(papers, 1):
                # 引用编号
                markdown += f'**index:** {idx}<br />\n'
                # 日期
                markdown += f'**Date:** {target_date.strftime("%Y-%m-%d")}<br />\n'
                # 英文标题
                markdown += f'**Title:** {paper["title"]}<br />\n'
                # 中文标题
                markdown += f'**Title_cn:** {paper.get("title_zh", "")}<br />\n'
                # 作者（已经是格式化好的字符串）
                markdown += f'**Authors:** {paper["authors"]}<br />\n'
                # PDF链接
                markdown += f'**PDF:** [PDF]({paper["pdf_url"]})<br />\n'

                # 合并代码链接和精简后的核心贡献
                markdown += '**Code/Contribution:**\n'

                # 精简核心贡献内容（最多保留三条，不截断）
                contrib_list = summarize_contribution(paper.get("核心贡献", ""), max_items=3, max_len=None)

                if contrib_list:
                    markdown += f'{", ".join(contrib_list)}\n'

                # 处理代码链接
                if paper.get('github_url'):
                    markdown += f'[代码]({paper["github_url"]})\n'

                # 添加空行
                markdown += '\n'

    return markdown


def save_papers_to_markdown(papers_by_category: dict, target_date):
    """保存论文信息到Markdown文件"""
    # 使用目标日期作为文件名
    filename = target_date.strftime("%Y-%m-%d") + ".md"
    year_month = target_date.strftime("%Y-%m")

    # 获取当前文件所在目录(scripts)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 输出目录来自 config.py（相对于 scripts/ 目录）
    data_base = os.path.normpath(os.path.join(current_dir, DATA_DIR))
    local_base = os.path.normpath(os.path.join(current_dir, LOCAL_DIR))

    # 创建年月子目录
    data_year_month = os.path.join(data_base, year_month)
    local_year_month = os.path.join(local_base, year_month)

    # 创建所需的目录结构
    os.makedirs(data_year_month, exist_ok=True)
    if ENABLE_DETAILED_OUTPUT:
        os.makedirs(local_year_month, exist_ok=True)

    # 生成完整的文件路径
    table_filepath = os.path.join(data_year_month, filename)
    detailed_filepath = os.path.join(local_year_month, filename)

    # 生成标题
    title = f"## [UPDATED!] **{target_date.strftime('%Y-%m-%d')}** (Update Time)\n\n"

    # 保存表格格式的markdown文件到data/年-月目录
    with open(table_filepath, 'w', encoding='utf-8') as f:
        f.write(title)
        f.write(df_to_markdown_table(papers_by_category))

    # 保存详细格式的markdown文件到local/年-月目录（受 ENABLE_DETAILED_OUTPUT 控制）
    if ENABLE_DETAILED_OUTPUT:
        with open(detailed_filepath, 'w', encoding='utf-8') as f:
            f.write(title)
            f.write(df_to_markdown_detailed(papers_by_category, target_date))

    print(f"\n表格格式文件已保存到: {table_filepath}")
    if ENABLE_DETAILED_OUTPUT:
        print(f"详细格式文件已保存到: {detailed_filepath}")
