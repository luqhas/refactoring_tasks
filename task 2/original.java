public class SalesReportGenerator {
    public String generate(Date from, Date to) {
        StringBuilder sb = new StringBuilder();
        sb.append("=== SALES REPORT ===");
        sb.append("Period: " + from + " - " + to);
        List<Sale> data = db.query(
            "SELECT * FROM sales WHERE date BETWEEN ? AND ?", from, to);
        if (data.isEmpty()) { sb.append("No data"); return sb.toString(); }
        double total = 0;
        for (Sale s : data) {
            sb.append(s.getId() + ": " + s.getAmount());
            total += s.getAmount();
        }
        sb.append("Total: " + total);
        logger.info("Sales report generated");
        emailService.send("manager@co.com", "Sales Report", sb.toString());
        return sb.toString();
    }
}

public class InventoryReportGenerator {
    public String generate(Date from, Date to) {
        StringBuilder sb = new StringBuilder();
        sb.append("=== INVENTORY REPORT ===");
        sb.append("Period: " + from + " - " + to);
        List<Item> data = db.query(
            "SELECT * FROM inventory WHERE updated BETWEEN ? AND ?", from, to);
        if (data.isEmpty()) { sb.append("No data"); return sb.toString(); }
        for (Item i : data) {
            sb.append(i.getName() + ": " + i.getStock() + " units");
        }
        sb.append("Generated at: " + new Date());
        logger.info("Inventory report generated");
        emailService.send("warehouse@co.com", "Inventory Report", sb.toString());
        return sb.toString();
    }
}
