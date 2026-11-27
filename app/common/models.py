# SqlAlchemy的数据库表映射类都需要继承共同的基类：Base，不仅仅是Product业务需要，以后的其它业务模型都需要，所以属于公共父类
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, func

class Base(DeclarativeBase):
    """
    通用的repr函数，用于控制台输出对象信息
    """
    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        attrs = {}
        for key, val in vars(self).items():
            if key.startswith("_"):
                continue
            if isinstance(val, datetime):
                attrs[key] = val.strftime("%Y-%m-%d %H:%M:%S")
            else:
                attrs[key] = val
        return f"<{cls_name}({attrs})>"


# 通用的时间戳【混入类】，这样其它数据模型不用重复定义时间相关字段
class CreateAtMixin:
    # func.now() 会让数据库在插入时自动生成服务器时间（如 PostgreSQL 的 NOW()）
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class UpdateAtMixin:
    # onupdate=func.now() 会在每次数据行被 UPDATE 时，由 SQLAlchemy 自动更新该字段
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )