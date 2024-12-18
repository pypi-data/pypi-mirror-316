"""
Base class and implementation of a class that moves models in and out of VRAM.
"""

from typing import Dict, Optional

import torch

from invokeai.backend.model_manager import AnyModel
from invokeai.backend.model_manager.load.model_cache.model_cache_base import (
    CacheRecord,
    ModelCacheBase,
    ModelLockerBase,
)


class ModelLocker(ModelLockerBase):
    """Internal class that mediates movement in and out of GPU."""

    def __init__(self, cache: ModelCacheBase[AnyModel], cache_entry: CacheRecord[AnyModel]):
        """
        Initialize the model locker.

        :param cache: The ModelCache object
        :param cache_entry: The entry in the model cache
        """
        self._cache = cache
        self._cache_entry = cache_entry

    @property
    def model(self) -> AnyModel:
        """Return the model without moving it around."""
        return self._cache_entry.model

    def get_state_dict(self) -> Optional[Dict[str, torch.Tensor]]:
        """Return the state dict (if any) for the cached model."""
        return self._cache_entry.state_dict

    def lock(self) -> AnyModel:
        """Move the model into the execution device (GPU) and lock it."""
        self._cache_entry.lock()
        try:
            if self._cache.lazy_offloading:
                self._cache.offload_unlocked_models(self._cache_entry.size)
            self._cache.move_model_to_device(self._cache_entry, self._cache.execution_device)
            self._cache_entry.loaded = True
            self._cache.logger.debug(f"Locking {self._cache_entry.key} in {self._cache.execution_device}")
            self._cache.print_cuda_stats()
        except torch.cuda.OutOfMemoryError:
            self._cache.logger.warning("Insufficient GPU memory to load model. Aborting")
            self._cache_entry.unlock()
            raise
        except Exception:
            self._cache_entry.unlock()
            raise

        return self.model

    def unlock(self) -> None:
        """Call upon exit from context."""
        self._cache_entry.unlock()
        if not self._cache.lazy_offloading:
            self._cache.offload_unlocked_models(0)
            self._cache.print_cuda_stats()
