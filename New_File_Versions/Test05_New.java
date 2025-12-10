public class ShoppingCart {

    private int itemCount;
    private double totalPrice;
    private double taxRate; // added

    public ShoppingCart() {
        itemCount = 0;
        totalPrice = 0.0; // initialize price
        taxRate = 0.13;   // added
    }

    public void printCart() {
        System.out.println("Items: " + itemCount);
        System.out.println("Total: $" + totalPrice);
    }

    public void addItem(double price) {
        itemCount++;
        totalPrice += price;
    }

    // removed removeItem(double price)

    public void applyTax() { // added method
        totalPrice = totalPrice * (1 + taxRate);
    }

    public double getTotalPrice() {
        return totalPrice;
    }
}
