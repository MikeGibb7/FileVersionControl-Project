public class LogManager {

    private String[] logs;
    private int count;

    public LogManager() {
        logs = new String[100];
        count = 0;
    }

    public void addLog(String message) {
        if (count < logs.length) {
            logs[count] = message;
            count++;
        }
    }

    public void clearLogs() {
        count = 0;
    }

    public int getLogCount() {
        return count;
    }

    public String getLog(int index) {
        if (index >= 0 && index < count) {
            return logs[index];
        }
        return null;
    }

    public void printAllLogs() {
        for (int i = 0; i < count; i++) {
            System.out.println(logs[i]);
        }
    }

    public void printLatestLog() {
        if (count > 0) {
            System.out.println(logs[count - 1]);
        }
    }

    public void printLogRange(int start, int end) {
        if (start < 0) start = 0;
        if (end > count) end = count;

        for (int i = start; i < end; i++) {
            System.out.println(logs[i]);
        }
    }

    public boolean isEmpty() {
        return count == 0;
    }

    public int capacity() {
        return logs.length;
    }

    public static void main(String[] args) {
        LogManager lm = new LogManager();
        lm.addLog("System started");
        lm.addLog("User logged in");
        lm.printAllLogs();
    }
}
