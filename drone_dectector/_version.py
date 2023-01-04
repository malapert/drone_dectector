# Drone dectector - Drone detector
# Copyright (C) 2023 - Malapert
#
# This file is part of Drone dectector.
#
# Drone dectector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Drone dectector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Drone dectector.  If not, see <https://www.gnu.org/licenses/>.
"""Project metadata."""
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

__name_soft__ = "drone_dectector"
try:
    __version__ = get_distribution(__name_soft__).version
except DistributionNotFound:
    __version__ = "0.0.0"
__title__ = "Drone dectector"
__description__ = "Drone detector"
__url__ = "https://github.com/malapert/drone_dectector"
__author__ = "Jean-Christophe Malapert"
__author_email__ = "jcmalapert@gmail.com"
__license__ = "GNU General Public License v3"
__copyright__ = "2023, Malapert"
