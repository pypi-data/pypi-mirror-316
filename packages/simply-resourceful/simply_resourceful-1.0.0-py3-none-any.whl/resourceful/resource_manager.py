from __future__ import annotations

from collections.abc import Callable
import difflib
import os
from pathlib import Path
from typing import Any, Literal, TypeVar


T = TypeVar("T")


class SentinelMeta(type):

    def __repr__(cls) -> str:
        return f"<{cls.__name__}>"

    def __bool__(cls) -> Literal[False]:
        return False


class NoDefault(metaclass=SentinelMeta):
    """
    Sentinel class to serve as a comparison for default asset parameters, allowing None
    to be a valid asset value.
    """

    pass


class ResourceManager[T]:
    """
    A class for that tracks resources of a given type, ascribing handles to them for
    easy reference, and lazy loading them when requested.
    """

    _instances: dict[type[T], dict[str, ResourceManager]] = {}

    def __init__(self, handle: str) -> None:
        """
        Create an asset manager for the given type, with the given handle.

        :param type: Type of asset to be managed.
        :param handle: Name for the asset manager, so multiple managers for the same
        resource type can exist.
        """
        self.handle = handle
        """
        Name of the Resource Manager
        """
        self.cache: dict[str, T] = {}
        """
        Dictionary caching all of the loaded assets with their handles.
        """
        self.resource_locations: dict[str, Any] = {}
        """
        Dictionary holding needed loading data for each asset.
        """
        self.default_asset: T | None | NoDefault = NoDefault
        """
        Default asset to be supplied if requested asset cannot be loaded.
        """

    def config(
        self,
        loader_helper: Callable | None = None,
        default_asset: T | None | NoDefault = NoDefault,
    ) -> None:
        """
        Modifies the resource manager's behavior per the specified parameters.

        :param loader_helper: Loader function for the resource. Must take the location
        data its parameter, and return an instance of the resource.
        :param default_asset: An asset matching the manager's managed type, or None.
        Defaults to No_Default.
        """
        if loader_helper:
            self._asset_loader = loader_helper
        if default_asset is not NoDefault:
            self.default_asset = default_asset

    def import_asset(self, asset_handle: str, resource_location: Any) -> None:
        """
        Prepares the resource manager to load a resource.

        :param asset_handle: The name of the resource, this will be the name that users
        of the resource will need to reference in order to acquire it.
        :param resource_location: The data the asset loader needs to produce the
        resource. It may be a path, or a download site, or anything else, so long
        as the asset loader can handle the parameters.
        """
        self.resource_locations.update({asset_handle: resource_location})

    def import_directory(
        self,
        folder: os.PathLike | str,
        recursive: bool = False,
        file_filter: Callable | None = None,
        name_generator: Callable | None = None,
        location_data_generator: Callable | None = None,
    ):
        """
        Parse a directory, importing all of the files inside into the resource manager.

        :param folder: Target directory
        :param recursive: Whether to recursively search through subdirectories,
        defaults to False
        :param file_filter: A function for choosing files to import, defaults all files.
        Will be called for subfolders as well, and can be used to exclude undesired
        subfolders.
        If you have mixed file types, do not rely on the default filter.
        :param name_generator: A function for creating asset names from files, defaults
        to the relative path to the directory plus the name of the file.
        :param location_data_generator: Function for generating the location data
        required for the asset loader, defaults to the file's path.
        """
        directory = Path(folder)

        if not directory.is_dir():
            raise NotADirectoryError(f"'{folder}' is not a valid directory.")

        if file_filter is None:

            def file_filter(file: Path) -> Path | None:
                return file

        if name_generator is None:

            def name_generator(file: Path) -> str:
                """
                Uses the relative path and filename, without suffixes,
                as the default asset handle.
                """
                file = file.relative_to(folder)
                while file.suffix != "":
                    file = file.with_suffix("")
                return str(file.as_posix())

        if location_data_generator is None:

            def location_data_generator(file: Path) -> Path:
                """
                Gives path of the file as its location.
                """
                return file

        files = list(directory.iterdir())
        for item in files:
            if not file_filter(item):
                # Filter first so the filter can be used to exclude specific folders.
                continue
            if item.is_dir():
                if recursive:
                    for file in item.iterdir():
                        files.append(file)
                continue
            self.import_asset(name_generator(item), location_data_generator(item))

    def force_load(self, asset_handle: str, resource_location: Any) -> None:
        """
        Establishes the resource in the database, and loads it immediately instead of
        deferring to when the asset is requested.

        :param asset_handle: The name of the resource, which can be referenced by
        users of that resource.
        :param resource_location: The data the asset loader needs to produce the
        resource.
        """
        self.import_asset(asset_handle, resource_location)
        asset: T = self._asset_loader(resource_location)
        self.cache.setdefault(asset_handle, asset)

    def update(self, asset_handle: str, asset: T) -> T | None:
        """
        Changes the loaded resource of the given handle to that of the given asset.

        :param asset_handle: The name of the resource, which can be referenced by
        users of that resource.
        :param asset: The new asset replacing the old asset.
        :return: The old asset, or None if the asset wasn't loaded.
        """
        old_asset = self.cache.get(asset_handle, None)
        self.cache[asset_handle] = asset
        return old_asset

    def force_update(self, asset_handle: str, asset: T) -> None:
        """
        [Experimental]

        Forces the asset at the given handle to become a copy of the supplied asset.
        This will hot-swap the asset for all of its users.

        Note - Not all objects may support this behavior, and may be broken by it.
        Only works when the asset class mainly used __dict__. Slotified classes may
        fail if they also lack a __dict__, or miss out on important data.

        :param asset_handle: The name of the resource
        :param asset: The new asset replacing the old asset.
        """
        old_asset = self.cache.get(asset_handle, None)
        if old_asset is None:
            # Nothing to replace, so just fill it in
            self.cache[asset_handle] = asset
            return
        # Otherwise, force the loaded asset to take on the new asset's attributes.
        old_asset.__dict__ = asset.__dict__

    def get(
        self, asset_handle: str, default: T | None | NoDefault = NoDefault
    ) -> T | None:
        """
        Gets the asset of the requested handle. Loads the asset if it hasn't been
        already.
        If the asset can't be loaded and a default is given or available in the manager,
        pass along that instead.
        The default is not added to the cache.

        :param asset_handle: Name of the asset to be gotten
        :param default: Item returned if the asset is unavailable
        :raises KeyError: Raised if handle is not found or fails to load,
        and no default is given or otherwise available.
        :return: The (loaded) instance of the asset, or the default if available.
        """
        if default is NoDefault and self.default_asset is not NoDefault:
            # Refer to the manager's default asset if no local default is provided.
            default = self.default_asset
        if asset_handle not in self.resource_locations:
            if default is NoDefault:
                closest = difflib.get_close_matches(
                    asset_handle, self.resource_locations.keys(), n=1
                )
                error_msg = f"Resource '{asset_handle}' is not handled by {self}."
                if len(closest) > 0:
                    error_msg += f" Did you mean '{closest[0]}'?"
                raise KeyError(error_msg)
            return default
        asset = self.cache.get(asset_handle, None)
        if asset is None:
            asset = self._asset_loader(self.resource_locations.get(asset_handle))
            if asset is None:
                # Last chance to get an asset
                if default is NoDefault:
                    raise KeyError(f"Resource '{asset_handle}' failed to load.")
                asset = default
            self.cache[asset_handle] = asset
        return asset

    def uncache(self, asset_handle: str) -> T | None:
        """
        Unloads the specified asset from the manager. Existing copies of the resource
        being used by objects will keep it in memory until they cease using it.

        If the asset is requested again, it will be reloaded.

        Safe to call, will not error if an invalid handle is used.

        :param asset_handle: The name of the resource
        :return: The resource being unloaded, or None if it does not exist.
        """
        return self.cache.pop(asset_handle, None)

    def clear(self, asset_handle: str) -> tuple[T | None, Any] | None:
        """
        Unloads the asset, and removes it from the load dictionary.

        If the resource is requested again, it will fail to load.

        :param asset_handle: The name of the resource being cleared.
        :return: A tuple containing the old asset and its location data, or None if
        none exists.
        """
        old_asset = self.uncache(asset_handle)
        old_location = self.resource_locations.pop(asset_handle, None)
        if old_location is None:
            return None
        return (old_asset, old_location)

    @staticmethod
    def _asset_loader(*args, **kwds):
        """
        This is overwritten by self.config

        :raises AttributeError: If asset_loader is not supplied via config.
        """
        raise AttributeError(
            "No loader function assigned. You must assign a loader to run."
        )


def getResourceManager(asset_type: type[T], handle: str = "") -> ResourceManager[T]:
    """
    Provides a Resource Manager of the specified type and handle.
    If the asset type or handle do not match an existing one, it will be created.

    :param asset_type: The Type of the resource being managed.
    :param handle: The name of the manager, defaults to ""
    :return: The resource manager of the type and handle specified.
    """
    manager_set = ResourceManager._instances.setdefault(asset_type, {})
    return manager_set.setdefault(handle, ResourceManager[asset_type](handle))
