from dataclasses import dataclass


class PostalService:
    @staticmethod
    def send(address: str, message: str):
        print(f"Sending to {address}: {message}")


class BankService:
    @staticmethod
    def transfer(bank_details: str, amount: float):
        print(f"Transferring {amount} via {bank_details}")


class Logger:
    @staticmethod
    def log(message: str):
        print(message)


@dataclass(frozen=True)
class Address:
    address: str
    city: str
    zip_code: str
    country: str

    def __str__(self):
        return f"{self.address}, {self.city}, {self.zip_code}, {self.country}"


@dataclass(frozen=True)
class BankDetails:
    bank_name: str
    bank_account: str
    bank_routing_number: str

    def __str__(self):
        return f"{self.bank_name} {self.bank_account} ({self.bank_routing_number})"


class SalaryCalculation:
    def __init__(
        self,
        base_salary: float,
        overtime_hours: int,
        tax_rate: float,
        pension_rate: float,
        health_rate: float,
    ):
        self.base_salary = base_salary
        self.overtime_hours = overtime_hours
        self.tax_rate = tax_rate
        self.pension_rate = pension_rate
        self.health_rate = health_rate

    def calculate_net(self) -> float:
        gross = self.base_salary + (self.overtime_hours * self.base_salary / 160 * 1.5)
        tax = gross * self.tax_rate
        pension = gross * self.pension_rate
        health = gross * self.health_rate
        return gross - tax - pension - health


class Employee:
    def __init__(
        self,
        name: str,
        salary: SalaryCalculation,
        bank_details: BankDetails,
        address: Address,
    ):
        self.name = name
        self.salary = salary
        self.bank_details = bank_details
        self.address = address

    def calculate_net_salary(self) -> float:
        return self.salary.calculate_net()

    def get_payment_details(self) -> str:
        return str(self.bank_details)

    def get_full_address(self) -> str:
        return str(self.address)

    def send_payslip(self):
        net = self.calculate_net_salary()
        addr = self.get_full_address()
        bank = self.get_payment_details()

        PostalService.send(addr, f"Payslip: {net}")
        BankService.transfer(bank, net)
        Logger.log(f"{self.name} paid {net} to {bank}")