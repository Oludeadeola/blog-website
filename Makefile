runserver:
	python manage.py runserver 0.0.0.0:8000

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

shell:
	python manage.py shell

admin:
	python manage.py bloggycreatesuperuser

push:
	git push

add:
	git add .

index-rebuild:
	python manage.py search_index --rebuild

crlf config:
	git config core.autocrlf true

#global crlf config:
#	git config --global core.autocrlf true

commit:
	git commit -m "$(message)"

push:
	git push origin $(branch)