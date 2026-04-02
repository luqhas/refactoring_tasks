public class Employee {
    private String name;
    private String department;
    private double baseSalary;
    private int hoursWorked;
    private int overtimeHours;
    private double taxRate;
    private double pensionRate;
    private double healthInsuranceRate;
    private String bankAccount;
    private String bankName;
    private String bankRoutingNumber;
    private String address;
    private String city;
    private String zipCode;
    private String country;

    public double calculateNetSalary() {
        double gross = baseSalary + (overtimeHours * baseSalary / 160 * 1.5);
        double tax = gross * taxRate;
        double pension = gross * pensionRate;
        double health = gross * healthInsuranceRate;
        return gross - tax - pension - health;
    }

    public String getPaymentDetails() {
        return bankName + " " + bankAccount + " (" + bankRoutingNumber + ")";
    }

    public String getFullAddress() {
        return address + ", " + city + ", " + zipCode + ", " + country;
    }

    public void sendPayslip() {
        double net = calculateNetSalary();
        String addr = getFullAddress();
        String bank = getPaymentDetails();
        PostalService.send(addr, "Payslip: " + net);
        BankService.transfer(bank, net);
        Logger.log(name + " paid " + net + " to " + bank);
    }
}
