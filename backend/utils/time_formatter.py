def format_timestamp(seconds: float) -> str:
    """
    Converts seconds into mm:ss format
    Example:
    65.4 → 01:05
    """

    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f"{minutes:02}:{seconds:02}"