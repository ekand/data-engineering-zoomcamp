from prefect.filesystems import GitHub

github_block = GitHub.load("my-github-block")

foo = github_block.get_directory('.')
print(type(foo))
print(foo)
