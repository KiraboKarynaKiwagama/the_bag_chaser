import unittest

from server import filter_jobs


class FilterJobsTests(unittest.TestCase):
    def test_search_filters_by_title_company_and_category(self):
        jobs = [
            {"title": "Senior Developer", "company": "Acme", "category": "Software Development"},
            {"title": "Designer", "company": "Beta", "category": "Design"},
            {"title": "Product Manager", "company": "Gamma", "category": "Product Management"},
        ]

        filtered = filter_jobs(jobs, "developer", "")

        self.assertEqual([job["title"] for job in filtered], ["Senior Developer"])

    def test_category_filter_matches_ui_values(self):
        jobs = [
            {"title": "Senior Developer", "company": "Acme", "category": "Software Development"},
            {"title": "Designer", "company": "Beta", "category": "Design"},
            {"title": "Sales Lead", "company": "Delta", "category": "Sales"},
        ]

        filtered = filter_jobs(jobs, "", "sales-business")

        self.assertEqual([job["title"] for job in filtered], ["Sales Lead"])


if __name__ == "__main__":
    unittest.main()
