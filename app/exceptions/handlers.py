from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

import logging

logger = logging.getLogger(__name__)
def final_error_response(msg : str ,status_code : int):

    json_error = JSONResponse(
        status_code= status_code,
        content= {
            "error" : True,
            "message" : msg,
            "code" : status_code
        } 
    )
    logger.error(f"[status_code : { status_code}] msg : {msg}")
    return json_error




def http_exception_handler(request : Request , excp : StarletteHTTPException):
    return final_error_response(excp.detail,excp.status_code)



def validation_exception_handler(request : Request , excp : RequestValidationError):

    errors = excp.errors()
    error_msg = "Invalid Input"

    if errors and isinstance(errors,list):
        error_msg = errors[0].get('msg',"Invalid Input")


    return final_error_response(error_msg,400)



def general_exception_handler(request : Request , excp : Exception):
    return final_error_response(str(excp),500)


