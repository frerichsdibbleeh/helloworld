#!/usr/bin/env python3
"""
An example demonstrating the use of the httpx library.
httpx is a modern HTTP client for Python.
"""

import httpx
import asyncio
import json


def sync_example():
    """Synchronous HTTP requests using httpx."""
    print("=== Synchronous Example ===\n")

    # Basic GET request
    print("1. GET request:")
    with httpx.Client() as client:
        response = client.get("https://httpbin.org/get")
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}\n")

    # POST request
    print("2. POST request:")
    with httpx.Client() as client:
        data = {"name": "Alice", "age": 30}
        response = client.post("https://httpbin.org/post", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}\n")

    # Request with custom headers
    print("3. Request with custom headers:")
    with httpx.Client() as client:
        headers = {"User-Agent": "MyApp/1.0", "Authorization": "Bearer token123"}
        response = client.get("https://httpbin.org/headers", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}\n")


async def async_example():
    """Asynchronous HTTP requests using httpx."""
    print("=== Asynchronous Example ===\n")

    # Multiple concurrent requests
    print("1. Multiple concurrent GET requests:")
    urls = [
        "https://httpbin.org/uuid",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/ip",
    ]

    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)

        for i, response in enumerate(responses, 1):
            print(f"Request {i}: {response.json()}")
    print()

    # Async POST with timeout
    print("2. Async POST with timeout:")
    async with httpx.AsyncClient(timeout=5.0) as client:
        data = {"message": "Hello from async httpx"}
        response = await client.post(
            "https://httpbin.org/post",
            json=data
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}\n")


def streaming_example():
    """Streaming large responses."""
    print("=== Streaming Example ===\n")

    with httpx.Client() as client:
        with client.stream("GET", "https://httpbin.org/stream/3") as response:
            print(f"Status Code: {response.status_code}")
            print("Streaming lines:")
            for line in response.iter_lines():
                if line:
                    print(f"  {line}")
    print()


def error_handling_example():
    """Example of error handling."""
    print("=== Error Handling Example ===\n")

    with httpx.Client() as client:
        try:
            # Request to non-existent URL
            response = client.get("https://httpbin.org/status/404")
            response.raise_for_status()  # Raise HTTPError for bad status codes
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code}")
        except httpx.RequestError as e:
            print(f"Request Error: {e}")
    print()


def main():
    """Run all examples."""
    print("HTTPX Library Examples\n")

    # Synchronous examples
    sync_example()

    # Streaming example
    streaming_example()

    # Error handling
    error_handling_example()

    # Asynchronous examples (requires event loop)
    print("Running async example...")
    asyncio.run(async_example())

    print("All examples completed!")


if __name__ == "__main__":
    main()
