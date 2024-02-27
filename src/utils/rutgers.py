from typing import List

import requests

SEMESTERS = {"spring": 1, "summer": 7, "fall": 9, "winter": 0}

CAMPUS_CODES = {"newark": "NK", "new brunswick": "NB", "camden": "CM"}

DAY_NAMES = {
    "M": "Monday",
    "T": "Tuesday",
    "W": "Wednesday",
    "H": "Thursday",
    "F": "Friday",
    "S": "Saturday",
}

SUBJECTS = {
    640: "Mathematics",
    198: "Computer Science",
    623: "Management Science and Information Systems",
    547: "Information Technology and Informatics",
    548: "Information Systems",
}


class RutgersScheduleOfClasses:
    def __init__(self, year: str, term: str, campus: str):
        self.year = year
        self.term = term
        self.campus = campus

    def _construct_url(self) -> str:
        """Constructs the URL for the HTTP request based on the term, year, and campus."""
        term = SEMESTERS[self.term.lower()]
        year = self.year
        campus = CAMPUS_CODES[self.campus.lower()]
        return f"https://classes.rutgers.edu/soc/api/courses.json?year={year}&term={term}&campus={campus}"

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
        Fetches the schedule of classes from the Rutgers API.

        Returns:
            A list of dictionaries representing the schedule of classes, or None if an error occurred.
        """
        try:
            response = requests.get(self._construct_url())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the schedule of classes: {e}")
            raise e

    def fetch_filtered_schedule_of_classes(self) -> List[dict]:
        """
        Fetches the schedule of classes from the Rutgers API and filters the results.

        Returns:
            A list of dictionaries representing the filtered schedule of classes, or None if an error occurred.
        """
        try:
            response = requests.get(self._construct_url())
            response.raise_for_status()
            return self._classes_parser(response.json())
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the schedule of classes: {e}")
            raise e
