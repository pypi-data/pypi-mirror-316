from fastapi import Request

from inhand.dto.ErrorException import APIError,Error, ErrorCodeException, ERR_CODE_400, ERR_CODE_403, ERR_CODE_404,ERR_CODE_500
from inhand.utilities.StringUtil import StringUtil

class HttpUtil:
    @staticmethod
    def parsePowerISApiHeader(request: Request) -> dict:
        base64str = request.headers.get("x-nezha-extra")
        if base64str is None:
            raise APIError(error=Error(code=ERR_CODE_403,message="Not a trust client, you need call the API with a apk key to the API gateway"))
        extra_dict=StringUtil.parseXAPIExtra(base64str)
        if 'app_id' not in extra_dict.keys():
            raise APIError(error=Error(code=ERR_CODE_403,message="Not a trust client"))
        return extra_dict
