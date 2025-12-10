public class Counter {
    private int count;

    public Counter() {
        count = 0;
    }

    public void increment() {
        count++;
    }

    public void decrement() {
        if(count > 0) {
            count--;
        }
    }

    public void reset() {
        count = 0;
    }

    public int getCount() {
        return count;
    }

    public static void main(String[] args) {
        Counter c = new Counter();
        c.increment();
        c.increment();
        c.decrement();
        c.reset();
        System.out.println("Count: " + c.getCount());
    }
}
