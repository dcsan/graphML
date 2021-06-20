# make stuff

freeze:
	pip freeze > requirements.txt

render:
	dot -Tpng DocName.dot -o DocName.png

dot-install:
	brew install graphviz

