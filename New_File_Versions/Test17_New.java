public class OrderProcessor {

    private int totalOrders;
    private double totalRevenue;

    public OrderProcessor() {
        totalOrders = 0;
        totalRevenue = 0.0;
    }

    public void addOrder(double amount) {
        totalOrders++;
        totalRevenue += amount;
    }

    public int getTotalOrders() {
        return totalOrders;
    }

    public double getTotalRevenue() {
        return totalRevenue;
    }

    public void printSummary() {
        System.out.println("Orders: " + totalOrders);
        System.out.println("Revenue: " + totalRevenue);
    }

    public boolean hasOrders() {
        return totalOrders > 0;
    }

    public double averageOrderValue() {
        if (totalOrders == 0) {
            return 0.0;
        }
        return totalRevenue / totalOrders;
    }

    public void printDetailedReport() { // moved
        System.out.println("=== REPORT ===");
        System.out.println("Orders: " + totalOrders);
        System.out.println("Revenue: " + totalRevenue);
        System.out.println("Average: " + averageOrderValue());
    }

    public void applyDiscount(double percent) { // moved
        if (percent > 0 && percent <= 100) {
            totalRevenue -= totalRevenue * (percent / 100);
        }
    }

    public void clearAll() { // moved
        totalOrders = 0;
        totalRevenue = 0.0;
    }

    public void applyServiceFee(double fee) { // added
        if (fee > 0) {
            totalRevenue += fee;
        }
    }

    // refundLastOrder removed

    public void logState() {
        System.out.println("[LOG] Orders=" + totalOrders + ", Revenue=" + totalRevenue);
    }

    public static void main(String[] args) {
        OrderProcessor op = new OrderProcessor();
        op.addOrder(100);
        op.addOrder(50);
        op.applyDiscount(10);
        op.printDetailedReport();
    }
}
