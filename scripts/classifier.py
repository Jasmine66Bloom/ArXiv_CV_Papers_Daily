"""论文分类器：基于关键词匹配与优先级规则的层次化分类"""
import math
import re
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

from categories_config import CATEGORY_THRESHOLDS
from config import ENABLE_LLM_ARBITRATION
from text_utils import preprocess_text, NLTK_AVAILABLE, _nltk_ngrams
from llm_helper import LLMHelper


def get_category_by_keywords(title: str, abstract: str, categories_config: Dict) -> List[Tuple[str, float, Optional[Tuple[str, float]], Optional[Dict]]]:
    """
    执行基于关键词匹配和优先级规则的层次化论文分类，带有增强的文本处理和置信度评分。

    Args:
        title (str): 论文标题，用于主要上下文分析
        abstract (str): 论文摘要，用于全面内容分析
        categories_config (Dict): 包含类别定义、关键词、权重和优先级的配置字典

    Returns:
        List[Tuple[str, float, Optional[Tuple[str, float]], Optional[Dict]]]: 按置信度降序排序的
        (类别, 置信度分数, 子类别信息, 分类解释) 元组列表
    """
    # 文本预处理
    title_lower = title.lower()
    abstract_lower = abstract.lower()

    # 使用高级文本预处理
    processed_title = preprocess_text(title)
    processed_abstract = preprocess_text(abstract)
    processed_combined = processed_title + " " + processed_abstract

    # 移除常见的停用词，提高匹配质量
    stop_words = {'a', 'an', 'the', 'in', 'on', 'at', 'for', 'to', 'of', 'and', 'or', 'with', 'by',
                  'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
                  'does', 'did', 'but', 'if', 'then', 'else', 'when', 'up', 'down', 'this', 'that'}

    # 分词并过滤停用词
    title_words = set(w for w in title_lower.split() if w not in stop_words)
    abstract_words = set(w for w in abstract_lower.split() if w not in stop_words)

    # 组合文本用于匹配
    combined_text = title_lower + " " + abstract_lower

    # 初始化得分累加器和匹配记录
    scores = defaultdict(float)
    match_details = defaultdict(list)

    # 计算每个类别的得分
    for category, config in categories_config.items():
        score = 0.0
        matches = []

        # 1. 正向关键词匹配
        for keyword, weight in config["keywords"]:
            keyword_lower = keyword.lower()
            keyword_words = set(w for w in keyword_lower.split() if w not in stop_words)

            # 对关键词也进行预处理
            processed_keyword = preprocess_text(keyword)

            # 完整短语精确匹配（最高权重）
            if keyword_lower in title_lower:
                match_score = weight * 0.25  # 标题中的精确匹配权重最高
                score += match_score
                matches.append(f"标题精确匹配 [{keyword}]: +{match_score:.2f}")
            elif keyword_lower in abstract_lower:
                match_score = weight * 0.15  # 摘要中的精确匹配权重次之
                score += match_score
                matches.append(f"摘要精确匹配 [{keyword}]: +{match_score:.2f}")

            # 使用预处理后的文本进行匹配（提高准确性）
            elif processed_keyword in processed_title:
                match_score = weight * 0.22  # 预处理标题中的匹配权重高
                score += match_score
                matches.append(f"标题语义匹配 [{keyword}]: +{match_score:.2f}")
            elif processed_keyword in processed_abstract:
                match_score = weight * 0.14  # 预处理摘要中的匹配权重中等
                score += match_score
                matches.append(f"摘要语义匹配 [{keyword}]: +{match_score:.2f}")

            # 标题中的关键词组合匹配（高权重）
            elif len(keyword_words) > 1 and keyword_words.issubset(title_words):
                match_score = weight * 0.18  # 标题中的词组匹配权重高
                score += match_score
                matches.append(f"标题词组匹配 [{keyword}]: +{match_score:.2f}")

            # 摘要中的关键词组合匹配（中等权重）
            elif len(keyword_words) > 1 and keyword_words.issubset(abstract_words):
                match_score = weight * 0.12  # 摘要中的词组匹配权重中等
                score += match_score
                matches.append(f"摘要词组匹配 [{keyword}]: +{match_score:.2f}")

            # 单词匹配（低权重）
            else:
                # 将关键词拆分为单词进行匹配
                word_matches = 0
                title_match_bonus = 0

                # 分别处理原始文本和预处理文本的匹配
                for word in keyword_words:
                    if len(word) <= 3:  # 忽略过短的词
                        continue

                    if word in title_words:
                        word_matches += 1
                        title_match_bonus += 1  # 标题匹配额外加分
                    elif word in abstract_words:
                        word_matches += 0.6  # 摘要匹配的权重低于标题

                # 处理预处理文本中的匹配
                processed_keyword_words = processed_keyword.split()
                for word in processed_keyword_words:
                    if len(word) <= 3:  # 忽略过短的词
                        continue

                    if word in processed_title:
                        word_matches += 0.8  # 预处理文本中的匹配权重稍低
                        title_match_bonus += 0.8
                    elif word in processed_abstract:
                        word_matches += 0.5

                # 只有当匹配到足够多的单词时才计算得分
                if word_matches > 0 and len(keyword_words) > 0:
                    # 计算匹配比例
                    match_ratio = word_matches / (len(keyword_words) + len(processed_keyword_words) / 2)
                    if match_ratio >= 0.4:  # 降低阈值以增加灵活性
                        match_score = weight * 0.08 * match_ratio  # 基础分
                        title_bonus = weight * 0.04 * (title_match_bonus / (len(keyword_words) + len(processed_keyword_words) / 2))  # 标题加分

                        total_score = match_score + title_bonus
                        score += total_score
                        matches.append(f"单词匹配 [{keyword}]: +{total_score:.2f} (匹配率: {match_ratio:.1f})")

            # 单词频率加成（对于重复出现的关键词给予额外加成）
            if len(keyword_words) == 1 and keyword_lower in combined_text:
                # 计算关键词在文本中出现的次数
                frequency = combined_text.count(keyword_lower)
                if frequency > 1:
                    # 频率加成，但有上限
                    freq_bonus = min(frequency * 0.02, 0.1) * weight
                    score += freq_bonus
                    matches.append(f"频率加成 [{keyword}] (x{frequency}): +{freq_bonus:.2f}")

        # 2. 负向关键词惩罚（更严格的惩罚机制）
        if "negative_keywords" in config:
            negative_score = 0
            for keyword_tuple in config["negative_keywords"]:
                if isinstance(keyword_tuple, tuple) and len(keyword_tuple) >= 1:
                    keyword = keyword_tuple[0].lower()
                    neg_weight = keyword_tuple[1] if len(keyword_tuple) > 1 else 1.0
                else:
                    # 兼容字符串格式
                    keyword = str(keyword_tuple).lower()
                    neg_weight = 1.0

                # 检查负向关键词是否出现在文本中
                if keyword in combined_text:
                    # 计算惩罚分数
                    penalty = neg_weight * 1.2
                    negative_score += penalty
                    matches.append(f"负向匹配 [{keyword}]: -{penalty:.2f}")

            # 使用更平滑的惩罚函数
            if negative_score > 0:
                original_score = score
                # 上下文感知的负向关键词处理
                # 检查负向关键词的上下文，判断是否存在否定词或对立词
                context_adjustment = 1.0

                # 检查否定词和对立词
                negation_words = ["not", "without", "no", "non", "instead of", "rather than", "unlike"]
                opposition_words = ["but", "however", "although", "despite", "contrary to"]

                # 如果存在否定词或对立词，减少惩罚
                for neg_word in negation_words:
                    if neg_word + " " + keyword_lower in combined_text or neg_word + "-" + keyword_lower in combined_text:
                        context_adjustment = 0.5  # 大幅减少惩罚
                        matches.append(f"检测到否定上下文: '{neg_word} {keyword_lower}', 惩罚减少")
                        break

                for opp_word in opposition_words:
                    if opp_word in combined_text and combined_text.find(opp_word) < combined_text.find(keyword_lower):
                        # 如果对立词在关键词之前，减少惩罚
                        context_adjustment = 0.7
                        matches.append(f"检测到对立上下文: '{opp_word}... {keyword_lower}', 惩罚部分减少")
                        break

                # 应用上下文调整
                negative_score *= context_adjustment

                # 使用改进的惩罚函数
                # 对于较小的负向分数使用线性惩罚，对于较大的负向分数使用指数惩罚
                if negative_score < 0.5:
                    # 轻微负向分数使用线性惩罚
                    penalty_factor = 1 - negative_score * 0.3
                else:
                    # 较大负向分数使用指数惩罚
                    penalty_factor = math.exp(-negative_score * 0.8)

                score *= penalty_factor
                penalty = original_score - score
                matches.append(f"负向惩罚总计: -{penalty:.2f} (因子: {penalty_factor:.2f}, 上下文调整: {context_adjustment:.1f})")

        # 3. 应用类别优先级缩放
        priority = config.get("priority", 0)
        if priority > 0:
            priority_bonus = score * (priority * 0.12)  # 优先级加成更明显
            score += priority_bonus
            matches.append(f"优先级加成 (级别 {priority}): +{priority_bonus:.2f}")

        # 记录得分和匹配详情
        if score > 0:
            scores[category] = score
            match_details[category] = matches

    # 4. 分类决策逻辑
    # 验证最低置信度阈值
    max_score = max(scores.values()) if scores else 0
    if max_score < 0.05:  # 进一步降低最低置信度要求，从0.08降低到0.05
        return []

    # 处理高优先级类别（包含所有主要类别）
    high_priority_categories = [
        "视觉表征与基础模型 (Visual Representation & Foundation Models)",
        "生成式视觉模型 (Generative Visual Modeling)",
        "视觉-语言协同理解 (Vision-Language Joint Understanding)",
        "视觉识别与理解 (Visual Recognition & Understanding)",
        "领域特定视觉应用 (Domain-specific Visual Applications)",
        "三维视觉与几何推理 (3D Vision & Geometric Reasoning)",
        "时序视觉分析 (Temporal Visual Analysis)",
        "自监督与表征学习 (Self-supervised & Representation Learning)",
        "计算效率与模型优化 (Computational Efficiency & Model Optimization)",
        "鲁棒性与可靠性 (Robustness & Reliability)",
        "低资源与高效学习 (Low-resource & Efficient Learning)",
        "具身智能与交互视觉 (Embodied Intelligence & Interactive Vision)",
        "新兴理论与跨学科方向 (Emerging Theory & Interdisciplinary Directions)"
    ]

    # 检查是否有应用类别的特征
    application_category = "领域特定视觉应用 (Domain-specific Visual Applications)"
    application_score = 0
    application_subcategory = None

    # 如果应用类别有足够的得分，则认为有应用特征 - 调整阈值为0.35，平衡准确性和覆盖率
    if application_category in scores and scores[application_category] >= 0.35:
        application_score = scores[application_category]
        # 尝试获取应用类别的子类别
        application_subcategory = get_subcategory(title, abstract, application_category, application_score)

        # 创建分类解释
        explanation = {
            "reason": "该论文具有明显的应用特征",
            "score": round(application_score, 4),
            "threshold": 0.35,
            "key_matches": match_details.get(application_category, [])[:5],
            "decision_method": "应用类别强制判断"
        }

        # 如果有应用特征，直接返回应用类别及解释
        return [(application_category, application_score, application_subcategory, explanation)]

    # 首先尝试使用高优先级类别（大幅降低阈值）
    result_with_subcategories = []

    for category in high_priority_categories:
        if category in scores and category in CATEGORY_THRESHOLDS:
            category_score = scores[category]
            threshold = CATEGORY_THRESHOLDS[category]["threshold"]
            # 动态阈值调整：根据文本长度和复杂度调整阈值
            # 计算文本复杂度因子
            text_length = len(title) + len(abstract)
            complexity_factor = 1.0

            # 较短文本需要更高的阈值（因为关键词密度更高）
            if text_length < 500:
                complexity_factor = 1.2
            elif text_length > 2000:
                complexity_factor = 0.9  # 较长文本需要更宽松的阈值

            # 计算关键词密度（匹配的关键词数量除以文本长度）
            keyword_density = len(match_details.get(category, [])) / (text_length / 100) if text_length > 0 else 0
            density_factor = 1.0

            if keyword_density > 1.5:  # 关键词密度高
                density_factor = 0.9  # 降低阈值要求
            elif keyword_density < 0.5:  # 关键词密度低
                density_factor = 1.1  # 提高阈值要求

            # 计算动态阈值系数
            dynamic_threshold_factor = 0.35 * complexity_factor * density_factor

            # 应用动态阈值
            if category_score >= threshold * dynamic_threshold_factor and category_score >= 0.10:
                # 尝试获取子类别
                subcategory = get_subcategory(title, abstract, category, category_score)
                # 优先返回有子类别的结果
                if subcategory:
                    return [(category, category_score, subcategory)]
                # 如果没有子类别，先保存结果，继续寻找其他可能有子类别的类别
                result_with_subcategories.append((category, category_score, None))

    # 收集候选类别
    candidate_categories = []

    # 将高优先级类别的结果添加到候选类别中
    if result_with_subcategories:
        candidate_categories.extend(result_with_subcategories)

    # 处理所有类别，收集候选类别
    for category, score in scores.items():
        # 跳过应用类别，因为它已经在前面处理过了
        if category == application_category:
            continue

        if category in CATEGORY_THRESHOLDS:
            threshold = CATEGORY_THRESHOLDS[category]["threshold"]
            # 使用更宽松的阈值收集候选类别
            if score >= threshold * 0.3:
                # 尝试获取子类别
                subcategory = get_subcategory(title, abstract, category, score)
                candidate_categories.append((category, score, subcategory))
        else:
            # 对于没有定义阈值的类别，使用更宽松的相对阈值
            if score >= max_score * 0.2:
                # 尝试获取子类别
                subcategory = get_subcategory(title, abstract, category, score)
                candidate_categories.append((category, score, subcategory))

    # 如果有候选类别，使用LLM做出最终决策
    if candidate_categories:
        # 按得分降序排序候选类别
        sorted_candidates = sorted(candidate_categories, key=lambda x: x[1], reverse=True)

        # 如果只有一个候选类别，直接返回
        if len(sorted_candidates) == 1:
            return [sorted_candidates[0]]

        # 关闭LLM仲裁时直接取得分最高的类别
        if not ENABLE_LLM_ARBITRATION:
            return [sorted_candidates[0]]

        # 仅当前两名得分接近时才调用LLM仲裁，节省API调用
        top_score = sorted_candidates[0][1]
        second_score = sorted_candidates[1][1]
        if top_score > 0 and (top_score - second_score) / top_score >= 0.3:
            return [sorted_candidates[0]]

        # 前两名得分接近，使用LLM做出决策
        try:
            llm_helper = LLMHelper()

            # 使用LLM决策最终类别
            final_category = llm_helper.decide_category(title, abstract, sorted_candidates)

            # 找到对应的候选类别元组
            for candidate in sorted_candidates:
                if candidate[0] == final_category:
                    return [candidate]

            # 如果找不到对应的候选类别，返回得分最高的
            return [sorted_candidates[0]]
        except Exception as e:
            print(f"LLM决策分类出错: {str(e)}")
            # 如果出错，返回得分最高的候选类别
            return [sorted_candidates[0]]

    # 如果没有候选类别，使用最简单的回退机制
    if scores:
        # 按得分降序排序所有类别
        all_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_category, top_score = all_categories[0]

        # 如果最高得分超过一个最低阈值
        if top_score >= 0.15:
            # 尝试获取子类别
            subcategory = get_subcategory(title, abstract, top_category, top_score)

            # 创建分类解释
            explanation = {
                "reason": "没有匹配到显著类别，使用得分最高的类别",
                "score": round(top_score, 4),
                "threshold": 0.15,
                "key_matches": match_details.get(top_category, [])[:5],
                "decision_method": "回退分类机制"
            }

            return [(top_category, top_score, subcategory, explanation)]

    # 如果所有尝试都失败，返回空列表
    return []


def get_subcategory(title: str, abstract: str, main_category: str, main_score: float) -> Optional[Tuple[str, float]]:
    """
    在确定主类别后，进一步确定子类别

    Args:
        title: 论文标题
        abstract: 论文摘要
        main_category: 主类别
        main_score: 主类别得分

    Returns:
        Optional[Tuple[str, float]]: 子类别及其得分，如果无法确定则返回None
    """
    # 增强的文本预处理
    title_lower = title.lower()
    abstract_lower = abstract.lower()
    combined_text = title_lower + " " + abstract_lower

    # 使用NLTK进行多级文本预处理
    processed_title = preprocess_text(title)
    processed_abstract = preprocess_text(abstract)
    processed_combined = processed_title + " " + processed_abstract

    # 创建N-gram版本的文本用于短语匹配
    # 这有助于捕获多词短语，即使它们的顺序或形式略有不同

    # 清理并标准化文本用于N-gram处理
    clean_title = re.sub(r'[^\w\s]', ' ', title_lower)
    clean_abstract = re.sub(r'[^\w\s]', ' ', abstract_lower)

    title_words = clean_title.split()
    abstract_words = clean_abstract.split()

    # 生成2-gram和3-gram（NLTK 不可用时降级为不生成）
    if NLTK_AVAILABLE and _nltk_ngrams is not None:
        title_bigrams = [' '.join(ng) for ng in _nltk_ngrams(title_words, 2)] if len(title_words) >= 2 else []
        abstract_bigrams = [' '.join(ng) for ng in _nltk_ngrams(abstract_words, 2)] if len(abstract_words) >= 2 else []
        title_trigrams = [' '.join(ng) for ng in _nltk_ngrams(title_words, 3)] if len(title_words) >= 3 else []
        abstract_trigrams = [' '.join(ng) for ng in _nltk_ngrams(abstract_words, 3)] if len(abstract_words) >= 3 else []
    else:
        title_bigrams = []
        abstract_bigrams = []
        title_trigrams = []
        abstract_trigrams = []

    # 合并所有N-gram
    all_ngrams = set(title_bigrams + abstract_bigrams + title_trigrams + abstract_trigrams)

    # 检查主类别是否有子类别定义
    if main_category in CATEGORY_THRESHOLDS and "subcategories" in CATEGORY_THRESHOLDS[main_category]:
        subcategories = CATEGORY_THRESHOLDS[main_category]["subcategories"]

        # 计算每个子类别的得分
        subcategory_scores = {}
        for subcategory_name, subcategory_threshold in subcategories.items():
            # 提取子类别名称中的关键词
            subcategory_keywords = subcategory_name.lower().split()
            score = 0.0

            # 完整短语精确匹配（最高权重）
            if subcategory_name.lower() in combined_text:
                score += 3.5  # 大幅增加精确匹配的权重，从2.5提高到3.5
            elif subcategory_name.lower() in title_lower:
                score += 4.0  # 如果子类别名称直接出现在标题中，给予更高权重

            # 使用预处理后的文本进行匹配
            processed_subcategory = preprocess_text(subcategory_name)
            if processed_subcategory in processed_combined:
                score += 2.5  # 增加预处理文本匹配的权重，从1.8提高到2.5
            elif processed_subcategory in processed_title:
                score += 3.0  # 如果预处理后的子类别名称出现在标题中

            # 增强的关键词匹配（语义相似度和上下文感知）
            for keyword in subcategory_keywords:
                if len(keyword) > 3:  # 忽略过短的词
                    # 原始文本匹配
                    if keyword in title_lower:
                        score += 1.5  # 标题中的精确匹配
                    elif keyword in abstract_lower:
                        score += 0.8  # 摘要中的精确匹配

                    # 预处理文本匹配
                    processed_keyword = preprocess_text(keyword)
                    if processed_keyword in processed_title:
                        score += 1.2  # 预处理后的标题匹配
                    elif processed_keyword in processed_abstract:
                        score += 0.6  # 预处理后的摘要匹配

                    # N-gram匹配（捕获短语变体）
                    for ngram in all_ngrams:
                        if keyword in ngram:
                            score += 0.4  # N-gram中的关键词匹配
                            break

                    # 词根匹配（处理词形变化）
                    keyword_root = preprocess_text(keyword)
                    for word in processed_title.split():
                        if keyword_root in word and len(keyword_root) > 4:  # 确保足够长以避免误匹配
                            score += 0.3
                            break
                    for word in processed_abstract.split():
                        if keyword_root in word and len(keyword_root) > 4:
                            score += 0.2
                            break

            # 大幅降低子类别阈值，确保大多数论文能被分配到子类别
            if score > 0:
                # 子类别得分需要达到主类别得分的一定比例，但大幅降低要求
                relative_threshold = main_score * 0.15 * subcategory_threshold  # 从0.25降低到0.15
                if score >= relative_threshold or score >= 0.5:  # 添加绝对分数阈值
                    subcategory_scores[subcategory_name] = score

        # 返回得分最高的子类别
        if subcategory_scores:
            best_subcategory = max(subcategory_scores.items(), key=lambda x: x[1])
            return best_subcategory

    return None
