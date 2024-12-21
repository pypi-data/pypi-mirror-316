import logging
import os

import pytest

from photobooth.container import Container, container

logger = logging.getLogger(name=None)


# need fixture on module scope otherwise tests fail because GPIO lib gets messed up
@pytest.fixture(scope="module")
def _container() -> Container:
    container.start()
    yield container
    container.stop()


def test_ensure_scaled_repr_created(_container: Container):
    """this function processes single images (in contrast to collages or videos)"""

    # get the newest image id
    mediaitem = _container.mediacollection_service.db_get_most_recent_mediaitem()

    # should just run without any exceptions.
    try:
        mediaitem.ensure_scaled_repr_created()
    except Exception as exc:
        raise AssertionError(f"'ensure_scaled_repr_created' raised an exception :( {exc}") from exc


def test_ensure_scaled_repr_created_processed(_container: Container):
    """this function processes single images (in contrast to collages or videos)"""

    # get the newest image id
    mediaitem = _container.mediacollection_service.db_get_most_recent_mediaitem()

    os.remove(mediaitem.path_full)
    os.remove(mediaitem.path_preview)
    os.remove(mediaitem.path_thumbnail)
    os.remove(mediaitem.path_full_unprocessed)
    os.remove(mediaitem.path_preview_unprocessed)
    os.remove(mediaitem.path_thumbnail_unprocessed)

    # should just run without any exceptions.
    try:
        mediaitem.ensure_scaled_repr_created()
    except Exception as exc:
        raise AssertionError(f"'ensure_scaled_repr_created' raised an exception :( {exc}") from exc

    assert os.path.isfile(mediaitem.path_full)
    assert os.path.isfile(mediaitem.path_preview)
    assert os.path.isfile(mediaitem.path_thumbnail)
    assert os.path.isfile(mediaitem.path_full_unprocessed)
    assert os.path.isfile(mediaitem.path_preview_unprocessed)
    assert os.path.isfile(mediaitem.path_thumbnail_unprocessed)
