def format_timestamp(seconds: float) -> str:
    """
    Converts seconds into mm:ss format
    Example:
    65.4 → 01:05
    """

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    return f"{minutes:02}:{remaining_seconds:02}"