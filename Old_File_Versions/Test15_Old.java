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

    public void removeBooks(int count) {
        if (totalBooks >= count) {
            totalBooks -= count;
        }
    }

    public void printStatus() {
        System.out.println("Library: " + libraryName);
        System.out.println("Total books: " + totalBooks);
        System.out.println("Open: " + open);
    }

    public void audit() {
        System.out.println("Audit started");
        addBooks(10);
        removeBooks(3);
        System.out.println("Audit completed");
    }

    public void resetInventory() {
        totalBooks = 0;
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