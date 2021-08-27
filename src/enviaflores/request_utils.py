import json
import traceback

from aws_lambda_powertools.utilities.validation import validate
from aws_lambda_powertools.utilities.validation.exceptions import SchemaValidationError

from .exceptions import NotFoundException, ForbiddenException, BadRequestException

def get_body(input_schema=None):
    print(input_schema)
    def dec_arguments(func):
        def wrapper(event, context):
            print(event)
            try:
                event["requestBody"] = json.loads(event.get("body")) if event.get("body") else {}
                if (input_schema is not None):
                    validate(event=event["requestBody"], schema=input_schema)
                return func(event, context)
            except BadRequestException as e:
                statusCode = 400
                body = str(e)
            except SchemaValidationError as e:
                statusCode = 400
                body = str(e)
            except ForbiddenException as e:
                statusCode = 403
                body = str(e)
            except NotFoundException as e:
                statusCode = 404
                body = str(e)
            except Exception as e:
                statusCode = 500
                body = repr(e)
                traceback.print_exc()
            
            return {
                "statusCode": statusCode,
                "body": body
            }
        return wrapper
    return dec_arguments
