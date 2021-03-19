from typing import List

import sys
import aiohttp
import asyncio

GENERATOR_DOMAIN = 'https://www.toptal.com/developers/gitignore/api'


def normalize_technology(technology: str) -> str:
    return technology.strip().replace(' ', '').lower()


async def fetch_gitignore_file(technologies: List[str]) -> str:
    subdir: str = ','.join([normalize_technology(t) for t in technologies])
    print(f'[OPERATION] fetching gitignore file... technologies: "{subdir}"')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{GENERATOR_DOMAIN}/{subdir}') as response:
            html = await response.text()
            print(
                f'[RESULT] gitignore file received, '
                f'length: "{len(html)}", '
                f'status: "{response.status}", '
                f'content-type:{response.headers.get("content-type", "")}'
            )
            return html


def clean_gitignore_file(content: str) -> str:
    print('[OPERATION] cleaning file content...')
    lines = content.split('\n')
    return '\n'.join(lines[3:-1])


def save_gitignore_file(content: str) -> None:
    print('[OPERATION] saving to ".gitignore"')
    with open('.gitignore', 'w', encoding='utf8') as file:
        file.write(content)


async def generate_gitignore_file(technologies: List[str]):
    fetched: str = await fetch_gitignore_file(technologies)
    save_gitignore_file(clean_gitignore_file(fetched))
    print('[RESULT] successfully generated .gitignore file')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_gitignore_file(sys.argv[1:]))
