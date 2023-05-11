
file = open("Procfile", "w")
file.write("web: gunicorn main:app")
file.close()

