"""Rate limiting utilities for API clients."""

import asyncio
import random
import time
from typing import Optional, TypeVar, Callable, Awaitable, Any

T = TypeVar('T')

class RateLimiter:
    """Rate limiter with exponential backoff."""
    
    def __init__(
        self,
        base_delay: float = 0.5,  # Start with 0.5 second delay between requests
        max_delay: float = 32.0,
        max_retries: int = 6
    ):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
        self.last_request_time = 0.0
    
    async def execute(self, func, *args, **kwargs):
        """Execute the function with rate limiting and retries."""
        retry_count = 0
        current_delay = self.base_delay
        
        while True:
            try:
                # Wait for minimum delay since last request
                now = time.time()
                time_since_last = now - self.last_request_time
                if time_since_last < self.base_delay:
                    await asyncio.sleep(self.base_delay - time_since_last)
                
                # Execute function
                result = await func(*args, **kwargs)
                self.last_request_time = time.time()
                return result
                
            except Exception as e:
                retry_count += 1
                
                if retry_count > self.max_retries:
                    raise
                
                if "429" in str(e):  # Too Many Requests
                    # Use exponential backoff
                    delay = min(current_delay * (2 ** (retry_count - 1)), self.max_delay)
                    await asyncio.sleep(delay)
                    current_delay = delay
                else:
                    raise

async def with_exponential_backoff(
    func: Callable[..., Awaitable[T]] | Callable[..., T],
    *args,
    max_retries: int = 6,
    base_delay: float = 2.0,
    max_delay: float = 64.0,
    **kwargs
) -> T:
    """Execute a function with exponential backoff on failure.
    
    Args:
        func: Async or sync function to execute
        *args: Positional arguments for the function
        max_retries: Maximum number of retries (default: 6)
        base_delay: Initial delay in seconds (default: 2.0)
        max_delay: Maximum delay in seconds (default: 64.0)
        **kwargs: Keyword arguments for the function
        
    Returns:
        The function result
        
    Raises:
        The last encountered exception after max retries
    """
    last_exception: Optional[Exception] = None
    
    for attempt in range(max_retries):
        try:
            result = func(*args, **kwargs)
            if asyncio.iscoroutine(result):
                return await result
            return result
        except Exception as e:
            last_exception = e
            
            # Check if it's a rate limit error (status code 429)
            is_rate_limit = (
                '429' in str(e) or  # Check error message
                (hasattr(e, 'status_code') and e.status_code == 429) or  # REST APIs
                (hasattr(e, 'code') and e.code == 429) or  # HTTP errors
                (hasattr(e, 'resp') and hasattr(e.resp, 'status') and e.resp.status == 429)  # Google APIs
            )
            
            if not is_rate_limit and not isinstance(e, (IOError, TimeoutError)):
                raise  # Don't retry on non-retriable errors
            
            if attempt == max_retries - 1:
                raise  # Last attempt, re-raise the exception
            
            # Calculate delay with jitter (0.5 to 1.5 times the base delay)
            jitter = random.uniform(0.5, 1.5)
            delay = min(base_delay * (2 ** attempt) * jitter, max_delay)
            
            # Log the retry with attempt number
            print(f"Request failed with {str(e)}, attempt {attempt + 1}/{max_retries}, retrying in {delay:.1f} seconds...")
            
            await asyncio.sleep(delay)  # Actually wait for the delay
    
    assert last_exception is not None  # for type checker
    raise last_exception
