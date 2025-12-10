public class ShoppingCart {

    private int itemCount;
    private double totalPrice;

    public ShoppingCart() {
        itemCount = 0;
        totalPrice = 0.0;
    }

    public void addItem(double price) {
        itemCount++;
        totalPrice += price;
    }

    public void removeItem(double price) {
        itemCount--;
        totalPrice -= price;
    }

    public void printCart() {
        System.out.println("Items: " + itemCount);
        System.out.println("Total: $" + totalPrice);
    }

    public double getTotalPrice() {
        return totalPrice;
    }
}
