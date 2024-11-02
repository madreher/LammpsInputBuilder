COMMENT_LINE_FIXED_LENGTH = 80
COMMENT_LINE_START = "#### "

def write_fixed_length_comment(text: str) -> str:
    """
    Write a fixed length comment to a string for a Lammps script. 
    This is a helper function to make the Lammps comments added in a 
    script to be more readable and consistent.
    Args:
        text (str): The text to write

    Returns:
        str: The fixed length comment
    """
    return f"{COMMENT_LINE_START}{text} ".ljust(COMMENT_LINE_FIXED_LENGTH, "#") + "\n"
