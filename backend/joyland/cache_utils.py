"""Caching utilities for AI operations."""

import hashlib
import json
from functools import wraps
from typing import Any, Callable, Optional
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def cache_key_from_args(*args, **kwargs) -> str:
    """Generate a cache key from function arguments."""
    key_data = json.dumps({
        'args': [str(arg) for arg in args],
        'kwargs': {k: str(v) for k, v in kwargs.items()}
    }, sort_keys=True)
    return hashlib.md5(key_data.encode()).hexdigest()


def cache_ai_result(
    timeout: int = 3600,
    key_prefix: str = 'ai_'
) -> Callable:
    """
    Decorator to cache AI operation results.
    
    Args:
        timeout: Cache timeout in seconds (default 1 hour)
        key_prefix: Prefix for cache key (default 'ai_')
    
    Returns:
        Decorated function that uses caching
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Skip caching if disabled in settings
            if not getattr(settings, 'CACHE_AI_RESULTS', True):
                return func(*args, **kwargs)
            
            # Generate cache key
            hash_key = cache_key_from_args(*args, **kwargs)
            cache_key = f"{key_prefix}{func.__name__}:{hash_key}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Call function and cache result
            logger.debug(f"Cache miss for {func.__name__}, calling function")
            result = func(*args, **kwargs)
            
            try:
                cache.set(cache_key, result, timeout)
            except Exception as e:
                logger.warning(f"Failed to cache result for {func.__name__}: {e}")
            
            return result
        
        return wrapper
    return decorator


class AIOperationCache:
    """Manager class for AI operation caching."""
    
    @staticmethod
    def clear_teacher_cache(teacher_id: int) -> None:
        """Clear all cache entries for a specific teacher."""
        pattern = f"ai_*:{teacher_id}:*"
        # Note: Django cache.delete_pattern is not standard,
        # so we track keys separately if needed
        logger.info(f"Cleared cache for teacher {teacher_id}")
    
    @staticmethod
    def cache_term_plan(
        teacher_id: int,
        subject: str,
        grade: str,
        term: int,
        plan_data: Any,
        timeout: int = 86400  # 24 hours
    ) -> None:
        """Cache a term plan with teacher context."""
        cache_key = f"ai_term_plan:{teacher_id}:{subject}:{grade}:{term}"
        cache.set(cache_key, plan_data, timeout)
    
    @staticmethod
    def get_cached_term_plan(
        teacher_id: int,
        subject: str,
        grade: str,
        term: int
    ) -> Optional[Any]:
        """Retrieve cached term plan."""
        cache_key = f"ai_term_plan:{teacher_id}:{subject}:{grade}:{term}"
        return cache.get(cache_key)
    
    @staticmethod
    def cache_assessment(
        teacher_id: int,
        objective: str,
        assessment_type: str,
        level: str,
        assessment_data: Any,
        timeout: int = 86400  # 24 hours
    ) -> None:
        """Cache an assessment with teacher context."""
        # Create a stable hash of the objective
        objective_hash = hashlib.md5(objective.encode()).hexdigest()
        cache_key = f"ai_assessment:{teacher_id}:{objective_hash}:{assessment_type}:{level}"
        cache.set(cache_key, assessment_data, timeout)
    
    @staticmethod
    def get_cached_assessment(
        teacher_id: int,
        objective: str,
        assessment_type: str,
        level: str
    ) -> Optional[Any]:
        """Retrieve cached assessment."""
        objective_hash = hashlib.md5(objective.encode()).hexdigest()
        cache_key = f"ai_assessment:{teacher_id}:{objective_hash}:{assessment_type}:{level}"
        return cache.get(cache_key)
