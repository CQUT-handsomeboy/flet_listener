import jieba

jieba.enable_paddle()

def participle_words(text: str, mode="precise"):
    """
    分词函数，返回的是一个生成器
    """
    match mode:
        case "precise":
            # 精准模式
            seg_list = jieba.cut(text, cut_all=False)
        case "paddle":
            # paddl模式
            seg_list = jieba.cut(text, use_paddle=True)
            pass
        case "full":
            # 全模式
            seg_list = jieba.cut(text, cut_all=True)
            pass
        case "search_engine":
            # 搜索引擎模式
            seg_list = jieba.cut_for_search(text)
            pass
        case "news":
            # 新闻模式
            seg_list = jieba.cut(text)
            pass

    return seg_list