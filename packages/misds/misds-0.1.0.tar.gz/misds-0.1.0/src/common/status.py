from starlette import status

# 400 ~ 499 客户端请求错误
not_found = status.HTTP_404_NOT_FOUND

data_exist = status.HTTP_400_BAD_REQUEST

ifnvalid_file = status.HTTP_400_BAD_REQUEST

ifnvalid_data = status.HTTP_400_BAD_REQUEST

# 500 ~ 599 服务端错误
server_err = status.HTTP_500_INTERNAL_SERVER_ERROR
