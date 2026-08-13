from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CachePolicy:
    cacheable: bool
    max_age: int | None = None


def parse_cache_control(value: str | None) -> CachePolicy:
    if value is None:
        return CachePolicy(cacheable=True)

    directives = [
        directive.strip().casefold()
        for directive in value.split(",")
        if directive.strip()
    ]

    max_age: int | None = None
    for directive in directives:
        if directive == "no-store":
            return CachePolicy(cacheable=False)

        if directive.startswith("max-age="):
            raw_value = directive.split("=")[1]

            try:
                parsed_max_age = int(raw_value)
            except ValueError:
                return CachePolicy(cacheable=False)

            if parsed_max_age < 0:
                return CachePolicy(cacheable=False)

            max_age = parsed_max_age
            continue

        # Если встретили что-то кроме no-store/max-age, то не кэшируем
        return CachePolicy(cacheable=False)

    return CachePolicy(cacheable=True, max_age=max_age)
