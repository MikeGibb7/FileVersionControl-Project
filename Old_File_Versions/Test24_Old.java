public class Test24 {

    private int counter;
    private String name;

    public Test24(String name) {
        this.name = name;
        this.counter = 0;
    }

    public void start() {
        initialize();
        process();
        finish();
    }

    private void initialize() {
        System.out.println("Initializing...");
        counter = 1;
        logState();
    }

    private void process() {
        for (int i = 0; i < 5; i++) {
            counter += i;
            updateStatus(i);
            validate(counter);
        }
    }

    private void finish() {
        cleanup();
        System.out.println("Done");
    }

    private void updateStatus(int step) {
        System.out.println("Step: " + step);
        saveProgress(step);
    }

    private void saveProgress(int value) {
        if (value % 2 == 0) {
            System.out.println("Saving even step");
        } else {
            System.out.println("Skipping odd step");
        }
    }

    private void validate(int value) {
        if (value < 0) {
            throw new IllegalStateException("Invalid value");
        }
    }

    private void cleanup() {
        System.out.println("Cleaning resources");
        reset();
    }

    private void reset() {
        counter = 0;
    }

    private void logState() {
        System.out.println("Counter = " + counter);
        System.out.println("Name = " + name);
    }

    private void unusedMethodA() {
        System.out.println("Unused A");
    }

    private void unusedMethodB() {
        System.out.println("Unused B");
    }

    private void unusedMethodC() {
        System.out.println("Unused C");
    }

    private void helperOne() {
        System.out.println("Helper One");
    }

    private void helperTwo() {
        System.out.println("Helper Two");
    }

    private void helperThree() {
        System.out.println("Helper Three");
    }

    private void helperFour() {
        System.out.println("Helper Four");
    }

    private void helperFive() {
        System.out.println("Helper Five");
    }

    private void helperSix() {
        System.out.println("Helper Six");
    }

    private void helperSeven() {
        System.out.println("Helper Seven");
    }

    private void helperEight() {
        System.out.println("Helper Eight");
    }

    private void helperNine() {
        System.out.println("Helper Nine");
    }

    private void helperTen() {
        System.out.println("Helper Ten");
    }
}
