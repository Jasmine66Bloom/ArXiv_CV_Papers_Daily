"""
计算机视觉论文分类配置文件 (2025前瞻版)
包含一级分类和二级分类的层次结构，以及中英文对照和元数据
"""

# 类别阈值配置（越大越严格）
CATEGORY_THRESHOLDS = {
    # 1. 视觉表征与基础模型
    "视觉表征与基础模型 (Visual Representation & Foundation Models)": {
        "threshold": 1.15,
        "subcategories": {
            "大规模预训练模型 (Large-scale Pretrained Models)": 1.25,
            "视觉Transformer架构 (Vision Transformer Architectures)": 1.25,
            "多模态表征学习 (Multimodal Representation Learning)": 1.25,
        },
        "priority": 5.0
    },
    
    # 2. 视觉识别与理解
    "视觉识别与理解 (Visual Recognition & Understanding)": {
        "threshold": 1.2,
        "subcategories": {
            "目标检测与定位 (Object Detection & Localization)": 1.3,
            "图像分类与识别 (Image Classification & Recognition)": 1.3,
            "语义/实例分割 (Semantic/Instance Segmentation)": 1.3,
            "关键点定位与姿态估计 (Keypoint Detection & Pose Estimation)": 1.3,
        },
        "priority": 5.1
    },
    
    # 3. 生成式视觉模型
    "生成式视觉模型 (Generative Visual Modeling)": {
        "threshold": 1.15,
        "subcategories": {
            "扩散概率模型 (Diffusion Probabilistic Models)": 1.25,
            "时空一致性生成 (Spatiotemporal Coherent Generation)": 1.25,
            "三维内容生成 (3D Content Generation)": 1.25,
            "条件式生成与编辑 (Conditional Generation & Editing)": 1.25,
        },
        "priority": 5.0
    },
    
    # 4. 三维视觉与几何推理
    "三维视觉与几何推理 (3D Vision & Geometric Reasoning)": {
        "threshold": 1.2,
        "subcategories": {
            "神经辐射场表示 (Neural Radiance Field Representation)": 1.3,
            "多视图几何重建 (Multi-view Geometric Reconstruction)": 1.3,
            "单视图三维推理 (Single-view 3D Inference)": 1.3,
            "视觉定位与映射 (Visual Localization & Mapping)": 1.3,
        },
        "priority": 4.9
    },
    
    # 5. 时序视觉分析
    "时序视觉分析 (Temporal Visual Analysis)": {
        "threshold": 1.2,
        "subcategories": {
            "动作识别与理解 (Action Recognition & Understanding)": 1.3,
            "时序建模与预测 (Temporal Modeling & Prediction)": 1.3,
            "视频目标跟踪 (Video Object Tracking)": 1.3,
            "长时序视频理解 (Long-term Video Understanding)": 1.3,
        },
        "priority": 4.8
    },
    
    # 6. 自监督与表征学习
    "自监督与表征学习 (Self-supervised & Representation Learning)": {
        "threshold": 1.15,
        "subcategories": {
            "对比学习方法 (Contrastive Learning Methods)": 1.25,
            "掩码自编码 (Masked Autoencoding)": 1.25,
            "跨模态一致性学习 (Cross-modal Consistency Learning)": 1.25,
            "表征知识迁移 (Representation Knowledge Transfer)": 1.25,
        },
        "priority": 4.7
    },
    
    # 7. 计算效率与模型优化
    "计算效率与模型优化 (Computational Efficiency & Model Optimization)": {
        "threshold": 1.2,
        "subcategories": {
            "模型压缩与加速 (Model Compression & Acceleration)": 1.3,
            "神经架构优化 (Neural Architecture Optimization)": 1.3,
            "资源受限视觉计算 (Resource-constrained Visual Computing)": 1.3,
            "推理优化 (Inference Optimization)": 1.3,
        },
        "priority": 4.6
    },
    
    # 8. 鲁棒性与可靠性
    "鲁棒性与可靠性 (Robustness & Reliability)": {
        "threshold": 1.2,
        "subcategories": {
            "对抗鲁棒性 (Adversarial Robustness)": 1.3,
            "分布外泛化 (Out-of-distribution Generalization)": 1.3,
            "不确定性量化 (Uncertainty Quantification)": 1.3,
            "视觉安全与隐私 (Visual Security & Privacy)": 1.3,
        },
        "priority": 4.5
    },
    
    # 9. 低资源与高效学习
    "低资源与高效学习 (Low-resource & Efficient Learning)": {
        "threshold": 1.2,
        "subcategories": {
            "小样本学习 (Few-shot Learning)": 1.3,
            "零/少样本泛化 (Zero/Few-shot Generalization)": 1.3,
            "半监督与弱监督 (Semi/Weakly-supervised Learning)": 1.3,
            "主动学习策略 (Active Learning Strategies)": 1.3,
        },
        "priority": 4.3
    },
    
    # 10. 具身智能与交互视觉
    "具身智能与交互视觉 (Embodied Intelligence & Interactive Vision)": {
        "threshold": 1.2,
        "subcategories": {
            "视觉导航与路径规划 (Visual Navigation & Path Planning)": 1.3,
            "视觉操作与控制 (Visual Manipulation & Control)": 1.3,
            "交互式感知 (Interactive Perception)": 1.3,
            "目标导向视觉决策 (Goal-oriented Visual Decision Making)": 1.3,
        },
        "priority": 4.1
    },
    
    # 11. 视觉-语言协同理解
    "视觉-语言协同理解 (Vision-Language Joint Understanding)": {
        "threshold": 1.15,
        "subcategories": {
            "视觉问答与推理 (Visual Question Answering & Reasoning)": 1.25,
            "视觉内容描述 (Visual Content Description)": 1.25,
            "多模态对话系统 (Multimodal Dialogue Systems)": 1.25,
            "跨模态检索与匹配 (Cross-modal Retrieval & Matching)": 1.25,
        },
        "priority": 4.0
    },
    
    # 12. 领域特定视觉应用（提高优先级，降低阈值）
    "领域特定视觉应用 (Domain-specific Visual Applications)": {
        "threshold": 1.05,  # 大幅降低阈值，使应用类论文更容易归入此类
        "subcategories": {
            "医学影像分析 (Medical Image Analysis)": 1.2,  # 降低子类别阈值
            "智能交通视觉 (Intelligent Transportation Vision)": 1.2,
            "工业视觉检测 (Industrial Visual Inspection)": 1.2,
            "遥感与地理信息 (Remote Sensing & Geospatial Information)": 1.2,
            "创意媒体生成 (Creative Media Generation)": 1.2,
            "增强/虚拟现实 (Augmented/Virtual Reality)": 1.2,
            "生物特征识别 (Biometric Recognition)": 1.2,
        },
        "priority": 5.2  # 显著提高优先级，超过大部分其他类别
    },
    
    # 13. 新兴理论与跨学科方向
    "新兴理论与跨学科方向 (Emerging Theory & Interdisciplinary Directions)": {
        "threshold": 1.2,
        "subcategories": {
            "神经-符号视觉 (Neuro-symbolic Vision)": 1.3,
            "视觉认知计算 (Visual Cognitive Computing)": 1.3,
            "量子视觉算法 (Quantum Visual Algorithms)": 1.3,
            "可解释视觉智能 (Explainable Visual Intelligence)": 1.3,
        },
        "priority": 3.5
    },
    
    # 其他类别
    "其他 (Others)": {
        "threshold": 1.5,
        "subcategories": {},
        "priority": 1
    }
}

# 类别显示顺序配置
CATEGORY_DISPLAY_ORDER = [
    # 1. 视觉表征与基础模型
    "视觉表征与基础模型 (Visual Representation & Foundation Models)",
    
    # 2. 视觉识别与理解
    "视觉识别与理解 (Visual Recognition & Understanding)",
    
    # 3. 生成式视觉模型
    "生成式视觉模型 (Generative Visual Modeling)",
    
    # 4. 三维视觉与几何推理
    "三维视觉与几何推理 (3D Vision & Geometric Reasoning)",
    
    # 5. 时序视觉分析
    "时序视觉分析 (Temporal Visual Analysis)",
    
    # 6. 自监督与表征学习
    "自监督与表征学习 (Self-supervised & Representation Learning)",
    
    # 7. 计算效率与模型优化
    "计算效率与模型优化 (Computational Efficiency & Model Optimization)",
    
    # 8. 鲁棒性与可靠性
    "鲁棒性与可靠性 (Robustness & Reliability)",
    
    # 9. 低资源与高效学习
    "低资源与高效学习 (Low-resource & Efficient Learning)",
    
    # 10. 具身智能与交互视觉
    "具身智能与交互视觉 (Embodied Intelligence & Interactive Vision)",
    
    # 11. 视觉-语言协同理解
    "视觉-语言协同理解 (Vision-Language Joint Understanding)",
    
    # 12. 领域特定视觉应用
    "领域特定视觉应用 (Domain-specific Visual Applications)",
    
    # 13. 新兴理论与跨学科方向
    "新兴理论与跨学科方向 (Emerging Theory & Interdisciplinary Directions)",
    
    # 其他类别
    "其他 (Others)"
]

# 分类提示词
CATEGORY_PROMPT = """
请将以下计算机视觉论文分类到最合适的类别中。

2025年计算机视觉分类体系：

# 1. 视觉表征与基础模型
"视觉表征与基础模型 (Visual Representation & Foundation Models)"：大规模预训练模型、视觉Transformer架构、多模态表征学习
   定义：研究视觉表征学习的基础模型、大规模预训练和视觉Transformer等前沿技术。

# 2. 视觉识别与理解
"视觉识别与理解 (Visual Recognition & Understanding)"：目标检测与定位、图像分类与识别、语义/实例分割、关键点定位与姿态估计
   定义：研究计算机视觉的基础识别任务和技术，如目标检测、图像分类、分割和姿态估计等。

# 3. 生成式视觉模型
"生成式视觉模型 (Generative Visual Modeling)"：扩散概率模型、时空一致性生成、三维内容生成、条件式生成与编辑
   定义：研究生成高质量视觉内容的方法，包括图像、视频和3D内容的生成与编辑。

# 4. 三维视觉与几何推理
"三维视觉与几何推理 (3D Vision & Geometric Reasoning)"：神经辐射场表示、多视图几何重建、单视图三维推理、视觉定位与映射
   定义：研究三维视觉和几何推理的技术，如NeRF、多视图重建、单视图3D推理和SLAM等。

# 5. 时序视觉分析
"时序视觉分析 (Temporal Visual Analysis)"：动作识别与理解、时序建模与预测、视频目标跟踪、长时序视频理解
   定义：研究视觉时序建模的任务和技术，如动作识别、时序分析、目标跟踪和视频预测等。

# 6. 自监督与表征学习
"自监督与表征学习 (Self-supervised & Representation Learning)"：对比学习方法、掩码自编码、跨模态一致性学习、表征知识迁移
   定义：研究自监督学习和表征学习的方法，如对比学习、掩码自编码和跨模态一致性学习等。

# 7. 计算效率与模型优化
"计算效率与模型优化 (Computational Efficiency & Model Optimization)"：模型压缩与加速、神经架构优化、资源受限视觉计算、推理优化
   定义：研究模型优化和计算效率的方法，如知识蒸馏、网络剪枝、量化优化和神经架构搜索等。

# 8. 鲁棒性与可靠性
"鲁棒性与可靠性 (Robustness & Reliability)"：对抗鲁棒性、分布外泛化、不确定性量化、视觉安全与隐私
   定义：研究模型鲁棒性和可靠性的方法，包括对抗鲁棒性、分布外泛化和不确定性量化等。

# 9. 低资源与高效学习
"低资源与高效学习 (Low-resource & Efficient Learning)"：小样本学习、零/少样本泛化、半监督与弱监督、主动学习策略
   定义：研究在有限数据或计算资源条件下的高效学习方法，如小样本学习、半监督学习和主动学习等。

# 10. 具身智能与交互视觉
"具身智能与交互视觉 (Embodied Intelligence & Interactive Vision)"：视觉导航与路径规划、视觉操作与控制、交互式感知、目标导向视觉决策
   定义：研究具身智能和交互视觉的方法，如视觉导航、视觉操作和目标导向视觉决策等。

# 11. 视觉-语言协同理解
"视觉-语言协同理解 (Vision-Language Joint Understanding)"：视觉问答与推理、视觉内容描述、多模态对话系统、跨模态检索与匹配
   定义：研究视觉与语言协同理解的方法，如视觉问答、图像描述和多模态对话等。

# 12. 领域特定视觉应用
"领域特定视觉应用 (Domain-specific Visual Applications)"：医学影像分析、智能交通视觉、工业视觉检测、遥感与地理信息、创意媒体生成、增强/虚拟现实、生物特征识别
   定义：研究视觉技术在特定领域的应用，如医学影像、智能交通和工业视觉等。

# 13. 新兴理论与跨学科方向
"新兴理论与跨学科方向 (Emerging Theory & Interdisciplinary Directions)"：神经-符号视觉、视觉认知计算、量子视觉算法、可解释视觉智能
   定义：研究视觉领域的新兴理论和跨学科方向，如神经-符号视觉、视觉认知计算和可解释视觉智能等。

# 其他类别
"其他 (Others)"：不属于以上类别的论文
   定义：其他不能明确归类到上述类别的视觉研究工作。

分类指南：
1. 首先分析论文的核心技术贡献和主要研究目标
2. 考虑论文的方法、实验和应用场景
3. 如果论文涉及多个类别，请选择最核心、最具创新性的方向
4. 优先考虑技术本质而非应用领域（除非应用创新是论文的主要贡献）
5. 只有在确实无法归类到前13个类别时，才选择“其他”类别

边界案例处理：
- 如果论文同时涉及“生成式视觉模型”和“视觉-语言协同理解”，但核心是文本引导的图像生成，应归类为“生成式视觉模型”
- 如果论文研究NeRF技术，即使应用于医疗领域，也应优先归类为“三维视觉与几何推理”而非“领域特定视觉应用”
- 如果论文提出新的视觉基础模型并展示了涌现能力，应归类为“视觉表征与基础模型”而非“视觉识别与理解”

请分析论文的核心技术和主要贡献，选择最合适的一个类别。只返回类别名称，不要有任何解释或额外文本。
"""

# 类别关键词配置
CATEGORY_KEYWORDS = {
    # 1. 视觉表征与基础模型
    "视觉表征与基础模型 (Visual Representation & Foundation Models)": {
        "keywords": [
            # 大规模预训练模型（高权重）
            ("vision foundation model", 2.0),      # 视觉基础模型
            ("large-scale pretrained model", 2.0), # 大规模预训练模型
            ("foundation model", 1.8),             # 基础模型
            
            # 视觉Transformer架构（高权重）
            ("vision transformer", 2.0),           # 视觉transformer
            ("transformer architecture", 1.8),      # transformer架构
            
            # 多模态表征学习（高权重）
            ("multimodal representation", 2.0),    # 多模态表征
            ("multimodal pretraining", 2.0),      # 多模态预训练
            ("multimodal foundation model", 2.0),  # 多模态基础模型
        ],
        "negative_keywords": [
            ("specific application", 1.0),         # 特定应用
            ("downstream task", 0.8),              # 下游任务
        ]
    },
    
    # 2. 视觉识别与理解
    "视觉识别与理解 (Visual Recognition & Understanding)": {
        "keywords": [
            # 目标检测与定位（高权重）
            ("object detection", 2.0),             # 目标检测
            ("object localization", 2.0),          # 目标定位
            ("detection transformer", 1.8),        # 检测 transformer
            
            # 图像分类与识别（高权重）
            ("image classification", 2.0),         # 图像分类
            ("image recognition", 2.0),            # 图像识别
            
            # 语义/实例分割（高权重）
            ("semantic segmentation", 2.0),        # 语义分割
            ("instance segmentation", 2.0),        # 实例分割
            
            # 关键点定位与姿态估计（高权重）
            ("keypoint detection", 2.0),           # 关键点检测
            ("pose estimation", 2.0),              # 姿态估计
        ],
        "negative_keywords": [
            ("generative", 1.0),                   # 生成式
            ("3D reconstruction", 0.8),             # 3D重建
        ]
    },
    
    # 3. 生成式视觉模型
    "生成式视觉模型 (Generative Visual Modeling)": {
        "keywords": [
            # 扩散概率模型（高权重）
            ("diffusion model", 2.0),              # 扩散模型
            ("latent diffusion", 2.0),             # 潜在扩散
            ("denoising diffusion", 2.0),          # 去噪扩散
            ("score-based", 1.8),                  # 基于分数
            
            # 时空一致性生成（高权重）
            ("spatiotemporal generation", 2.0),    # 时空生成
            ("coherent generation", 2.0),          # 一致性生成
            ("video generation", 1.8),             # 视频生成
            
            # 三维内容生成（高权重）
            ("3D content generation", 2.0),        # 3D内容生成
            ("3D generative", 2.0),                # 3D生成
            
            # 条件式生成与编辑（高权重）
            ("conditional generation", 2.0),        # 条件式生成
            ("image editing", 2.0),                # 图像编辑
            ("text-to-image", 2.0),                # 文本生成图像
        ],
        "negative_keywords": [
            ("recognition", 1.0),                  # 识别
            ("classification", 1.0),               # 分类
        ]
    },
    
    # 4. 三维视觉与几何推理
    "三维视觉与几何推理 (3D Vision & Geometric Reasoning)": {
        "keywords": [
            # 神经辐射场表示（高权重）
            ("neural radiance field", 2.0),         # 神经辐射场
            ("NeRF", 2.0),                         # NeRF
            ("3D representation", 1.8),            # 3D表示
            
            # 多视图几何重建（高权重）
            ("multi-view reconstruction", 2.0),     # 多视图重建
            ("geometric reconstruction", 2.0),      # 几何重建
            ("structure from motion", 1.8),         # 运动恢复结构
            
            # 单视图三维推理（高权重）
            ("single-view 3D", 2.0),               # 单视图3D
            ("monocular 3D", 2.0),                 # 单目3D
            ("depth estimation", 1.8),             # 深度估计
            
            # 视觉定位与映射（高权重）
            ("visual localization", 2.0),          # 视觉定位
            ("SLAM", 2.0),                         # SLAM
            ("visual mapping", 1.8),               # 视觉映射
        ],
        "negative_keywords": [
            ("2D only", 1.2),                     # 仅2D（提升惩罚）
            ("image-level", 1.0),                  # 图像级别
            ("semantic segmentation", 0.8),       # 避免与2D分割混淆
            ("object detection", 0.8),              # 避免与2D检测混淆
        ]
    },
    
    # 5. 时序视觉分析
    "时序视觉分析 (Temporal Visual Analysis)": {
        "keywords": [
            # 动作识别与理解（高权重）
            ("action recognition", 2.0),             # 动作识别
            ("action understanding", 2.0),           # 动作理解
            ("human activity recognition", 1.8),     # 人类活动识别
            
            # 时序建模与预测（高权重）
            ("temporal modeling", 2.0),              # 时序建模
            ("video prediction", 2.0),               # 视频预测
            ("future prediction", 1.8),              # 未来预测
            
            # 视频目标跟踪（高权重）
            ("video object tracking", 2.0),          # 视频目标跟踪
            ("multi-object tracking", 2.0),          # 多目标跟踪
            ("visual tracking", 1.8),                # 视觉跟踪
            
            # 长时序视频理解（高权重）
            ("long-term video understanding", 2.0),   # 长时序视频理解
            ("video summarization", 2.0),            # 视频摘要
            ("video captioning", 1.8),               # 视频描述
        ],
        "negative_keywords": [
            ("static image", 1.2),                   # 静态图像（提升惩罚）
            ("single frame", 1.0),                  # 单帧
            ("semantic segmentation", 0.8),         # 避免与2D分割混淆
            ("image classification", 0.8),           # 避免与2D分类混淆
        ]
    },
    
    # 6. 自监督与表征学习
    "自监督与表征学习 (Self-supervised & Representation Learning)": {
        "keywords": [
            # 对比学习方法（高权重）
            ("contrastive learning", 2.0),         # 对比学习
            ("contrastive representation", 2.0),    # 对比表征
            ("SimCLR", 1.8),                       # SimCLR
            
            # 掩码自编码（高权重）
            ("masked autoencoding", 2.0),          # 掩码自编码
            ("MAE", 2.0),                          # MAE
            ("masked prediction", 1.8),             # 掩码预测
            
            # 跨模态一致性学习（高权重）
            ("cross-modal consistency", 2.0),       # 跨模态一致性
            ("multimodal consistency", 2.0),        # 多模态一致性
            
            # 表征知识迁移（高权重）
            ("representation transfer", 2.0),       # 表征迁移
            ("knowledge transfer", 2.0),            # 知识迁移
        ],
        "negative_keywords": [
            ("fully supervised", 1.2),              # 全监督（提升惩罚）
            ("labeled data", 1.0),                  # 标注数据
            ("classification", 0.8),                # 避免与纯分类混淆
            ("object detection", 0.8),              # 避免与检测混淆
        ]
    },
    
    # 7. 计算效率与模型优化
    "计算效率与模型优化 (Computational Efficiency & Model Optimization)": {
        "keywords": [
            # 模型压缩与加速（高权重）
            ("model compression", 2.0),             # 模型压缩
            ("model acceleration", 2.0),            # 模型加速
            ("knowledge distillation", 1.8),        # 知识蒸馏
            
            # 神经架构优化（高权重）
            ("neural architecture", 2.0),           # 神经架构
            ("architecture optimization", 2.0),      # 架构优化
            ("NAS", 1.8),                           # 神经架构搜索
            
            # 资源受限视觉计算（高权重）
            ("resource-constrained", 2.0),          # 资源受限
            ("efficient inference", 2.0),           # 高效推理
            
            # 推理优化（高权重）
            ("inference optimization", 2.0),         # 推理优化
            ("quantization", 2.0),                  # 量化
            ("pruning", 2.0),                       # 剪枝
        ],
        "negative_keywords": [
            ("accuracy only", 1.0),                 # 仅精度
            ("theoretical", 0.8),                   # 理论的
        ]
    },
    
    # 8. 鲁棒性与可靠性
    "鲁棒性与可靠性 (Robustness & Reliability)": {
        "keywords": [
            # 对抗鲁棒性（高权重）
            ("adversarial robustness", 2.0),        # 对抗鲁棒性
            ("adversarial attack", 2.0),            # 对抗攻击
            ("adversarial defense", 2.0),           # 对抗防御
            
            # 分布外泛化（高权重）
            ("out-of-distribution", 2.0),          # 分布外
            ("distribution generalization", 2.0),    # 分布泛化
            ("domain generalization", 1.8),         # 域泛化
            
            # 不确定性量化（高权重）
            ("uncertainty quantification", 2.0),     # 不确定性量化
            ("uncertainty estimation", 2.0),         # 不确定性估计
            
            # 视觉安全与隐私（高权重）
            ("visual security", 2.0),               # 视觉安全
            ("visual privacy", 2.0),                # 视觉隐私
        ],
        "negative_keywords": [
            ("accuracy only", 1.0),                 # 仅精度
            ("standard benchmark", 0.8),            # 标准基准
        ]
    },
    
    # 9. 低资源与高效学习
    "低资源与高效学习 (Low-resource & Efficient Learning)": {
        "keywords": [
            # 小样本学习（高权重）
            ("few-shot learning", 2.0),             # 小样本学习
            ("few-shot", 2.0),                      # 小样本
            
            # 零/少样本泛化（高权重）
            ("zero-shot", 2.0),                     # 零样本
            ("few-shot generalization", 2.0),        # 小样本泛化
            
            # 半监督与弱监督（高权重）
            ("semi-supervised", 2.0),               # 半监督
            ("weakly-supervised", 2.0),             # 弱监督
            
            # 主动学习策略（高权重）
            ("active learning", 2.0),               # 主动学习
            ("learning strategies", 2.0),           # 学习策略
        ],
        "negative_keywords": [
            ("large dataset", 1.0),                 # 大数据集
            ("fully supervised", 0.8),              # 全监督
        ]
    },
    
    # 10. 具身智能与交互视觉
    "具身智能与交互视觉 (Embodied Intelligence & Interactive Vision)": {
        "keywords": [
            # 视觉导航与路径规划（高权重）
            ("visual navigation", 2.0),              # 视觉导航
            ("path planning", 2.0),                  # 路径规划
            ("embodied navigation", 1.8),            # 具身导航
            
            # 视觉操作与控制（高权重）
            ("visual manipulation", 2.0),            # 视觉操作
            ("visual control", 2.0),                 # 视觉控制
            ("robotic manipulation", 1.8),           # 机器人操作
            
            # 交互式感知（高权重）
            ("interactive perception", 2.0),          # 交互式感知
            ("embodied interaction", 2.0),           # 具身交互
            
            # 目标导向视觉决策（高权重）
            ("goal-oriented vision", 2.0),           # 目标导向视觉
            ("visual decision making", 2.0),         # 视觉决策
        ],
        "negative_keywords": [
            ("passive perception", 1.0),             # 被动感知
            ("static scene", 0.8),                   # 静态场景
        ]
    },
    
    # 11. 视觉-语言协同理解
    "视觉-语言协同理解 (Vision-Language Joint Understanding)": {
        "keywords": [
            # 视觉问答与推理（高权重）
            ("visual question answering", 2.0),      # 视觉问答
            ("VQA", 2.0),                           # VQA
            ("visual reasoning", 2.0),               # 视觉推理
            
            # 视觉内容描述（高权重）
            ("image captioning", 2.0),               # 图像描述
            ("visual description", 2.0),             # 视觉描述
            ("visual content description", 1.8),      # 视觉内容描述
            
            # 多模态对话系统（高权重）
            ("multimodal dialogue", 2.0),            # 多模态对话
            ("visual dialogue", 2.0),                # 视觉对话
            ("conversational agents", 1.8),          # 对话代理
            
            # 跨模态检索与匹配（高权重）
            ("cross-modal retrieval", 2.0),          # 跨模态检索
            ("vision-language matching", 2.0),        # 视觉-语言匹配
            ("image-text matching", 1.8),             # 图像-文本匹配
        ],
        "negative_keywords": [
            ("vision-only", 1.0),                    # 仅视觉
            ("language-only", 0.8),                  # 仅语言
        ]
    },
    
    # 12. 领域特定视觉应用
    "领域特定视觉应用 (Domain-specific Visual Applications)": {
        "keywords": [
            # 医学影像分析（高权重）
            ("medical image analysis", 2.0),          # 医学影像分析
            ("medical imaging", 2.0),                 # 医学成像
            ("disease diagnosis", 1.8),               # 疾病诊断
            
            # 智能交通视觉（高权重）
            ("intelligent transportation", 2.0),      # 智能交通
            ("autonomous driving", 2.0),              # 自动驾驶
            ("traffic analysis", 1.8),                # 交通分析
            
            # 工业视觉检测（高权重）
            ("industrial inspection", 2.0),           # 工业检测
            ("defect detection", 2.0),                # 缺陷检测
            ("quality control", 1.8),                 # 质量控制
            
            # 遥感与地理信息（高权重）
            ("remote sensing", 2.0),                  # 遥感
            ("geospatial information", 2.0),          # 地理信息
            ("satellite imagery", 1.8),               # 卫星图像
        ],
        "negative_keywords": [
            ("general vision", 1.0),                  # 通用视觉
            ("foundation model", 0.8),                # 基础模型
        ]
    },
    
    # 13. 新兴理论与跨学科方向
    "新兴理论与跨学科方向 (Emerging Theory & Interdisciplinary Directions)": {
        "keywords": [
            # 神经-符号视觉（高权重）
            ("neuro-symbolic vision", 2.0),           # 神经-符号视觉
            ("symbolic reasoning", 2.0),              # 符号推理
            ("neural-symbolic", 1.8),                 # 神经-符号
            
            # 视觉认知计算（高权重）
            ("visual cognitive computing", 2.0),      # 视觉认知计算
            ("cognitive vision", 2.0),                # 认知视觉
            ("brain-inspired vision", 1.8),           # 脑启发视觉
            
            # 量子视觉算法（高权重）
            ("quantum visual algorithm", 2.0),        # 量子视觉算法
            ("quantum vision", 2.0),                  # 量子视觉
            
            # 可解释视觉智能（高权重）
            ("explainable visual intelligence", 2.0), # 可解释视觉智能
            ("explainable vision", 2.0),              # 可解释视觉
            ("interpretable vision", 1.8),            # 可解释视觉
        ],
        "negative_keywords": [
            ("traditional vision", 1.0),               # 传统视觉
            ("standard approach", 0.8),               # 标准方法
        ]
    },
    
    # 其他类别
    "其他 (Others)": {
        "keywords": [
            # 不属于上述类别的论文（低权重）
            ("miscellaneous", 1.0),                # 杂项
            ("other", 1.0),                        # 其他
            ("novel approach", 1.0),               # 新型方法
        ],
        "negative_keywords": [
            # 所有主要类别的关键词都是负面关键词
            ("foundation model", 1.0),             # 基础模型
            ("detection", 1.0),                    # 检测
            ("segmentation", 1.0),                 # 分割
            ("generative", 1.0),                   # 生成式
            ("3D", 1.0),                           # 3D
            ("temporal", 1.0),                     # 时序
            ("self-supervised", 1.0),              # 自监督
            ("efficiency", 1.0),                   # 效率
            ("robustness", 1.0),                   # 鲁棒性
            ("few-shot", 1.0),                     # 小样本
            ("embodied", 1.0),                     # 具身
            ("vision-language", 1.0),              # 视觉-语言
            ("application", 1.0),                  # 应用
            ("interdisciplinary", 1.0),            # 跨学科
        ]
    }
}