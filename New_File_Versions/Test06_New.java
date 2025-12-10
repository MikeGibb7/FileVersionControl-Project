public class TemperatureConverter {

    private double celsius;
    private double fahrenheit;
    private double kelvin; // added

    public void printValues() { // moved higher
        System.out.println("Celsius: " + celsius);
        System.out.println("Fahrenheit: " + fahrenheit);
        System.out.println("Kelvin: " + kelvin); // added
    }

    public TemperatureConverter() {
        celsius = 0.0;
        fahrenheit = 32.0;
        kelvin = 273.15; // added
    }

    public void setCelsius(double c) {
        celsius = c;
        fahrenheit = (c * 9/5) + 32;
        kelvin = c + 273.15; // added
    }

    // removed setFahrenheit(double f)

    public void setKelvin(double k) { // added new method
        kelvin = k;
        celsius = k - 273.15;
        fahrenheit = (celsius * 9/5) + 32;
    }

    public double getCelsius() {
        return celsius;
    }

    public double getFahrenheit() {
        return fahrenheit;
    }

    public double getKelvin() {
        return kelvin; // added
    }
}
