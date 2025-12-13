public class TransactionProcessor {

    private String systemName;
    private int processedCount;

    public TransactionProcessor(String systemName) {
        this.systemName = systemName;
        this.processedCount = 0;
    }

    public void start() {
        logStartup();
        initializeCounters();
    }

    private void logStartup() {
        System.out.println("Starting system: " + systemName);
    }

    private void initializeCounters() {
        processedCount = 0;
    }

    public void processTransaction(String id, double amount) {
        if (validate(id, amount)) {
            processedCount++; // moved
            applyTransaction(id, amount);
        }
    }

    private boolean validate(String id, double amount) {
        if (id == null || id.isEmpty()) {
            return false;
        }
        if (amount <= 0) { 
            return false;
        }
        return true;
    }

    private void applyTransaction(String id, double amount) {
        double finalAmount = applyDiscount(amount); // changed
        recordTransaction(id, finalAmount);
        auditTransaction(id, finalAmount); // changed
    }

    private double applyDiscount(double amount) { // changed
        return amount - calculateFee(amount);
    }

    private double calculateFee(double amount) {
        return amount * 0.015; // changed
    }

    private void auditTransaction(String id, double value) { // changed
        System.out.println("Audit: " + id + " value=" + value);
    }

    private void recordTransaction(String id, double value) {
        System.out.println("Recorded: " + id + " => " + value);
    }

    public int getProcessedCount() {
        return processedCount;
    }

    public void shutdown() {
        flushLogs();
        printSummary();
    }

    private void flushLogs() {
        System.out.println("Flushing logs");
    }

    private void printSummary() {
        System.out.println("Total processed: " + processedCount);
    }

    public String getSystemName() {
        return systemName;
    }

    public void resetSystem() {
        processedCount = 0;
        System.out.println("System reset");
    }

    public boolean isHealthy() {
        return processedCount >= 0;
    }
}
