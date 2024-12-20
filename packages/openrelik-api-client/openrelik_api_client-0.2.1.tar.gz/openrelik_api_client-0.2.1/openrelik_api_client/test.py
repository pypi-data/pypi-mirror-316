from folders import FoldersAPI


def main():
    c = FoldersAPI("http://172.19.0.6:8710", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmZThmMjkyYWViZDM0MjA3YjkyODYxOGQ5MmRmZThkMSIsImlhdCI6MTczNDQ0NzcyOSwibmJmIjoxNzM0NDQ3NzI5LCJleHAiOjE3MzUwNTI1MjksImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODcxMCIsImF1ZCI6ImFwaS1jbGllbnQiLCJqdGkiOiI2ZWZhNzBiYWU0ZDE0MjJlOGM4ODY5OGY1NDhmOTBjYiIsInRva2VuX3R5cGUiOiJyZWZyZXNoIn0.MJA48D570agD49oE4HXfTWCQRpyh5JCy7YCIsHN5YJs")
    # r = c.create_root_folder("myfolder")
    # r = c.create_subfolder(33, 'myfolder_sub')
    print(c.folder_exists(1))


main()
