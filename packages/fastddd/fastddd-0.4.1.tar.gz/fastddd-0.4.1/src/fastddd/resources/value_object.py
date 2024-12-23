from pydantic import BaseModel, RootModel, ValidationError
from typing import TypeVar

from ..errors.app import ValidationException, RootModelValidationException

T = TypeVar("T")


def value_object(validation_exception=None, object_name: str | None = None):
    """[DDDのValueObjectに付与するデコレータ]

    ValueObjectクラスには以下の機能を追加する
    - BaseModelもしくはRootModelを継承しているかチェック
    - new関数が定義されていない場合は、デフォルトのnew関数を定義する
    - new関数がValidationErrorをスローした場合は、ValidationExceptionをスローする

    Args:
        validation_exception (Exception): ValidationErrorをスローした場合にスローする例外クラス
    """

    # 戻り値は引数で受け取ったクラスにnew関数を付与したクラス
    def decorator(cls: T) -> T:
        # pydanticのBaseModelもしくはRootModelを継承しているかチェック
        if not issubclass(cls, (BaseModel, RootModel)):
            raise ValueError(
                "ValueObject class must inherit BaseModel or RootModel")

        # new関数が定義されていない場合は、デフォルトのnew関数を定義する
        if not hasattr(cls, "new"):
            # クラス名を取得
            class_name = cls.__name__

            # クラスのプロパティを取得
            properties = cls.__annotations__.keys()

            # クラスがRootModelを継承している場合
            if issubclass(cls, RootModel):
                # プロパティがrootの一つの場合は、decoratorの引数にobject_nameが必須である旨をエラーとして返す
                if object_name is None and len(properties) == 1 and "root" in properties:
                    raise ValueError(
                        "ValueObject class with only one property named 'root' must have object_name argument")

                # validation_exceptionが指定されていて、RootModelValidationExceptionを継承していない場合はエラーとして返す
                if validation_exception is not None and not issubclass(validation_exception, RootModelValidationException):
                    raise ValueError(
                        "ValueObject class with validation_exception argument must inherit RootModelValidationException")

            # new関数を定義
            def new(cls, *args, **kwargs):
                # プロパティの値を取得
                values = dict(zip(properties, args))
                values.update(kwargs)
                try:
                    return cls(**values)
                except ValidationError as e:
                    value_object_name = object_name if object_name is not None else class_name
                    if validation_exception is None:
                        if issubclass(cls, RootModel):
                            raise RootModelValidationException(
                                e, f"{class_name} validation error", "NOT DEFINED ERROR CODE", value_object_name)
                        else:
                            raise ValidationException(
                                e, f"{class_name} validation error", "NOT DEFINED ERROR CODE")
                    else:
                        if issubclass(cls, RootModel):
                            raise validation_exception(e, value_object_name)
                        else:
                            raise validation_exception(e)

            cls.new = classmethod(new)
        else:
            new = getattr(cls, "new")

            # 例外処理を追加
            def new_with_exception(cls, *args, **kwargs):
                try:
                    return new(*args, **kwargs)
                except ValidationError as e:
                    if validation_exception is None:
                        raise ValidationException(
                            e, f"{cls.__name__} validation error", "NOT DEFINED ERROR CODE")
                    else:
                        raise validation_exception(e)

            cls.new = classmethod(new_with_exception)

        # ValueObjectの比較演算子をオーバーライド
        def __eq__(self, other: object) -> bool:
            if not isinstance(other, cls):
                return False

            for key, value in self.__dict__.items():
                if value != other.__dict__.get(key):
                    return False

            return True

        return cls

    return decorator
