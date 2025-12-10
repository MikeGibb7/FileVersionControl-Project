public class Rectangle {
    private int width;
    private int height;
    private String color; // added

    public Rectangle(int w, int h) { 
        width = w;
        height = h;
    }

    public int getPerimeter() { // moved
        return 2 * (width + height);
    }
    
    public void setColor(String c) { // added
        color = c;
    }

    public String getColor() { // added
        return color;
    }

    public void printDetails() { // added
        System.out.println("Width: " + width);
        System.out.println("Height: " + height);
        System.out.println("Color: " + color);
        System.out.println("Perimeter: " + getPerimeter());
    }

    public static void main(String[] args) {
        Rectangle r = new Rectangle(5, 10);
        r.setColor("Red"); // added
        r.printDetails();  // added
    }
}
