# Copyright © 2025-2026 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from neuro_san.interfaces.coded_tool import CodedTool

logger = logging.getLogger(__name__)


class TravelPlanner(CodedTool):
    """
    Generates a short travel itinerary or a budget-aware recommendation.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Builds either:
          - an itinerary for a given destination, duration, interests, and style, or
          - a budget recommendation for a trip destination and total budget.
        """
        destination = args.get("destination") or sly_data.get("destination") or "your destination"
        duration_days = int(args.get("duration_days") or args.get("trip_length_days") or sly_data.get("duration_days") or 3)
        interests = args.get("interests") or sly_data.get("interests") or ["food", "culture", "nature"]
        travel_style = args.get("travel_style") or sly_data.get("travel_style") or "balanced"

        if "budget_usd" in args or "trip_length_days" in args or "budget_usd" in sly_data:
            budget_usd = float(args.get("budget_usd") or sly_data.get("budget_usd") or 600.0)
            trip_length_days = int(args.get("trip_length_days") or sly_data.get("trip_length_days") or duration_days)
            daily_budget = round(budget_usd / max(trip_length_days, 1), 2)
            recommendations = [
                "Choose a mid-range hotel or guesthouse near the city center for easier access.",
                "Use public transit or rideshare strategically to reduce daily transport costs.",
                "Prioritize one signature activity per day and mix in free walking tours or local markets."
            ]
            return {
                "destination": destination,
                "trip_length_days": trip_length_days,
                "budget_usd": round(budget_usd, 2),
                "daily_budget_usd": daily_budget,
                "recommendations": recommendations,
                "travel_style": travel_style,
            }

        if isinstance(interests, str):
            interests = [interests]

        itinerary: List[Dict[str, Any]] = []
        for day in range(1, duration_days + 1):
            focus = interests[(day - 1) % len(interests)] if interests else "local highlights"
            itinerary.append({
                "day": day,
                "theme": focus,
                "plan": f"Spend the day exploring {destination} with a focus on {focus}, keeping a relaxed {travel_style} pace."
            })

        return {
            "destination": destination,
            "duration_days": duration_days,
            "travel_style": travel_style,
            "interests": interests,
            "itinerary": itinerary,
        }

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Async wrapper around the synchronous invoke implementation.
        """
        return self.invoke(args, sly_data)
