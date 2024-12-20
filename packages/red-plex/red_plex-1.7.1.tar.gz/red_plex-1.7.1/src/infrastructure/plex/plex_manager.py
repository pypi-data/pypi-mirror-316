"""Module for managing Plex albums and playlists."""

import os
from datetime import datetime, timezone
from plexapi.server import PlexServer
from src.infrastructure.logger.logger import logger
from src.infrastructure.cache.album_cache import AlbumCache

class PlexManager:
    """Handles operations related to Plex."""

    def __init__(self, url, token, section_name, csv_file=None):
        self.url = url
        self.token = token
        self.section_name = section_name
        self.plex = PlexServer(self.url, self.token)
        self.library_section = self.plex.library.section(self.section_name)

        # Initialize the album cache
        self.album_cache = AlbumCache(csv_file)
        self.album_data = self.album_cache.load_albums()

    def populate_album_cache(self):
        """Fetches new albums from Plex and updates the cache."""
        logger.info('Updating album cache...')

        # Determine the latest addedAt date from the existing cache
        if self.album_data:
            latest_added_at = max(added_at for _, added_at in self.album_data.values())
            logger.info('Latest album added at: %s', latest_added_at)
        else:
            latest_added_at = datetime(1970, 1, 1, tzinfo=timezone.utc)
            logger.info('No existing albums in cache. Fetching all albums.')

        # Fetch albums added after the latest date in cache
        filters = {"addedAt>>": latest_added_at}
        new_albums = self.library_section.searchAlbums(filters=filters)
        logger.info('Found %d new albums added after %s.', len(new_albums), latest_added_at)

        # Update the album_data dictionary with new albums
        for album in new_albums:
            tracks = album.tracks()
            if tracks:
                media_path = tracks[0].media[0].parts[0].file
                album_folder_path = os.path.dirname(media_path)
                added_at = album.addedAt
                self.album_data[int(album.ratingKey)] = (album_folder_path, added_at)
            else:
                logger.warning('Skipping album with no tracks: %s', album.title)

        # Save the updated album data to the cache
        self.album_cache.save_albums(self.album_data)

    def reset_album_cache(self):
        """Resets the album cache by deleting the cache file."""
        self.album_cache.reset_cache()
        self.album_data = {}
        logger.info('Album cache has been reset.')

    def get_rating_keys(self, path):
        """Returns the rating keys if the path matches an album folder."""
        rating_keys = [key for key, (folder_path, _)
                       in self.album_data.items() if path in folder_path]
        if rating_keys:
            logger.info('Matched album folder name: %s, returning rating keys %s...', path,
                        rating_keys)
        return rating_keys

    def fetch_albums_by_keys(self, rating_keys):
        """Fetches album objects from Plex using their rating keys."""
        logger.info('Fetching albums from Plex using rating keys: %s', rating_keys)
        return self.plex.fetchItems(rating_keys)

    def create_playlist(self, name, albums):
        """Creates a playlist in Plex."""
        logger.info('Creating playlist with name "%s" and %d albums.', name, len(albums))
        playlist = self.plex.createPlaylist(name, self.section_name, albums)
        return playlist

    def create_collection(self, name, albums):
        """Creates a collection in Plex."""
        logger.info('Creating collection with name "%s" and %d albums.', name, len(albums))
        collection = self.library_section.createCollection(name, items=albums)
        return collection

    def get_playlist_by_name(self, name):
        """Finds a playlist by name."""
        playlists = self.plex.playlists()
        for playlist in playlists:
            if playlist.title == name:
                logger.info('Found existing playlist with name "%s".', name)
                return playlist
        logger.info('No existing playlist found with name "%s".', name)
        return None

    def get_collection_by_name(self, name):
        """Finds a collection by name."""
        collections = self.library_section.collections()
        for collection in collections:
            if collection.title == name:
                logger.info('Found existing collection with name "%s".', name)
                return collection
        logger.info('No existing collection found with name "%s".', name)
        return None

    def add_items_to_playlist(self, playlist, albums):
        """Adds albums to an existing playlist."""
        logger.info('Adding %d albums to playlist "%s".', len(albums), playlist.title)
        playlist.addItems(albums)

    def add_items_to_collection(self, collection, albums):
        """Adds albums to an existing collection."""
        logger.info('Adding %d albums to collection "%s".', len(albums), collection.title)
        collection.addItems(albums)
