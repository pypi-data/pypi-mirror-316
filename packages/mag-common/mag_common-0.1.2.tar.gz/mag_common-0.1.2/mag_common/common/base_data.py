from typing import Optional, List, Dict

from mag_tools.bean.common.data_format import DataFormat
from mag_tools.bean.common.text_format import TextFormat
from mag_tools.model.common.justify_type import JustifyType
from mag_tools.utils.common.string_format import StringFormat


class BaseData:
    _text_format: TextFormat
    _data_formats: Dict[str, DataFormat]

    def __init__(self):
        """
        初始化 BaseData 类，设置默认的文本格式和数据格式
        """
        self._text_format = TextFormat(number_per_line=4, justify_type=JustifyType.LEFT, at_header='',
                                       decimal_places=4,
                                       decimal_places_of_zero=1)
        self._data_formats = {}

    def set_pad_lengths(self, pad_lengths: dict[str, int]):
        """
        设置每个参数的填充长度
        :param pad_lengths: 参数名和填充长度的字典
        """
        for arg_name, value in pad_lengths.items():
            data_format = self.get_data_format(arg_name)
            data_format.pad_length = value

    def set_same_pad_length(self, pad_length: int):
        """
        设置所有参数相同的填充长度
        :param pad_length: 填充长度
        """
        for data_format in self.__get_data_formats().values():
            data_format.pad_length = pad_length

    def set_justify_type(self, justify_type: JustifyType):
        """
        设置对齐类型
        :param justify_type: 对齐类型
        """
        self._text_format.justify_type = justify_type
        for data_format in self.__get_data_formats().values():
            data_format.justify_type = justify_type

    def set_decimal_places(self, decimal_places: int):
        """
        设置小数位数
        :param decimal_places: 小数位数
        """
        self._text_format.decimal_places = decimal_places
        for data_format in self.__get_data_formats().values():
            data_format.decimal_places = decimal_places

    def set_decimal_places_of_zero(self, decimal_places_of_zero: int):
        """
        设置零值的小数位数
        :param decimal_places_of_zero: 零值的小数位数
        """
        self._text_format.decimal_places_of_zero = decimal_places_of_zero
        for data_format in self.__get_data_formats().values():
            data_format.decimal_places_of_zero = decimal_places_of_zero

    def set_number_per_line(self, number_per_line: int):
        """
        设置每行的数字数量
        :param number_per_line: 每行的数字数量
        """
        self._text_format.number_per_line = number_per_line

    def set_at_header(self, at_header: str):
        """
        设置头部字符串
        :param at_header: 头部字符串
        """
        self._text_format.at_header = at_header

    def set_scientific(self, scientific: bool):
        """
        设置是否使用科学计数法
        :param scientific: 是否使用科学计数法
        """
        self._text_format.scientific = scientific

    def get_text(self, arg_names: List[str], delimiter: Optional[str] = None) -> str:
        """
        根据参数名数组拼成一个字符串。
        :param arg_names: 类成员变量的名字数组
        :param delimiter: 分隔符
        :return: 拼接后的字符串
        """
        if delimiter is None:
            delimiter = ''

        strings = []
        need_space = False
        for arg_name in arg_names:
            data_format = self.get_data_format(arg_name)
            value_str = str(vars(self).get(arg_name))
            pad_length = max(len(value_str), data_format.pad_length)
            need_space = need_space or pad_length == len(value_str)

            strings.append(StringFormat.pad_value(value_str, pad_length, data_format.justify_type))

        text = (' ' if need_space else '').join(strings)
        if delimiter:
            text = text.rstrip(delimiter)  # 删除末尾的分隔符
        return text

    def get_data_format(self, arg_name: str) -> DataFormat:
        """
        获取参数的数据格式
        :param arg_name: 参数名
        :return: 数据格式
        """
        return self.__get_data_formats()[arg_name]

    def __get_data_formats(self) -> Dict[str, DataFormat]:
        for name, value in vars(self).items():
            if name not in ['_text_format', '_data_formats']:
                if self._data_formats.get(name) is None:
                    self._data_formats[name] = self._text_format.get_data_format_by_value(value)

        return self._data_formats

class TestData(BaseData):
    def __init__(self, name: Optional[str] = None, age: Optional[int] = None, height: Optional[float] = None):
        """
        初始化 TestData 类，继承自 BaseData
        :param name: 名字
        :param age: 年龄
        :param height: 身高
        """
        super().__init__()

        self.name = name
        self.age = age
        self.height = height


if __name__ == '__main__':
    data = TestData('xlcao', 12, 1)
    print(data.get_text(['name', 'age', 'height'], ','))

    data.set_pad_lengths({'name': 20, 'age': 8, 'height': 10})
    print(data.get_text(['name', 'age', 'height'], ','))

    data.set_justify_type(JustifyType.LEFT)
    print(data.get_text(['name', 'age', 'height'], ','))

    data.set_justify_type(JustifyType.CENTER)
    print(data.get_text(['name', 'age', 'height'], ','))
