import os
import sys
import logging
import json
import random
from urllib.parse import urljoin

import httpx
from httpx import codes
from faker import Faker


NUMBER_OF_USERS = 10
MAX_POSTS_PER_USER = 10
MAX_LIKES_PER_USER = 10

BASE_URL = "http://127.0.0.1:8000/api/"
POSTS_ENDPOINT = urljoin(BASE_URL, "posts/")
REGISTRATION_ENDPOINT = urljoin(BASE_URL, "user/register/")
TOKEN_ENDPOINT = urljoin(BASE_URL, "user/token/")

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s:%(message)s", level=logging.INFO
)

fake = Faker()


def read_config(config_path: str) -> dict:
    if not os.path.isfile(config_path):
        logging.error("Invalid path to the configuration file")
        sys.exit(1)

    if os.stat(config_path).st_size == 0:
        logging.error("Configuration file is empty")
        sys.exit(1)

    with open(config_path) as fobj:
        try:
            config = json.load(fobj)
        except json.JSONDecodeError as e:
            logging.debug(e)
            logging.error("Configuration file contains invalid json")
            sys.exit(1)

    return config


def generate_users(number_of_users: int) -> list[dict]:
    users = [
        {"username": fake.user_name(), "password": fake.password()}
        for _ in range(number_of_users)
    ]

    return users


def signup_users(users: list[dict], client: httpx.Client) -> None:
    for user_data in users:
        response = client.post(REGISTRATION_ENDPOINT, json=user_data)
        response.raise_for_status()


def get_jwt_tokens(users: list[dict], client: httpx.Client) -> list[str]:
    jwt_tokens = []
    for user_data in users:
        response = client.post(TOKEN_ENDPOINT, json=user_data)
        if response.status_code == codes.OK:
            jwt_tokens.append(response.json()["access"])
        else:
            logging.info(
                f"Token request was not successful: {response.status_code}"
            )

    return jwt_tokens


def create_posts(
    jwt_tokens: list[str], max_posts_per_user: int, client: httpx.Client
) -> int:
    created_posts = 0
    for token in jwt_tokens:
        for _ in range(random.randint(1, max_posts_per_user)):
            data = {"title": fake.text(30), "text": fake.text()}
            headers = {"Authorization": f"Bearer {token}"}
            response = client.post(POSTS_ENDPOINT, json=data, headers=headers)
            if response.status_code == codes.CREATED:
                created_posts += 1

    return created_posts


def like_posts(
    jwt_tokens: list[str],
    max_likes_per_user: int,
    num_posts: int,
    client: httpx.Client,
) -> None:
    for token in jwt_tokens:
        headers = {"Authorization": f"Bearer {token}"}
        for _ in range(max_likes_per_user):
            post_id = random.randint(1, num_posts)
            url = urljoin(POSTS_ENDPOINT, f"{post_id}/like/")
            response = client.post(url, headers=headers)
            response.raise_for_status()


def main(args: list[str]) -> None:
    if len(args) == 1:
        logging.error("Path to the configuration file is not specified")
        sys.exit(1)

    _, config_path, *_ = args

    config = read_config(config_path)

    number_of_users = config.get("number_of_users", NUMBER_OF_USERS)
    max_posts_per_user = config.get("max_posts_per_user", MAX_POSTS_PER_USER)
    max_likes_per_user = config.get("max_likes_per_user", MAX_LIKES_PER_USER)

    users = generate_users(number_of_users)

    with httpx.Client() as client:
        signup_users(users, client)
        jwt_tokens = get_jwt_tokens(users, client)
        created_posts = create_posts(jwt_tokens, max_posts_per_user, client)
        like_posts(jwt_tokens, max_likes_per_user, created_posts, client)


if __name__ == "__main__":
    main(sys.argv)
