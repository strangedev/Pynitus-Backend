"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel

    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import jinja2
from jinja2 import Environment


class HtmlBuilder(object):

    __environment = None  # type: Environment
    __management = None

    @classmethod
    def setJinja2Environment(cls, template_path: str) -> None:
        HtmlBuilder.__environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path)
        )

    @classmethod
    def setManagement(cls, management):
        HtmlBuilder.__management = management

    @staticmethod
    def render(template_name: str, ip_address: int, **kwargs) -> str:
        template = HtmlBuilder.__environment.get_template(template_name)

        return template.render(
            html_dir=HtmlBuilder.__management.config.get("html_dir"),
            actionsLeft=HtmlBuilder.__management.flood_protection.actionsLeft(ip_address),
            maxActions=HtmlBuilder.__management.flood_protection.max_actions,
            playbackQueue=HtmlBuilder.__management.playback_queue,
            voteCount=HtmlBuilder.__management.vote_handler.votes,
            votesRequired=HtmlBuilder.__management.vote_handler.getRequiredVotes(),
            playing=HtmlBuilder.__management.playback_queue.playing,
            **kwargs
            )
