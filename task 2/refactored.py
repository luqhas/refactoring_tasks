from abc import ABC, abstractmethod
from datetime import datetime

# Strategy: Formatter

class FormatterStrategy(ABC):
    @abstractmethod
    def format(self, text: str) -> str:
        pass


class TextFormatter(FormatterStrategy):
    def format(self, text: str) -> str:
        return text


class CSVFormatter(FormatterStrategy):
    def format(self, text: str) -> str:
        return text.replace("\n", ",")


class HTMLFormatter(FormatterStrategy):
    def format(self, text: str) -> str:
        return f"<html><body><pre>{text}</pre></body></html>"

# Chain of Responsibility

class Handler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, report: str):
        self.process(report)
        if self.next_handler:
            self.next_handler.handle(report)

    @abstractmethod
    def process(self, report: str):
        pass


class LoggingHandler(Handler):
    def process(self, report: str):
        print("LOG: Report generated")


class EmailHandler(Handler):
    def __init__(self, email_service, recipient, subject, next_handler=None):
        super().__init__(next_handler)
        self.email_service = email_service
        self.recipient = recipient
        self.subject = subject

    def process(self, report: str):
        self.email_service.send(self.recipient, self.subject, report)


class ArchiveHandler(Handler):
    def process(self, report: str):
        print("Archived report")

# Template Method

class AbstractReportGenerator(ABC):
    def __init__(self, db, formatter: FormatterStrategy, handler_chain: Handler):
        self.db = db
        self.formatter = formatter
        self.handler_chain = handler_chain

    def generate(self, date_from, date_to):
        data = self.fetch_data(date_from, date_to)

        if not data:
            return self.formatter.format("No data")

        content = []
        content.append(self.get_title())
        content.append(f"Period: {date_from} - {date_to}")

        content.extend(self.process_data(data))

        footer = self.get_footer()
        if footer:
            content.append(footer)

        report = self.formatter.format("\n".join(content))

        self.handler_chain.handle(report)

        return report

    @abstractmethod
    def fetch_data(self, date_from, date_to):
        pass

    @abstractmethod
    def process_data(self, data):
        pass

    @abstractmethod
    def get_title(self):
        pass

    def get_footer(self):
        return ""

# Concrete Reports

class SalesReportGenerator(AbstractReportGenerator):
    def fetch_data(self, date_from, date_to):
        return self.db.query("sales", date_from, date_to)

    def get_title(self):
        return "=== SALES REPORT ==="

    def process_data(self, data):
        result = []
        total = 0
        for s in data:
            result.append(f"{s['id']}: {s['amount']}")
            total += s['amount']
        result.append(f"Total: {total}")
        return result


class InventoryReportGenerator(AbstractReportGenerator):
    def fetch_data(self, date_from, date_to):
        return self.db.query("inventory", date_from, date_to)

    def get_title(self):
        return "=== INVENTORY REPORT ==="

    def process_data(self, data):
        return [f"{i['name']}: {i['stock']} units" for i in data]

    def get_footer(self):
        return f"Generated at: {datetime.now()}"


class UserActivityReportGenerator(AbstractReportGenerator):
    def fetch_data(self, date_from, date_to):
        return self.db.query("activity", date_from, date_to)

    def get_title(self):
        return "=== USER ACTIVITY REPORT ==="

    def process_data(self, data):
        return [f"{u['user']}: {u['actions']} actions" for u in data]

# Mock Infrastructure

class DB:
    def query(self, table, date_from, date_to):
        if table == "sales":
            return [
                {"id": 1, "amount": 100},
                {"id": 2, "amount": 200},
            ]
        elif table == "inventory":
            return [
                {"name": "Item A", "stock": 50},
                {"name": "Item B", "stock": 20},
            ]
        elif table == "activity":
            return [
                {"user": "Alice", "actions": 5},
                {"user": "Bob", "actions": 3},
            ]
        return []


class EmailService:
    def send(self, to, subject, body):
        print(f"Email sent to {to} with subject '{subject}'")

# Example Usage


if __name__ == "__main__":
    db = DB()
    email_service = EmailService()

    formatter = TextFormatter()

    handler_chain = LoggingHandler(
        EmailHandler(
            email_service,
            "manager@co.com",
            "Report",
            ArchiveHandler()
        )
    )

    sales_report = SalesReportGenerator(db, formatter, handler_chain)
    print(sales_report.generate("2024-01-01", "2024-01-31"))

    inventory_report = InventoryReportGenerator(db, formatter, handler_chain)
    print(inventory_report.generate("2024-01-01", "2024-01-31"))

    activity_report = UserActivityReportGenerator(db, formatter, handler_chain)
    print(activity_report.generate("2024-01-01", "2024-01-31"))