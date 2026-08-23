"""文本预处理工具：NLTK 初始化与文本预处理"""
import os
from datetime import datetime
from functools import lru_cache

# =============================================================================
# NLTK 初始化：优先使用项目自带的 nltk_data 目录，缺失时自动下载
# =============================================================================
try:
    import nltk
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.util import ngrams as _nltk_ngrams

    # 设置NLTK数据目录为项目scripts目录下的nltk_data
    nltk_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nltk_data')
    # 确保目录存在
    os.makedirs(nltk_data_dir, exist_ok=True)
    # 添加到NLTK数据搜索路径最前面，优先用项目目录的数据
    nltk.data.path.insert(0, nltk_data_dir)

    # 创建标志文件路径
    nltk_flag_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.nltk_data_downloaded')

    # 检查是否已经下载过NLTK数据
    if os.path.exists(nltk_flag_file):
        # 已经下载过，直接使用
        NLTK_AVAILABLE = True
    else:
        # 检查必要的NLTK数据是否已下载
        needed_data = []
        for data_name in ['punkt', 'wordnet', 'stopwords']:
            try:
                path = f"{'tokenizers/' if data_name == 'punkt' else 'corpora/'}{data_name}"
                nltk.data.find(path)
                print(f"NLTK数据 '{data_name}' 已存在于: {path}")
            except LookupError:
                needed_data.append(data_name)
                print(f"NLTK数据 '{data_name}' 不存在，需要下载")

        # 只下载缺失的数据
        if needed_data:
            print(f"正在下载缺失的NLTK数据文件到: {nltk_data_dir}")
            for data_name in needed_data:
                print(f"开始下载 '{data_name}'...")
                download_result = nltk.download(data_name, download_dir=nltk_data_dir, quiet=False)
                print(f"下载 '{data_name}' 结果: {download_result}")
            print("NLTK数据文件下载完成")

        # 特别处理punkt_tab
        try:
            nltk.data.find('tokenizers/punkt_tab')
            print("NLTK数据 'punkt_tab' 已存在")
        except LookupError:
            print("开始下载 'punkt_tab'...")
            download_result = nltk.download('punkt_tab', download_dir=nltk_data_dir, quiet=False)
            print(f"下载 'punkt_tab' 结果: {download_result}")

        # 创建标志文件表示数据已下载
        with open(nltk_flag_file, 'w') as f:
            f.write(f"NLTK data downloaded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        NLTK_AVAILABLE = True
except ImportError:
    print("NLTK库未安装，将使用基本文本处理")
    NLTK_AVAILABLE = False
    _nltk_ngrams = None


@lru_cache(maxsize=8192)
def preprocess_text(text: str) -> str:
    """
    对文本进行预处理，包括小写转换、分词、去停用词、词干提取和词形还原

    Args:
        text: 原始文本

    Returns:
        str: 预处理后的文本
    """
    import re

    # 转换为小写
    text = text.lower()

    # 基本文本处理：先去除特殊字符
    basic_processed = re.sub(r'[^\w\s]', ' ', text)

    # 如果NLTK不可用，直接返回基本处理结果
    if not NLTK_AVAILABLE:
        return basic_processed

    # 尝试使用NLTK进行高级处理
    try:
        # 分词 - 先使用基本分词作为备选
        try:
            tokens = word_tokenize(text)
        except Exception:
            # 如果高级分词失败，使用基本分词
            tokens = basic_processed.split()

        # 去除停用词
        try:
            stop_words = set(stopwords.words('english'))
            tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
        except Exception:
            # 如果停用词处理失败，使用基本停用词列表
            basic_stop_words = {'a', 'an', 'the', 'in', 'on', 'at', 'for', 'to', 'of', 'and', 'or', 'with', 'by'}
            tokens = [token for token in tokens if token not in basic_stop_words and len(token) > 2]

        # 词干提取和词形还原 - 可选功能
        try:
            stemmer = PorterStemmer()
            stemmed_tokens = [stemmer.stem(token) for token in tokens]

            lemmatizer = WordNetLemmatizer()
            lemmatized_tokens = [lemmatizer.lemmatize(token) for token in stemmed_tokens]

            # 重新组合成文本
            return " ".join(lemmatized_tokens)
        except Exception:
            # 如果词干提取或词形还原失败，只返回分词和去停用词的结果
            return " ".join(tokens)

    except Exception as e:
        print(f"NLTK处理文本时出错: {str(e)}")
        # 如果所有NLTK处理都失败，回退到基本处理
        return basic_processed
