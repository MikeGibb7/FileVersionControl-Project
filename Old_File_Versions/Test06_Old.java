public class TemperatureConverter {

    private double celsius;
    private double fahrenheit;

    public TemperatureConverter() {
        celsius = 0.0;
        fahrenheit = 32.0;
    }

    public void setCelsius(double c) {
        celsius = c;
        fahrenheit = (c * 9/5) + 32;
    }

    public void setFahrenheit(double f) {
        fahrenheit = f;
        celsius = (f - 32) * 5/9;
    }

    public double getCelsius() {
        return celsius;
    }

    public double getFahrenheit() {
        return fahrenheit;
    }

    public void printValues() {
        System.out.println("Celsius: " + celsius);
        System.out.println("Fahrenheit: " + fahrenheit);
    }
}
