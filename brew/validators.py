
def validate_percentage(percent):
    if 0.0 <= percent <= 1.0:
        return percent
    else:
        raise Exception("Percentage values should be in decimal format")
