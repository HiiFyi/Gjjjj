from typing import Union

from pyrate_limiter import BucketFullException, Duration, InMemoryBucket, Limiter, Rate


class RateLimiter:
    """
    Implement rate limit logic using leaky bucket
    algorithm, via pyrate_limiter.
    (https://pypi.org/project/pyrate-limiter/)
    """

    def __init__(self) -> None:
        # 15 requests per minute.
        self.minute_rate = Rate(15, Duration.MINUTE)

        # 100 requests per hour
        self.hourly_rate = Rate(100, Duration.HOUR)

        # 300 requests per day
        self.daily_rate = Rate(300, Duration.DAY)

        self.limiter = Limiter([self.minute_rate, self.hourly_rate, self.daily_rate])

    async def acquire(self, userid: Union[int, str]) -> bool:
        """
        Acquire rate limit per userid and return True / False
        based on userid ratelimit status.
        """

        try:
            self.limiter.try_acquire(userid)
            return False
        except BucketFullException:
            return True
