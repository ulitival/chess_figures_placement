# chess_figures_placement

## How to run
gunicorn --workers 4 --bind localhost:5050 --timeout 60 phrase_chess_task.api.flask_app:app