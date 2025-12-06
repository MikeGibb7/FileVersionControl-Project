public class TemperatureConverter {

    public static double toCelsius(double fahrenheit) {
        double result = (fahrenheit - 32) * 5 / 9;
        return result;
    }

    public static double toFahrenheit(double celsius) {
        double result = (celsius * 9 / 5) + 32;
        return result;
    }

    public static void main(String[] args) {
        double f = 98.6;
        double c = toCelsius(f);

        System.out.println("F to C: " + c);

        double c2 = 37.0;
        double f2 = toFahrenheit(c2);

        System.out.println("C to F: " + f2);
    }
}
