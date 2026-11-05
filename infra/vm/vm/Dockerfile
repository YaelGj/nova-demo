# Image des « VM » de Nova : un Python minimal qui sert le dossier /srv en HTTP sur le port 8000.
# Ansible s'y connecte par Docker (sans SSH) et remplace /srv/index.html.
FROM python:3.12-slim
COPY index.html /srv/index.html
EXPOSE 8000
# SIGINT : python s'arrête aussitôt (SIGTERM est ignoré par un processus de PID 1 sans gestionnaire).
STOPSIGNAL SIGINT
CMD ["python", "-m", "http.server", "8000", "--directory", "/srv"]
