const hourHand = document.querySelector("#hour");
const minuteHand = document.querySelector("#minute");
const secondHand = document.querySelector("#second");

var date = new Date();
let hr = date.getHours();
let min = date.getMinutes();
let sec = date.getSeconds();

let secPosition = sec * 360 / 60;
let minPosition = (min * 360 / 60) + (secPosition / 60);
let hrPosition = (hr * 360 / 12) + (minPosition / 12);

function runTheClock() {
    hrPosition += (3 / 360)
    minPosition += (6 / 60)
    secPosition += 6

    hourHand.style.transform = "rotate(" + hrPosition + "deg)";
    minuteHand.style.transform = "rotate(" + minPosition + "deg)";
    secondHand.style.transform = "rotate(" + secPosition + "deg)";
}

var interval = setInterval(runTheClock, 1000)