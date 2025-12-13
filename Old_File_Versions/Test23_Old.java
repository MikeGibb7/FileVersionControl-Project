public class Library {
    private String name;
    private String location;
    private int capacity;
    private List<Book> books;
    private List<Librarian> staff;
    
    public Library(String name, String location, int capacity) {
        this.name = name;
        this.location = location;
        this.capacity = capacity;
        this.books = new ArrayList<>();
        this.staff = new ArrayList<>();
    }
    
    public void addBook(Book book) {
        if (books.size() < capacity) {
            books.add(book);
        }
    }
    
    public void removeBook(Book book) {
        books.remove(book);
    }
    
    public Book findBookByTitle(String title) {
        for (Book book : books) {
            if (book.getTitle().equals(title)) {
                return book;
            }
        }
        return null;
    }
    
    public void hireLibrarian(Librarian librarian) {
        staff.add(librarian);
    }
    
    public void fireLibrarian(Librarian librarian) {
        staff.remove(librarian);
    }
    
    public List<Book> getBooks() {
        return books;
    }
    
    public List<Librarian> getStaff() {
        return staff;
    }
    
    public void openLibrary() {
        System.out.println("Library " + name + " is now open at " + location);
    }
    
    public void closeLibrary() {
        System.out.println("Library " + name + " is now closed.");
    }
    
    public int totalBooks() {
        return books.size();
    }
    
    public int totalStaff() {
        return staff.size();
    }
    
    public static void main(String[] args) {
        Library lib = new Library("Central Library", "Downtown", 1000);
        lib.openLibrary();
    }
}
