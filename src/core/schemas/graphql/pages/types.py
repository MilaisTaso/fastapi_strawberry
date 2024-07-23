import strawberry


@strawberry.type(name="PageMeta")
class PageMeta:
    current_page: int
    total_page_count: int
    total_data_count: int
    per_page: int
