from app.database.models import FreelanceProject


class FilterAgent:
    name = "FilterAgent"

    def free_to_apply(self, projects: list[FreelanceProject]) -> list[FreelanceProject]:
        return [
            project
            for project in projects
            if project.is_free_to_apply == "yes"
        ]
