media/

This directory stores user-uploaded media files (images, documents, etc.) for the Django project.

Guidance:
- In development, Django can serve media files when `DEBUG = True` if you configure `MEDIA_URL` and `MEDIA_ROOT` in `settings.py` and include the proper `urlpatterns` in `realestate_project/urls.py`.

Example settings (add to `realestate_project/settings.py`):

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

(If your `settings.py` uses os.path instead of pathlib, set `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`.)

Example URL configuration (for development; add to `realestate_project/urls.py`):

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your existing url patterns
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Notes:
- Do NOT commit large or sensitive user-uploaded files to the repository. Use cloud storage (S3, GCS) or a separate persistent storage in production.
- Add `media/` to `.gitignore` if you don't want to track uploaded files. A `.gitkeep` file is included here to ensure the empty folder is tracked until real media is added.
