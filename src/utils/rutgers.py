import json
from typing import List

from src.utils.aws import S3Access
from src.utils.cache import RedisAccess

DAY_NAMES = {
    "M": "Monday",
    "T": "Tuesday",
    "W": "Wednesday",
    "H": "Thursday",
    "F": "Friday",
    "S": "Saturday",
}

SUBJECTS = {
    198: "Computer Science",
    547: "Information Technology and Informatics",
    548: "Information Systems",
    623: "Management Science and Information Systems",
    640: "Mathematics",
}


class RutgersScheduleOfClasses(S3Access):
    def __init__(self, year: str, term: str, campus: str, role_arn: str, bucket_name: str):
        super().__init__(role_arn, bucket_name)
        self.year = year
        self.term = term.lower()
        self.campus = campus.lower()

    @staticmethod
    def _classes_parser(data: List[dict]) -> List[dict]:
        """Parses the classes from the response data."""
        subject_to_filter = list(SUBJECTS.keys())
        course_info = [
            {
                "title": x["expandedTitle"].strip(),
                "department": SUBJECTS.get(int(x["subject"]), "Unknown Department"),
                "courseCode": x["courseString"],
                "credits": x["creditsObject"]["description"],
                "sections": [
                    {
                        "section": section["number"],
                        "instructor": section["instructorsText"],
                        "status": "Open" if section["openStatus"] else "Closed",
                        "meetings": [
                            f"{DAY_NAMES.get(mt['meetingDay'], 'Unknown Day')}: {mt['startTime']} - {mt['endTime']}, {mt['campusName']}"  # noqa
                            for mt in section["meetingTimes"]
                        ],
                    }
                    for section in x["sections"]
                ],
            }
            for x in data
            if int(x["subject"]) in subject_to_filter and x["expandedTitle"].strip() != ""
        ]

        return course_info

    def fetch_schedule_of_classes(self) -> List[dict]:
        """
        Fetches the schedule of classes from our s3 bucket.

        Returns:
            A list of dictionaries representing the schedule of classes, or None if an error occurred.
        """
        try:

            key = f"{self.year}/{self.term}/{self.campus}.json"

            response = self.get_object(key)

            return json.loads(response)
        except Exception as e:
            print(f"An error occurred while fetching the schedule of classes: {e}")
            raise e

    def fetch_filtered_schedule_of_classes(self) -> List[dict]:
        """
        Fetches the schedule of classes from the Rutgers API and filters the results.

        Returns:
            A list of dictionaries representing the filtered schedule of classes, or None if an error occurred.
        """
        try:
            cache_key = f"{self.year}:{self.term}:{self.campus}"

            cache = RedisAccess()

            cached_response = cache.get_value(cache_key)
            if cached_response:
                return json.loads(cached_response)

            key = f"{self.year}/{self.term}/{self.campus}.json"

            response = self.get_object(key)
            if not response:
                print(f"An error occurred while fetching the schedule of classes: {response}")
                return []
            filtered_data = self._classes_parser(json.loads(response))
            cache.set_value(cache_key, json.dumps(filtered_data))
            return filtered_data
        except Exception as e:
            print(f"An error occurred while fetching the schedule of classes: {e}")
            raise e
