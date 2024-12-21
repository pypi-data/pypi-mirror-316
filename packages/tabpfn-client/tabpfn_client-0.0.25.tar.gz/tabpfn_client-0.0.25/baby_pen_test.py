import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def get():
    return requests.get(
        "https://api.github.com/repos/tabpfn/tabpfn-client/releases/latest"
    )


pool = ThreadPoolExecutor(max_workers=100)

futures = [pool.submit(get) for _ in range(100_000)]


seen_codes = set()

for future in as_completed(futures):
    response = future.result()
    if response.status_code not in seen_codes:
        seen_codes.add(response.status_code)
        print(response.status_code, response.content)
