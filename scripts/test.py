from os import path


fn=__file__
print(fn)
print(path.abspath(fn))
print(path.dirname(path.abspath(fn)))
print(path.abspath(path.join(path.dirname(path.abspath(fn)), '..', 'projects')))
