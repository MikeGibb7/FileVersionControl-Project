public class LibraryManager {

    private String libraryName;
    private int totalBooks;
    private boolean open;

    public LibraryManager(String name) {
        this.libraryName = name;
        this.totalBooks = 0;
        this.open = true;
    }

    public void openLibrary() {
        open = true;
    }

    public void closeLibrary() {
        open = false;
    }

    public boolean isOpen() {
        return open;
    }

    public void addBooks(int count) {
        totalBooks += count;
    }

    public void printStatus() {
        System.out.println("Library: " + libraryName);
        System.out.println("Total books: " + totalBooks);
        System.out.println("Open: " + open);
    }

    public void audit() {
        System.out.println("Audit started");

        logAudit();          // added
        removeBooks(3);      // moved
        addBooks(10);        // moved

        System.out.println("Audit completed");
    }

    private void logAudit() { // added
        System.out.println("Logging audit activity");
    }

    public int getTotalBooks() {
        return totalBooks;
    }

    public String getLibraryName() {
        return libraryName;
    }

    public static void main(String[] args) {
        LibraryManager lm = new LibraryManager("Central");
        lm.addBooks(50);
        lm.audit();
        lm.printStatus();
    }
}