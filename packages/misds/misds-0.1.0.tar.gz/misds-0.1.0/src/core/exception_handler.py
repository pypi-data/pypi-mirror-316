from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.common.logger import logger
from src.config import settings

CUSTOM_MESSAGES = {
    'string_too_long': '{loc}长度超过规定长度：{max_length}！',
    'string_too_short': '{loc}长度低于规定长度：{min_length}！',

    'bool_type': '无效的布尔类型！',
    'bool_parsing': '无法解析为布尔类型！',

    'datetime_parsing': '无法解析为日期时间类型！',
    'datetime_type': '无效的日期时间类型！',

    'date_parsing': '无法解析为日期类型！',
    'date_type': '无效的日期类型！',

    'float_type': '无效的浮点类型！',
    'float_parsing': '无法解析为浮点类型！',

    'int_type': '{loc}无效的INT类型！',
    'int_parsing': '无法解析{loc}为INT类型！',

    'greater_than': '当前值不大于{value}！',
    'greater_than_equal': '当前值不大于等于{value}！',

    'less_than': '当前值不小于{value}！',
    'less_than_equal': '当前值不小于等于{value}！',

    'missing': "该值{loc}为必传值！",
    "missing_argument": "该值{loc}为必传值！",
    "missing_keyword_only_argument": "该值{loc}为必传值！",

    "string_type": "无效的Strng类型！",

    'time_parsing': '无效的时间类型！',
    'time_type': '无法解析为时间类型！',

    'too_long': '最大长度超出限制！',
    'too_short': '最小长度低于限制！',

    'bytes_type': '无效的字节类型！',

    'json_invalid': '请输入有效的json数据！',

}


def convert_errors(e: RequestValidationError | ValidationError) -> str:
    """
        将错误提取出来， 只获取第一个错误信息。
    """
    if len(e.errors()) > 0:
        error = e.errors()[0]
        custom_message = CUSTOM_MESSAGES.get(error['type'])
        if custom_message:
            param = error.get('loc')[1]
            ctx = error.get('ctx', None)
            error_msg = custom_message.format(loc=param, **ctx) if ctx else custom_message.format(loc=param)
        else:
            error_msg = error['msg']
    else:
        error_msg = "参数解析失败！"
    return error_msg


def register_exception(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def unicorn_exception_handler(request: Request, exc: StarletteHTTPException):
        """
        重写HTTPException异常处理器
        """
        if settings.APP_DEBUG:
            logger.error(f"请求地址: {str(request.url)}", )
            logger.error("捕捉到重写HTTPException异常异常：unicorn_exception_handler")
            logger.error(exc.detail)
        # 打印栈信息，方便追踪排查异常
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": exc.status_code,
                "msg": exc.detail,
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        重写请求验证异常处理器
        """
        if settings.APP_DEBUG:
            logger.error("请求地址", request.url.__str__())
            logger.error("捕捉到重写请求验证异常异常：validation_exception_handler")
            logger.error(exc.errors())
        # 打印栈信息，方便追踪排查异常
        logger.exception(exc)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": status.HTTP_400_BAD_REQUEST,
                "msg": convert_errors(exc),
            }
        )

    @app.exception_handler(ValueError)
    async def value_exception_handler(request: Request, exc: ValueError):
        """
        捕获值异常
        """
        if settings.APP_DEBUG:
            logger.error("请求地址", request.url.__str__())
            logger.error("捕捉到值异常：value_exception_handler")
            logger.error(exc.__str__())
        # 打印栈信息，方便追踪排查异常
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {
                    "msg": exc.__str__(),
                    "code": status.HTTP_400_BAD_REQUEST
                }
            ),
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        捕获全部异常
        """
        if settings.APP_DEBUG:
            logger.error("请求地址", request.url.__str__())
            logger.error("捕捉到全局异常：all_exception_handler")
            logger.error(exc.__str__())
        # 打印栈信息，方便追踪排查异常
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {
                    "msg": f"接口异常！{exc.__str__()}",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR
                }
            ),
        )
