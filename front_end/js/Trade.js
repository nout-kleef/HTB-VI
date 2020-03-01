class Trade {
    constructor(time, isBuy, price, volume) {
        this.x = time;
        this.y = price;
        this.color = isBuy ? "green" : "red";
        this.radius = 10; // implement volume later
    }
}
