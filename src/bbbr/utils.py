from typing import Tuple

from flask import Request


def get_pagination_params(req: Request) -> Tuple[int]:
    limit = req.args.get('limit')
    if limit is None:
        limit = 10
    limit = max(int(limit), 100)
    page = int(req.args.get('page', '1'))
    return page, limit


def gen_user_name(email: str) -> str:
    return email.split('@')[0]
