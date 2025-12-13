public class TaskManager {

    private String name;
    private int maxTasks;
    private int currentTasks;
    private int completedTasks;

    public TaskManager(String name, int maxTasks) {
        this.name = name;
        this.maxTasks = maxTasks;
        this.currentTasks = 0;
    }

    public boolean canAddTask() {
        return currentTasks < maxTasks;
    }
    
    public String getName() {
        return name;
    }

    public int getCurrentTasks() {
        return currentTasks;
    }

    public void addTask() {
        if (canAddTask()) {
            currentTasks++;
        }
    }

    public int getCompletedTasks() {
        return completedTasks;
    }

    public void resetTasks() {
        currentTasks = 0;
    }

    public void printStatus() {
        System.out.println("Manager: " + name);
        System.out.println("Tasks: " + currentTasks + "/" + maxTasks);
    }

    public void simulateWorkload() {
        addTask();
        addTask();
        removeTask();
        addTask();
        printStatus();
    }

    public void logStart() {
        System.out.println("Starting task manager...");
    }

    public void logEnd() {
        System.out.println("Stopping task manager...");
    }

    public void fullRun() {
        logStart();
        simulateWorkload();
        logEnd();
    }

    public static void main(String[] args) {
        TaskManager tm = new TaskManager("Primary", 5);
        tm.fullRun();
    }
}
