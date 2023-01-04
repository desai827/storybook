# storybook

Run the following when you first clone the repo
```
$ pip install -r requirements.txt
$ virtualenv venv
```

Subsequent runs:
```
$ source venv/bin/activate
$ ipython
```

Run the folliwng in iPython:
```
from main import Storybook
sb = Storybook()
sb.generate_story()
html = sb.generate_storybook()

with open("test.html","w") as fp:
	fp.write(html)
```
