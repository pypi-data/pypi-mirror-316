def get_data_type_info(data_type: str):
    if data_type in ["int", "int32", "long"]:
        return {"length": 4, "decode_symbol": "i", "python_type": int}

    if data_type in ["uint32"]:
        return {"length": 4, "decode_symbol": "I", "python_type": int}

    elif data_type in ["float"]:
        return {"length": 4, "decode_symbol": "f", "python_type": float}

    elif data_type in ["double"]:
        return {"length": 8, "decode_symbol": "d", "python_type": float}

    elif data_type in ["uint16"]:
        return {"length": 2, "decode_symbol": "H", "python_type": int}

    elif data_type in ["int16"]:
        return {"length": 2, "decode_symbol": "h", "python_type": int}

    elif data_type in ["uint8"]:
        return {"length": 1, "decode_symbol": "B", "python_type": int}

    elif data_type in ["int8"]:
        return {"length": 1, "decode_symbol": "b", "python_type": int}

    elif data_type in ["bool"]:
        return {"length": 1, "decode_symbol": "?", "python_type": bool}

    else:
        raise Exception(f"Unsupported data class provided: {data_type}")
