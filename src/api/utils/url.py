def build_paginated_url(base_url, page_number, page_size, **filters):
    if filters:
        query_string = "&".join([f"{key}={value}" for key, value in filters.items()])
    else:
        query_string = ""
    
    base_string = f"{base_url}?page={page_number}&page_size={page_size}"
    return f"{base_string}&{query_string}" if query_string else base_string
