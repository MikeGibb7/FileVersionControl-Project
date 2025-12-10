public class Counter {
    private int count;
    private int step; // added

    public Counter() {
        count = 0;
        step = 1; // added
    }

    public void decrement() { // moved
        if(count > 0) {
            count--;
        }
    }

    public void increment() { //moved
        count++;
    }

    public void reset() {
        count = 0;
    }

    public int getCount() {
        return count;
    }

    public void setStep(int s) { // added method
        step = s;
    }

    public static void main(String[] args) {
        Counter c = new Counter();
        c.setStep(2); // added test
        c.increment();
        c.increment();
        c.decrement();
        c.reset();
        System.out.println("Count: " + c.getCount());
    }
}
