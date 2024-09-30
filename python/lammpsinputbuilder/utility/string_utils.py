COMMENT_LINE_FIXED_LENGTH = 80
COMMENT_LINE_START = "#### "

def write_fixed_length_comment(text: str) -> str:
    return f"{COMMENT_LINE_START}{text} ".ljust(COMMENT_LINE_FIXED_LENGTH, "#") + "\n"
