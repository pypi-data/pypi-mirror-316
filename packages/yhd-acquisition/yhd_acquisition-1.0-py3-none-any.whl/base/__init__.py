from pydantic import BaseModel

from typing import Generic, TypeVar, Optional

# 定义一个泛型类型变量
T = TypeVar('T')


# 定义一个 BaseModel
class BusinessResponse(BaseModel, Generic[T]):
    rt_code: int = 500000,
    rt_msg: str = '失败',
    data: Optional[T] = None

    @staticmethod
    def __getInstance(rt_code: int, rt_msg: str, data: T) -> 'BusinessResponse':
        return BusinessResponse(rt_code=rt_code, rt_msg=rt_msg, data=data)

    @staticmethod
    def ok(data: T) -> 'BusinessResponse':
        return BusinessResponse.__getInstance(0, 'success', data)

    @staticmethod
    def fail(rt_msg: str, data: T) -> 'BusinessResponse':
        return BusinessResponse.__getInstance(500000, 'success', data)

    @staticmethod
    def fail(data: T) -> 'BusinessResponse':
        return BusinessResponse.fail('fail', data)
