public class BankAccount {
    private double balance;
    private String owner; // added

    public BankAccount(double initialBalance, String ownerName) { 
        balance = initialBalance;
        owner = ownerName; // added
    }

    public void withdraw(double amount) { // moved
        if(amount <= balance) {
            balance -= amount;
        }
    }

    public void deposit(double amount) { // moved
        balance += amount;
    }

    public double getBalance() {
        return balance;
    }

    public String getOwner() { // added method
        return owner;
    }

    public void setOwner(String name) { // added method
        owner = name;
    }

    public static void main(String[] args) {
        BankAccount account = new BankAccount(100); 
        account.deposit(50);
        account.withdraw(30);
        account.setOwner("Bob"); // added test
        System.out.println("Balance: " + account.getBalance());
        System.out.println("Owner: " + account.getOwner()); // added
    }
}
