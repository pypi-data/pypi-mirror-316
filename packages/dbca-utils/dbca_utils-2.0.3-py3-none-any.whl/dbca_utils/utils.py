import ast
import os


def env(key, default=None, required=False, value_type=None):
    """
    Retrieves environment variables and returns Python natives. The (optional)
    default will be returned if the environment variable does not exist.
    """
    try:
        value = os.environ[key]
        value = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        pass
    except KeyError:
        if default is not None or not required:
            return default
        raise Exception(f"Missing required environment variable {key}")

    if value_type is None:
        if default is not None:
            value_type = default.__class__

    if value_type is None:
        return value
    elif isinstance(value, value_type):
        return value
    elif issubclass(value_type, list):
        if isinstance(value, tuple):
            return list(value)
        else:
            value = str(value).strip()
            if not value:
                return []
            else:
                return [s.strip() for s in value.split(",") if s.strip()]
    elif issubclass(value_type, tuple):
        if isinstance(value, list):
            return tuple(value)
        else:
            value = str(value).strip()
            if not value:
                return tuple()
            else:
                return tuple([s.strip() for s in value.split(",") if s.strip()])
    elif issubclass(value_type, bool):
        value = str(value).strip()
        if not value:
            return False
        elif value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            raise Exception(
                f"{key} is a boolean environment variable and only accepts 'true' ,'false' and '' (case-insensitive), but the configured value is '{value}'"
            )
    elif issubclass(value_type, int):
        return int(value)
    elif issubclass(value_type, float):
        return float(value)
    else:
        raise Exception(
            f"{key} is a {value_type} environment variable, but {value_type} is not supported now"
        )
