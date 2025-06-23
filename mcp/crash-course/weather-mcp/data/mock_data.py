# Mock weather data
MOCK_WEATHER_DATA = {
    "new_york": {
        "current": {
            "temperature": 72,
            "humidity": 65,
            "conditions": "Partly Cloudy",
            "wind_speed": 8,
            "wind_direction": "NW",
            "pressure": 1013.2,
            "visibility": 10,
            "uv_index": 6
        },
        "forecast": [
            {"day": "Today", "high": 75, "low": 60, "conditions": "Partly Cloudy", "precipitation": 10},
            {"day": "Tomorrow", "high": 78, "low": 62, "conditions": "Sunny", "precipitation": 0},
            {"day": "Day 3", "high": 73, "low": 58, "conditions": "Light Rain", "precipitation": 70},
            {"day": "Day 4", "high": 69, "low": 55, "conditions": "Cloudy", "precipitation": 30},
            {"day": "Day 5", "high": 76, "low": 61, "conditions": "Sunny", "precipitation": 5}
        ]
    },
    "london": {
        "current": {
            "temperature": 16,
            "humidity": 78,
            "conditions": "Overcast",
            "wind_speed": 12,
            "wind_direction": "SW",
            "pressure": 1008.5,
            "visibility": 8,
            "uv_index": 3
        },
        "forecast": [
            {"day": "Today", "high": 18, "low": 12, "conditions": "Overcast", "precipitation": 40},
            {"day": "Tomorrow", "high": 20, "low": 14, "conditions": "Light Rain", "precipitation": 60},
            {"day": "Day 3", "high": 17, "low": 11, "conditions": "Heavy Rain", "precipitation": 85},
            {"day": "Day 4", "high": 15, "low": 9, "conditions": "Cloudy", "precipitation": 20},
            {"day": "Day 5", "high": 19, "low": 13, "conditions": "Partly Cloudy", "precipitation": 15}
        ]
    },
    "tokyo": {
        "current": {
            "temperature": 23,
            "humidity": 72,
            "conditions": "Sunny",
            "wind_speed": 6,
            "wind_direction": "E",
            "pressure": 1015.8,
            "visibility": 12,
            "uv_index": 8
        },
        "forecast": [
            {"day": "Today", "high": 26, "low": 18, "conditions": "Sunny", "precipitation": 0},
            {"day": "Tomorrow", "high": 28, "low": 20, "conditions": "Partly Cloudy", "precipitation": 10},
            {"day": "Day 3", "high": 25, "low": 17, "conditions": "Thunderstorms", "precipitation": 80},
            {"day": "Day 4", "high": 22, "low": 15, "conditions": "Rainy", "precipitation": 90},
            {"day": "Day 5", "high": 24, "low": 16, "conditions": "Cloudy", "precipitation": 30}
        ]
    }
}