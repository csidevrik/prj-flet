import os
def replace_extension (filepath, new_extension):
    # Split the file path into its base and current extension
    base = os.path.splitext(file_path)[0]
    # Combine the base with the new extension
    new_file_path = f"{base}.{new_extension}"
    # Rename the file
    os.rename(file_path, new_file_path)
    return new_file_path


# # Example usage:
# old_file = 'example.txt'
# new_extension = 'md'
# new_file = replace_extension(old_file, new_extension)
# print(f"File renamed to: {new_file}")