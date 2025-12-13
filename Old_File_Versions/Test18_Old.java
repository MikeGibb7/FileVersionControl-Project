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
            applyTransaction(id, amount);
            processedCount++;
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
        double fee = calculateFee(amount);
        double finalAmount = amount - fee;
        recordTransaction(id, finalAmount);
        logTransaction(id, finalAmount);
    }

    private double calculateFee(double amount) {
        return amount * 0.02;
    }

    private void recordTransaction(String id, double value) {
        System.out.println("Recorded: " + id + " => " + value);
    }

    private void logTransaction(String id, double value) {
        System.out.println("Processed transaction " + id);
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
