import itertools, collections
import numpy as np

def counteree(data):
    """
    description
    -----------
    collections.Counter计算纯数字的pd.Series时，会出现np.nan无法合并统计。
    """
    data_list = []
    for i in data:
        if isinstance(i, float) and np.isnan(i):  # np.isnan只能判断数值，且对于np.array会广播，所以要限制类型。
            data_list.append(np.nan)
        else:
            data_list.append(i)
    return collections.Counter(data_list)

def chainee(datas):
    """
    description
    -----------
    原始chain只能处理iterable对象，这里可以自动将非iterable对象放入列表，然后进行chain。
    """
    dt = [x if isinstance(x, collections.Iterable) else [x] for x in datas]
    rst = itertools.chain(*dt)
    return rst

class idict(dict):
    """
    反转时行为
    ----------
    要求 value 可 hash。否则请用 invert_unhashable。
    value 重复时合并，取最后出现的 key。np.nan 重复也会合并。
    输出类型仍是 idict。
    
    固化顺序
    --------
    输出为嵌套元组
    
    example
    -------
    vd = idict(name='Allen', age=np.nan, gender='male', gende=np.nan) 
    vd.invert
    vd.invert_unhashable
    vd.preserve
    vd.invert.preserve
    vd.invert_unhashable.preserve
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    @property
    def invert(self):
        return self.__class__({v: k for k, v in self.items()})
    @property
    def invert_unhashable(self):
        return self.__class__({str(v): k for k, v in self.items()})
    @property
    def preserve(self):
        return tuple(self.items())
