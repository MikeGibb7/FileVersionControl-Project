public class LightSwitch {
    private boolean isOn;
    private String location; // added

    public LightSwitch() {
        isOn = false;
        location = "Living Room"; // added
    }

    public void toggle() { // moved
        isOn = !isOn;
    }

    public void turnOn() { // moved
        isOn = true;
    }

    public void turnOff() { // moved
        isOn = false;
    }

    public boolean getState() {
        return isOn;
    }

    public void setLocation(String loc) { // added method
        location = loc;
    }

    public String getLocation() { // added method
        return location;
    }

    public static void main(String[] args) {
        LightSwitch light = new LightSwitch();
        light.setLocation("Bedroom"); // added test
        light.turnOn();
        light.toggle();
        System.out.println("Light is on: " + light.getState());
        System.out.println("Location: " + light.getLocation()); // added
    }
}
