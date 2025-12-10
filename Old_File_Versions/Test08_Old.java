public class LightSwitch {
    private boolean isOn;

    public LightSwitch() {
        isOn = false;
    }

    public void turnOn() {
        isOn = true;
    }

    public void turnOff() {
        isOn = false;
    }

    public void toggle() {
        isOn = !isOn;
    }

    public boolean getState() {
        return isOn;
    }

    public static void main(String[] args) {
        LightSwitch light = new LightSwitch();
        light.turnOn();
        light.toggle();
        System.out.println("Light is on: " + light.getState());
    }
}
